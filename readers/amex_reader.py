import pandas as pd


class AmexReader:
    """This class will be used to read statements from American Express"""

    def __init__(self):
        # Initialize all the category mappings from the bank to this app
        self.category_mappings = {
            "Restaurant": "Eating Out",
            "Transportation": "Travel",
            "Merchandise & Supplies": "Random Purchases",
            "Other": "Random Purchases",
            "Business Services": "Random Purchases",
            "Entertainment": "Random Purchases",
            "Fees & Adjustments": "Random Purchases",
        }

    def parseTransactions(self, transactions):
        """
        This method takes in a DataFrame of transactions and normalizes the data  by converting categories into standardized types.

        transactions (DataFrame): These are all the transactions from a specific credit card to be uploaded.
        """

        # Drop rows with negative values in the 'Amount' column
        transactions = transactions[transactions["Amount"] >= 0]

        # Extract text before the first dash for categories such as `Transportation-Taxis & Coach`
        transactions.loc[:, "Category"] = transactions["Category"].apply(
            lambda x: x.split("-")[0] if "-" in x else x
        )

        # Normalize all category names
        transactions.loc[:, "Category"] = transactions["Category"].replace(
            self.category_mappings
        )

        # Drop irrelevant columns
        transactions = transactions.drop(
            columns=[
                "Extended Details",
                "Appears On Your Statement As",
                "Address",
                "City/State",
                "Zip Code",
                "Country",
                "Reference",
            ]
        )

        # Normalize the name of the `Date` column to `Transaction Date`
        transactions = transactions.rename(columns={"Date": "Transaction Date"})

        return transactions
