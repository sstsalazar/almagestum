from datetime import datetime
from lxml import etree
from urllib import request
from urllib.error import HTTPError
import sys

from almagestum.fetcher import WebFetcher


class XPathFetcher(WebFetcher):

    def scrap(self, section):
        """
        Crawls the webpage and extracts the content associated with the elements desired.

        :param dict section: Dictionary with the tags of the information desired and it's XPath notation path.
        """
        root = self.site.xpath(section["path"])
        # Processes each element of the parse tree
        for e in root:
            # Convert relative links into absolute ones.
            e.make_links_absolute()
            result = {}
            # Verifies the path of the sub element relative to the base search path.
            for k in section["tags"].keys():
                for r in e.xpath(section["tags"][k]):
                    # Different elements will give instances of different classes whose
                    # content extraction method varies.
                    if isinstance(r, etree._ElementUnicodeResult):
                        result[k] = r.strip()
                    else:
                        result[k] = r.text_content().strip()
            self.results.append(result)

    def fetch(self, source):
        """
        Fetches the content of the provided URL and saves it locally.

        :param str source: URL of the source of the content to be downloaded.
        """
        for result in self.results:
            if source in result:
                filename = result[source].rsplit("/")[-1]
                # Date format according to the ISO 8601 international standard in UTC format
                info = dict(Date = datetime.utcnow().isoformat()+'Z' )
                info["File"] = filename
                try:
                    with request.urlopen(result[source]) as response, open(filename, 'wb') as output:
                        data = response.read()  # a `bytes` object
                        output.write(data)
                        info["Status"] = "OK"
                except HTTPError:
                    print("[ERROR] Could not download file {}.".format(filename), file=sys.stderr)
                    info["Status"] = "ERROR"
                self.log.append(info)
