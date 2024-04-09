import pandas as pd

class CaponeReader:
    def __init__(self):
        self.category_mappings = {
            'Other Services': 'Misc',
            'Payment': 'Payment',
            'Dining': 'Eating Out',
            'Merchandise': 'Misc',
            'Internet': 'Rent',
            'Airfare': 'Travel',
            'Other Travel': 'Travel',
            'Phone/Cable': 'Phone',
            'Grocery': 'Grocery',
            'Gas/Automotive': 'Travel',
            'Healthcare': 'Personal Health',
            'Entertainment': 'Entertainment',
            'Lodging': 'Travel'
        }
    
    def parseTransactions(self, transactions):
        transactions['Category'] = transactions['Category'].replace(self.category_mappings)
        transactions = transactions.drop(columns=['Posted Date', 'Card No.', 'Credit'])
        transactions.drop(transactions[transactions['Category'] == 'Payment/Credit'].index, inplace=True)
        transactions = transactions.rename(columns={'Debit': 'Amount'})
        return transactions