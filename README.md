#Almagestum

A Python scrapper that works with many data sources. It creates a JSON formated dictionary with the data desired and is able to download files from the specified tags.

Almagestum is named after the book [Almagest](https://en.wikipedia.org/wiki/Almagest) from [Claudius Ptolemaeus](https://en.wikipedia.org/wiki/Ptolemy) and was developed for the BSDC.

##Dependencies

This program requires:
- Python 3.4+.
- [lxml](http://lxml.de/)

##Usage

```
usage: almagestum [-h] -c CONFIGFILE [-d DEST] [-l LOGDEST]

Scraps data out of a URL.

optional arguments:
  -h, --help     show this help message and exit
  -c CONFIGFILE  Config file
  -d DEST        Destination of the extracted data.
  -l LOGDEST     Directory to store the logs.
```

##Configuration

The configuration file is a JSON file with the following structure:

* source - A Dictionary whose keys are obligatory for the program use.
  * name - Name for the repository.
  * url - Base URL where the data is available.
  * method - Method used to scrap the data (XPath, CSSPath and etc)

* sections
  * path - Path as formated by the fetching method specified.
  * fetch - A list with the tags that contain files do be downloaded.
  * tags - A Dictionary that relates the path to the data in the base url and the title given in the extracted data JSON file.
