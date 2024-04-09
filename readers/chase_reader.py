import pandas as pd

class ChaseReader:
    def __init__(self):
        self.category_mappings = {
            'Shopping': "Shopping",
            'nan': "Misc"
        }
    
    def parseTransactions(self, transactions):
        transactions['Category'] = transactions['Category'].replace(self.category_mappings)
        transactions.drop(transactions[transactions['Type'] == 'Payment'].index, inplace=True)
        transactions.drop(transactions[transactions['Category'] == 'Bills & Utilities'].index, inplace=True)
        transactions = transactions.drop(columns=['Post Date', 'Memo', 'Type'])
        transactions['Amount'] *= -1
        return transactions