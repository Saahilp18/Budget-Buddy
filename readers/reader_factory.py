from readers.capone_reader import CaponeReader
from readers.chase_reader import ChaseReader
from readers.discover_reader import DiscoverReader
class ReaderFactory:
    def getReader(self, bank):
        if bank == "capone":
            return CaponeReader()
        if bank == "chase":
            return ChaseReader()
        if bank == "discover":
            return DiscoverReader()