from abc import abstractmethod
from lxml import html
from urllib import request
from urllib.error import HTTPError
import sys

from almagestum.fetcher  import Fetcher

class WebFetcher(Fetcher):
    def __init__(self, url):
        """
        Constructor for the WebFetcher Class

        :param str url: The URL for the webpage to be scrapped.
        """
        super()
        self.url = url
        self.site = self.catch(url)


    def catch(self, url):
        try:
            return html.parse(request.urlopen(self.url))
        except HTTPError as err:
            print("Error accessing the URL: {}".format(err), file=sys.stderr)
