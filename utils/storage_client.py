from utils.secrets import Secrets
import os
from google.cloud import storage

class StorageClient:
    def  __init__(self):
        Secrets().read_gcp_secrets()

        self.storage_client = storage.Client(project=os.environ["project_id"])
        self.bucket_name = os.environ["bucket"]
        self.bucket = self.storage_client.get_bucket(self.bucket_name)

