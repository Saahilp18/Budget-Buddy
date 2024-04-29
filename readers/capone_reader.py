import pandas as pd

class CaponeReader:
    """This class will be used to read statements from Capital One"""

    def __init__(self):
        # Initialize all the category mappings from the bank to this app
        self.category_mappings = {
            "Other Services": "Random Purchases",
            "Payment": "Payment",
            "Dining": "Eating Out",
            "Merchandise": "Random Purchases",
            "Internet": "Home",
            "Airfare": "Travel",
            "Other Travel": "Travel",
            "Phone/Cable": "Phone",
            "Grocery": "Groceries",
            "Gas/Automotive": "Travel",
            "Health Care": "Personal Health",
            "Healthcare": "Personal Health",
            "Entertainment": "Random Purchases",
            "Lodging": "Travel",
            "Fee/Interest Charge": "Random Purchases",
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
        transactions = transactions.drop(columns=["Posted Date", "Card No.", "Credit"])

        # Drop rows with irrelevant categories
        transactions.drop(
            transactions[transactions["Category"] == "Payment/Credit"].index,
            inplace=True,
        )

        # Normalize the name of the `Debit` column to `Amount`
        transactions = transactions.rename(columns={"Debit": "Amount"})

        return transactions
