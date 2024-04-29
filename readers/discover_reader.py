import pandas as pd


class DiscoverReader:
    def __init__(self):
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
        transactions["Category"] = transactions["Category"].replace(
            self.category_mappings
        )
        transactions = transactions.drop(columns=["Post Date"])
        categories_to_drop = [
            "Payments and Credits",
            "Awards and Rebate Credits",
            "Balance Transfers",
            "Cash Advances"
        ]

        mask = transactions["Category"].isin(categories_to_drop)

        transactions.drop(transactions[mask].index, inplace=True)
        transactions = transactions.rename(columns={'Trans. Date': 'Transaction Date'})
        return transactions
