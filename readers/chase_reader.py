import pandas as pd

class ChaseReader:
    def __init__(self):
        self.category_mappings = {
            'Shopping': 'Shopping',
            'nan': 'Misc',
            'Automotive': 'Travel',
            'Bills & Utilities': "Misc",
            'Education': 'Misc',
            'Entertainment': 'Entertainment',
            'Fees & adjustments': 'Misc',
            'Food & drink': 'Eating Out',
            'Gas': 'Travel',
            'Gifts & donations': 'Misc',
            'Groceries': 'Groceries',
            'Health & wellness': "Personal Health",
            'Home': "Housing",
            'Miscellaneous': "Misc",
            'Personal': 'Misc',
            'Professional Services': 'Misc',
            'Travel': 'Travel'
        }
    
    def parseTransactions(self, transactions):
        transactions['Category'] = transactions['Category'].replace(self.category_mappings)
        transactions.drop(transactions[transactions['Type'] == 'Payment'].index, inplace=True)
        transactions = transactions.drop(columns=['Post Date', 'Memo', 'Type'])
        transactions['Amount'] *= -1
        return transactions