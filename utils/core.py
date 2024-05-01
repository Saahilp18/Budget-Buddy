from utils.statement_aggregator import StatementAggregator
from utils.spending_visualizer import SpendingVisualizer
from utils.storage_client import StorageClient
import os
import shutil

class Core:
    def __init__(self, ):
        self.storage_client = StorageClient()

        self.aggregator = StatementAggregator(self.storage_client)
        self.visualizer = SpendingVisualizer(self.storage_client)

        # Clean folders if they exist (They should not at this stage)
        if os.path.exists("./Transactions To Edit"):
            shutil.rmtree("./Transactions To Edit")
        if os.path.exists("./Spending"):
            shutil.rmtree("./Spending")