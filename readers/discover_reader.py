import pandas as pd


class DiscoverReader:
    """This class will be used to read statements from Discover"""

    def __init__(self):
        # Initialize all the category mappings from the bank to this app
        self.category_mappings = {
            "Automotive": "Random Purchases",
            "Department Stores": "Random Purchases",
            "Education": "Random Purchases",
            "Gasoline": "Travel",
            "Government Services": "Random Purchases",
            "Home Improvement": "Random Purchases",
            "Medical Services": "Personal Health",
            "Merchandise": "Random Purchases",
            "Restaurants": "Eating Out",
            "Services": "Random Purchases",
            "Supermarkets": "Groceries",
            "Travel/ Entertainment": "Random Purchases",
            "Wholesale Clubs": "Groceries",
            "Awards and Rebate Credits": "Awards and Rebate Credits",
            "Balance Transfers": "Balance Transfers",
            "Cash Advances": "Cash Advances",
            "Fees": "Random Purchases",
            "Interest": "Random Purchases",
            "Other/ Miscellaneous": "Random Purchases",
            "Payments and Credits": "Payments and Credits",
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
        transactions = transactions.drop(columns=["Post Date"])

        # Drop rows with irrelevant categories
        categories_to_drop = [
            "Payments and Credits",
            "Awards and Rebate Credits",
            "Balance Transfers",
            "Cash Advances",
        ]
        mask = transactions["Category"].isin(categories_to_drop)
        transactions.drop(transactions[mask].index, inplace=True)

        # Normalize the name of the `Trans. Date` column to `Transaction Date`
        transactions = transactions.rename(columns={"Trans. Date": "Transaction Date"})

        return transactions
