from utils.secrets import Secrets
import os
from google.cloud import storage
import pandas as pd
import json

class StorageClient:
    """
    This client is used to interact with the Google Cloud Storage service
    """

    def __init__(self):
        Secrets().read_gcp_secrets()

        # Retrieve GCP credentials from the secrets file
        self.storage_client = storage.Client(project=os.environ["project_id"])
        self.bucket_name = os.environ["bucket"]

        # Retrieve the GCS Bucket containing all the transaction data
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

    def edit_transactions(self, date):
        """
        This function pulls a file from GCS and allows the user to edit it before reuploading it
        """
        # Retrieve budget values
        with open("budget.json", "r") as f:
            self.budget_categories = json.load(f).keys()
        file_name = f"{date}.csv"

        # Get the specific blob containing the csv
        blob = self.bucket.blob(file_name)
        if not blob.exists():
            print("There are no transactions for this time period.")
            return
        
        # Create the directory where the file will be downloaded to
        os.mkdir('./Transactions To Edit')
        blob.download_to_filename(f"./Transactions To Edit/{blob.name}")
        print(f'{file_name} has been downloaded to the `Transactions To Edit` folder. Please make your changes.')
        print()
        while os.path.exists('./Transactions To Edit'):
            input("Press enter to continue...")
            updated_df = pd.read_csv(f'./Transactions To Edit/{file_name}')

            # Check that all categories assigned to the transactions are valid
            invalid_categories = set(updated_df["Category"]) - set(
                        self.budget_categories
                    )
            if invalid_categories:
                        print(
                            f"The following categories for {file_name[:-4]} are invalid. Please revise them:"
                        )
                        for cat in invalid_categories:
                            print(f"- {cat}")
                            print()
                        continue
            blob.upload_from_string(updated_df.to_csv(index=False))
            os.remove(f'./Transactions To Edit/{file_name}')
            os.rmdir(f'./Transactions To Edit')
        print(f'Transactions for {date} have successfully been updated.')

    def get_blob(self, file):
        """
        This function returns the GCS blob containing the desired csv
        """
        return self.bucket.blob(file)

    def list_blobs(self):
        """
        This function lists all the files present in the bucket
        """
        return list(self.bucket.list_blobs())
        
