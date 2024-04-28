import os
import pandas as pd
from readers.reader_factory import ReaderFactory
import io
import json


class StatementAggregator:
    def __init__(self, storage_client):
        self.storage_client = storage_client
        with open("budget.json", "r") as f:
            self.budget_categories = json.load(f).keys()

    def read_statements(self):
        dir = "./statements"
        files = os.listdir(dir)
        spending_dir = "./spending"
        if not os.path.exists(spending_dir):
            os.mkdir(spending_dir)
        # Read all statements
        for file in files:
            statement_path = f"./{dir}/{file}"
            bank, card = file[:-4].split("-")
            transactions = pd.read_csv(statement_path)

            # Convert the Transaction date to datetime and format it correctly
            transactions["Transaction Date"] = pd.to_datetime(
                transactions["Transaction Date"]
            ).dt.strftime("%Y-%m-%d")

            transactions["Card"] = card

            # Filter out dates that have already been read
            unique_dates = (
                pd.to_datetime(transactions["Transaction Date"])
                .dt.strftime("%Y-%m")
                .unique()
            )

            dfs = []
            # aggregate all relevant dataframes
            for date in unique_dates:
                file = f"{date}.csv"
                blob = self.storage_client.get_blob(file)
                # if data exists for this date, add it
                if blob.exists():
                    dfs.append(pd.read_csv(blob.open()))

            # Parse the transactions
            transactions = (
                ReaderFactory().getReader(bank).parseTransactions(transactions)
            )

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
                        f"Duplicate transactions that will be omitted for your {card} card:"
                    )
                    print(both_present.to_markdown(index=False))

                # Filter out rows present in both DataFrames
                transactions = merged[merged["_merge"] == "left_only"].copy()

                # Drop the '_merge' column as it's no longer needed
                transactions.drop(columns="_merge", inplace=True)

            # # Allocate the data to the correct JSON file by year-month
            for date in unique_dates:
                filtered_transactions = transactions[
                    transactions["Transaction Date"].str[:7] == date
                ]
                file_path = f"./spending/{date}.csv"
                if os.path.exists(file_path):
                    filtered_transactions.to_csv(
                        file_path, mode="a", header=False, index=False
                    )
                else:
                    filtered_transactions.to_csv(file_path, index=False)

            os.remove(statement_path)

        if os.listdir("./spending"):
            print(
                f"""
Finished processing statements! Please adjust the transactions in the spending folder before continuing.

Here are the following budget categories:"""
            )
            for cat in self.budget_categories:
                print(f"\t{cat}")
            print()

            # Check to see if any unrecognized categories still exist
            while os.listdir(spending_dir):
                input("Press enter to continue...")
                print()
                for file in os.listdir(spending_dir):
                    df = pd.read_csv(spending_dir + "/" + file)
                    # Check if there are any unrecognized categories in the data
                    invalid_categories = set(df["Category"]) - set(
                        self.budget_categories
                    )
                    if invalid_categories:
                        print(
                            f"The following categories for {file[:-4]} are invalid. Please revise them:"
                        )
                        for cat in invalid_categories:
                            print(f"- {cat}")
                            print()
                        continue

                    os.remove(spending_dir + "/" + file)
                    if df.empty:
                        continue
                    blob = self.storage_client.get_blob(file)
                    existing_df = (
                        pd.read_csv(io.BytesIO(blob.download_as_string()))
                        if blob.exists()
                        else pd.DataFrame()
                    )
                    updated_df = pd.concat([existing_df, df], ignore_index=True)
                    blob.upload_from_string(updated_df.to_csv(index=False))
            print("Transactions have been uploaded!")
        os.rmdir(spending_dir)
