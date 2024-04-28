import pandas as pd

class ChaseReader:
    def __init__(self):
        self.category_mappings = {
            'Shopping': 'Random Purchases',
            'nan': 'Random Purchases',
            'Automotive': 'Random Purchases',
            'Bills & Utilities': "Random Purchases",
            'Education': 'Random Purchases',
            'Entertainment': 'Random Purchases',
            'Fees & adjustments': 'Random Purchases',
            'Food & drink': 'Eating Out',
            'Gas': 'Random Purchases',
            'Gifts & donations': 'Random Purchases',
            'Groceries': 'Groceries',
            'Health & wellness': "Personal Health",
            'Home': "Home",
            'Miscellaneous': "Random Purchases",
            'Personal': 'Random Purchases',
            'Professional Services': 'Random Purchases',
            'Travel': 'Random Purchases'
        }
    
    def parseTransactions(self, transactions):
        transactions['Category'] = transactions['Category'].replace(self.category_mappings)
        transactions.drop(transactions[transactions['Type'] == 'Payment'].index, inplace=True)
        transactions = transactions.drop(columns=['Post Date', 'Memo', 'Type'])
        transactions['Amount'] *= -1
        return transactions