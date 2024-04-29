import pandas as pd


class ChaseReader:
    """This class will be used to read statements from Chase"""

    def __init__(self):
        self.category_mappings = {
            "Shopping": "Random Purchases",
            "nan": "Random Purchases",
            "Automotive": "Random Purchases",
            "Bills & Utilities": "Random Purchases",
            "Education": "Random Purchases",
            "Entertainment": "Random Purchases",
            "Fees & adjustments": "Random Purchases",
            "Food & drink": "Eating Out",
            "Gas": "Travel",
            "Gifts & donations": "Random Purchases",
            "Groceries": "Groceries",
            "Health & wellness": "Personal Health",
            "Home": "Home",
            "Miscellaneous": "Random Purchases",
            "Personal": "Random Purchases",
            "Professional Services": "Random Purchases",
            "Travel": "Travel",
        }

    def parseTransactions(self, transactions):
        """
        This method takes in a DataFrame of transactions and normalizes the data  by converting categories into standardized types.

        transactions (DataFrame): These are all the transactions from a specific credit card to be uploaded.
        """

        # Normalize all category names
        transactions["Category"] = transactions["Category"].replace(
            self.category_mappings
        )

        # Drop irrelevant columns
        transactions = transactions.drop(columns=["Post Date", "Memo", "Type"])

        # Drop rows with irrelevant categories
        transactions.drop(
            transactions[transactions["Type"] == "Payment"].index, inplace=True
        )

        # Convert all transactions from negative to positive
        transactions["Amount"] *= -1

        return transactions
