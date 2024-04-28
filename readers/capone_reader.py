import pandas as pd

class CaponeReader:
    def __init__(self):
        self.category_mappings = {
            'Other Services': 'Random Purchases',
            'Payment': 'Payment',
            'Dining': 'Eating Out',
            'Merchandise': 'Random Purchases',
            'Internet': 'Home',
            'Airfare': 'Random Purchases',
            'Other Travel': 'Random Purchases',
            'Phone/Cable': 'Phone',
            'Grocery': 'Groceries',
            'Gas/Automotive': 'Random Purchases',
            'Health Care': 'Personal Health',
            'Healthcare': 'Personal Health',
            'Entertainment': 'Random Purchases',
            'Lodging': 'Random Purchases',
            'Fee/Interest Charge': 'Random Purchases'
        }
    
    def parseTransactions(self, transactions):
        transactions['Category'] = transactions['Category'].replace(self.category_mappings)
        transactions = transactions.drop(columns=['Posted Date', 'Card No.', 'Credit'])
        transactions.drop(transactions[transactions['Category'] == 'Payment/Credit'].index, inplace=True)
        transactions = transactions.rename(columns={'Debit': 'Amount'})
        return transactions