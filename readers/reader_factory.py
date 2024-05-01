from readers.capone_reader import CaponeReader
from readers.chase_reader import ChaseReader
from readers.discover_reader import DiscoverReader
from readers.amex_reader import AmexReader
class ReaderFactory:
    def __init__(self):
        self.column_order = [
            'Transaction Date',
            'Description',
            'Category',
            'Amount'
        ]
        
    def getReader(self, bank):
        if bank == "capone":
            return CaponeReader(self.column_order)
        if bank == "chase":
            return ChaseReader(self.column_order)
        if bank == "discover":
            return DiscoverReader(self.column_order)
        if bank == "amex":
            return AmexReader(self.column_order)