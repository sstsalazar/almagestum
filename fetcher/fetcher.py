from abc import ABC, abstractmethod

class Fetcher(ABC):
    def __init__(self):
        self.results = []
        self.log = []

    def get_results(self):
        return self.results

    def get_log(self):
        return self.log
    @abstractmethod
    def scrap(self, section):
        pass

    @abstractmethod
    def fetch(self, source):
        pass
