import pandas as pd


class ChaseReader:
    """This class will be used to read statements from Chase"""

    def __init__(self, column_order):
        self.column_order = column_order

        # Initialize all the category mappings from the bank to this app
        self.category_mappings = {
            "Shopping": "Random Purchases",
            "nan": "Random Purchases",
            "Automotive": "Random Purchases",
            "Bills & Utilities": "Random Purchases",
            "Education": "Random Purchases",
            "Entertainment": "Random Purchases",
            "Fees & Adjustments": "Random Purchases",
            "Food & Drink": "Eating Out",
            "Gas": "Travel",
            "Gifts & Donations": "Random Purchases",
            "Groceries": "Groceries",
            "Health & Wellness": "Personal Health",
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

        # Drop rows with irrelevant categories
        transactions.drop(
            transactions[transactions["Type"] == "Payment"].index, inplace=True
        )

        # Drop irrelevant columns
        transactions = transactions.drop(columns=["Post Date", "Memo", "Type"])

        # Convert all transactions from negative to positive
        transactions["Amount"] *= -1

        return transactions[self.column_order]
