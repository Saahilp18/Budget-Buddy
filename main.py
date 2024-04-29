from utils.statement_aggregator import StatementAggregator
from utils.spending_visualizer import SpendingVisualizer
from utils.storage_client import StorageClient
import datetime
import os
import time

storage_client = StorageClient()

aggregator = StatementAggregator(storage_client)
aggregator.read_statements()

visualizer = SpendingVisualizer(storage_client)


if __name__ == "__main__":
    while True:
        if os.name == 'nt':
            os.system('cls')
        # For Unix/Linux/MacOS
        else:
            os.system('clear')
            print(
            """ 
Welcome to Budget Buddy!

1. Show spending for this month
2. Show all time spending
3. Edit transactions for a month
4. Exit
            """
        )
        choice = int(input("Which would you like?: "))
        if choice == 1:
            visualizer.generate_graph(datetime.datetime.now().strftime("%Y-%m"))
        if choice == 2:
            visualizer.generate_graphs()
        if choice == 3:
            date = input("Which transactions would you like to modify? (MM-YYYY): ")
            month, year = date.split('-')
            storage_client.edit_transactions(f'{year}-{month}')
        if choice == 4:
            break
        time.sleep(3)
