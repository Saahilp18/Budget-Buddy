import os
import pandas as pd
from readers.reader_factory import ReaderFactory
import io
import json
from datetime import datetime


class StatementAggregator:
    """This class takes in all new credit card statements and merges them together by month"""

    def __init__(self, storage_client):
        self.storage_client = storage_client

        # Read the budget limits per category
        with open("budget.json", "r") as f:
            self.budget_limits = json.load(f)

    def read_statements(self):
        """
        This function will read all the credit card statements, merge them together, and upload them to Google Storage
        """

        dir = "./Statements"
        files = os.listdir(dir)
        spending_dir = "./Spending"

        # Create the directory where the aggregated statements will be stored
        if not os.path.exists(spending_dir):
            os.mkdir(spending_dir)

        # Read all statements
        for file in files:
            statement_path = f"./{dir}/{file}"
            bank, card = file[:-4].split("-")
            transactions = pd.read_csv(statement_path)

            # Parse the transactions
            transactions = (
                ReaderFactory().getReader(bank).parseTransactions(transactions)
            )

            # Convert the Transaction date to datetime and format it correctly
            transactions["Transaction Date"] = pd.to_datetime(
                transactions["Transaction Date"]
            ).dt.strftime("%Y-%m-%d")

            # Add a column for which credit card the purchase was made on
            transactions["Card"] = card

            # Find all the unique dates in the data
            unique_dates = (
                pd.to_datetime(transactions["Transaction Date"])
                .dt.strftime("%Y-%m")
                .unique()
            )

            # Filter out dates that have already been read
            dfs = []
            # aggregate all relevant dataframes
            for date in unique_dates:
                file = f"{date}.csv"
                blob = self.storage_client.get_blob(file)
                # if data exists for this date, add it
                if blob.exists():
                    dfs.append(pd.read_csv(blob.open()))

            if dfs:
                combined_dfs = pd.concat(dfs, ignore_index=True)
                # Merge transactions and combined_dfs on all columns
                merged = pd.merge(
                    transactions, combined_dfs, how="left", indicator=True
                )

                # Print rows present in both dataframes
                both_present = merged[merged["_merge"] == "both"].drop(
                    columns=["_merge", "Card"]
                )
                if not both_present.empty:
                    print(
                        f"Here are duplicate transactions that will be omitted for your {card} card:"
                    )
                    print(both_present.to_markdown(index=False))

                # Filter out rows present in both DataFrames
                transactions = merged[merged["_merge"] == "left_only"].copy()

                # Drop the '_merge' column as it's no longer needed
                transactions.drop(columns="_merge", inplace=True)

            # Allocate the data to the correct JSON file by year-month
            for date in unique_dates:
                filtered_transactions = transactions[
                    transactions["Transaction Date"].str[:7] == date
                ]
                file_path = f"{spending_dir}/{date}.csv"
                if os.path.exists(file_path):
                    filtered_transactions.to_csv(
                        file_path, mode="a", header=False, index=False
                    )
                else:
                    # If this is the first time creating the file, include the basic expenditures that will be made every month
                    if not self.storage_client.get_blob(f"{date}.csv").exists():
                        static_categories = [
                            "Rent/Utilities",
                            "401k",
                            "Savings",
                            "Investments",
                        ]
                        static_df = pd.DataFrame(
                            [
                                {
                                    "Transaction Date": f"{date}-00",
                                    "Description": static_cat,
                                    "Category": static_cat,
                                    "Amount": self.budget_limits[static_cat],
                                    "Card": "N/A",
                                }
                                for static_cat in static_categories
                            ]
                        )
                        filtered_transactions = pd.concat(
                            [filtered_transactions, static_df], ignore_index=True
                        )

                    # Write the filtered transactions to a csv for editing as long as the df is not empty
                    if not filtered_transactions.empty:
                        filtered_transactions.to_csv(file_path, index=False)

            # Remove the statement as it is no longer needed
            os.remove(statement_path)

        if os.listdir(spending_dir):
            # Sort transactions by date for readability
            for file in os.listdir(spending_dir):
                df = pd.read_csv(spending_dir + "/" + file)
                df = df.sort_values(
                    by="Transaction Date",
                    ascending=True,
                    ignore_index=True,
                )
                df.to_csv(spending_dir + "/" + file, index=False)

            print(
                f"""
Finished processing statements! Please adjust the transactions in the Spending folder before continuing.

Here are the following budget categories:"""
            )
            for cat in self.budget_limits.keys():
                print(f"\t{cat}")
            print()

            # Check to see if any unrecognized categories still exist
            while os.listdir(spending_dir):
                input("Press enter to continue...")
                print()
                for file in os.listdir(spending_dir):
                    df = pd.read_csv(spending_dir + "/" + file)
                    # Create a set of unrecognized categories in the data
                    invalid_categories = set(df["Category"]) - set(
                        self.budget_limits.keys()
                    )

                    # If unrecognized categories exist, then prompt the user to fix the issue
                    if invalid_categories:
                        print(
                            f"The following categories for {file[:-4]} are invalid. Please revise them:"
                        )
                        for cat in invalid_categories:
                            print(f"- {cat}")
                            print()
                        continue

                    # Remove the file since all its contents have been processed
                    os.remove(spending_dir + "/" + file)

                    # If there are no new transactions to upload, then skip this file
                    if df.empty:
                        continue

                    # Retrieve the Google Cloud Storage blob containing the csv
                    blob = self.storage_client.get_blob(file)

                    # If there is existing data for the relevant month, append to the data. Otherwise, create a new csv
                    existing_df = (
                        pd.read_csv(io.BytesIO(blob.download_as_string()))
                        if blob.exists()
                        else pd.DataFrame()
                    )
                    updated_df = pd.concat([existing_df, df], ignore_index=True)
                    blob.upload_from_string(updated_df.to_csv(index=False))
            print("Transactions have been uploaded!")

        # Remove the Spending directory as it is no longer needed
        os.rmdir(spending_dir)
