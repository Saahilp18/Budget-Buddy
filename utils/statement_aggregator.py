import os
import pandas as pd
from readers.reader_factory import ReaderFactory
from google.cloud import storage
from utils.secrets import Secrets
import io

class StatementAggregator:
    def __init__(self):
        Secrets().read_gcp_secrets()

        self.storage_client = storage.Client(project=os.environ["project_id"])
        self.bucket_name = os.environ["bucket"]
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

    def read_statements(self):
        dir = "./statements"
        files = os.listdir(dir)

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
                blob = self.bucket.blob(file)
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

            # Allocate the data to the correct JSON file by year-month
            for date in unique_dates:
                file_name = f"{date}.csv"
                blob = self.bucket.blob(file_name)

                existing_df = pd.read_csv(io.BytesIO(blob.download_as_string())) if blob.exists() else pd.DataFrame()

                filtered_transactions = transactions[transactions["Transaction Date"].str[:7] == date]

                updated_df = pd.concat([existing_df, filtered_transactions], ignore_index=True)

                blob.upload_from_string(updated_df.to_csv(index=False))

            # os.remove(statement_path)
