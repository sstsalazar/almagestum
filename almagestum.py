import inspect
import sys

import almagestum.fetcher

class Almagestum:
    def __init__(self, source, sections):
        #self.__source = None
        #self.__sections = None
        self.set_source(source)
        self.set_sections(sections)
        self.fetcher = self.set_fetcher()

    def set_source(self, source):
        """
        Check if the sections were passed as a valid dict.

        :param dict source: The data structure that contains the sections info.
        """
        if not isinstance(source, dict):
            raise TypeError("The source must be passed as a dict.")
        else:
            missing = []
            if "name" not in source:
                missing.append("name")
            if "url" not in source:
                missing.append("url")
            if "method" not in source:
                missing.append("method")
            if len(missing) != 0:
                raise ValueError("Missing the obligatory source tags: ".format("".join([m+"," for m in missing])[0:-1]))
        self.__source = source

    def set_sections(self, sections):
        """
        Check if the sections were passed as a valid list.

        :param list sections: The data structure that contains the sections info.
        """
        if not isinstance(sections, list):
            raise TypeError("The sections must be passed as a list.")
        else:
            for s in sections:
                missing = []
                if "path" not in s:
                    missing.append("path")
                if "fetch" not in s:
                    missing.append("fetch")
                if "tags" not in s:
                    missing.append("tags")
                if len(missing) != 0:
                    raise ValueError("Missing the obligatory section tags: ".format(
                        "".join([m + "," for m in missing])[0:-1]))
        self.__sections = sections

    def set_fetcher(self):
        fetchers = self.get_fetchers()
        if self.__source["method"] in fetchers:
            return fetchers[self.__source["method"]](self.__source["url"])
        else:
            raise  ValueError("Acquisition method \"{} \"is not available: ".format(
                self.__source["method"] ))

    def get_fetchers(self):
        # Use dict comprehesion to get the concrete Fetcher classes available.
        fetchers = { c[0].replace("Fetcher","") : c[1] for c in inspect.getmembers(almagestum.fetcher, inspect.isclass) if not inspect.isabstract(c[1])}
        try:
            import almagestum_extra
            fetchers.update( { c[0].replace("Fetcher","") : c[1] for c in inspect.getmembers(almagestum_extra, inspect.isclass) if not inspect.isabstract(c[1])} )
        except:
            print("Module almagestum_extra not available.")
        return fetchers

    def get_metadata(self):
        return self.fetcher.results

    def get_log(self):
        return self.fetcher.log

    def scrap(self):
        """
        Scrap the information out of the resource.
        """
        try:
            for s in self.__sections:
                self.fetcher.scrap( s )
        except Exception as err:
            print("Error in the scrap execution: {}".format(err))
            sys.exit(-1)

    def fetch(self, path):
        """
        Fetch the data requested from the resource available.
        """
        try:
            for s in self.__sections:
                for tag in s["fetch"]:
                    self.fetcher.fetch(tag)
        except Exception as err:
            print("Error in the fetch execution: {}".format(err))
            sys.exit(-1)
