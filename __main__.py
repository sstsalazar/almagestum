import argparse
import hashlib
import json
import os
from almagestum import Almagestum

def hash(filepath, hashfunction=hashlib.md5()):
    '''
    Calculates the hash value of a file.

    :param str filepath: Path to the file to be analyzed.
    :param constructor hashfunction: A hashlib constructor to calculate the file hash value. Defaults to md5.
    '''
    hash = hashfunction
    with open(filepath, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()



def access_path(path):
    """
    Verifies if the current proccess is in the path desired and if not changes the current working directory to it
    """
    if os.getcwd() != path:
        if os.access(path, os.R_OK):
            return True
        else:
            try:
                os.makedirs(path)
            except:
                raise ("Directory {} is not accessible!".format(path))

def print_json(data, filename):
    """
    Writes a dictionary into a JSON file.
    :param dict data: Data dictionary to be printed.
    :param str log: Filename of the output file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    """
    Execute the script with the JSON config file passed.
    """
    parser = argparse.ArgumentParser(description="Scraps data out of a URL.")
    parser.prog = "almagestum"
    parser.add_argument("-c", action="store", dest="configFile",
                        help="Config file", required=True)
    parser.add_argument("-d", action="store", type=str, dest="dest", default=".",
                        help="Destination of the extracted data.")
    parser.add_argument("-l", action="store", type=str,dest="logDest", default=".",
                        help=" Directory to store the logs.")
    parameters = parser.parse_args()
    with open(parameters.configFile) as configFile:
        config = json.load(configFile)
    # Verify paths accessibility
    pwd = os.getcwd()
    access_path(parameters.dest)
    access_path(parameters.logDest)
    #Scrap Data
    scraper = Almagestum(config["source"], config["sections"])
    scraper.scrap()
    # Save Data and Metadata and hashes
    os.chdir(parameters.dest)
    scraper.fetch(parameters.dest)
    print_json(scraper.get_metadata(), "data.json")
    logs = scraper.get_log()
    for log in logs:
        if log["Status"] == "OK":
            log['Hash'] = hash(log['File'])
    # SaVe Log and hashes
    os.chdir(pwd)
    os.chdir(parameters.logDest)
    print_json( logs, "log.json")
    # Sava hashes
    os.chdir(pwd)
