from readers.capone_reader import CaponeReader
from readers.chase_reader import ChaseReader

class ReaderFactory:
    def getReader(self, bank):
        if bank == "capone":
            return CaponeReader()
        if bank == "chase":
            return ChaseReader()