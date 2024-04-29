from utils.statement_aggregator import StatementAggregator
from utils.spending_visualizer import SpendingVisualizer
from utils.storage_client import StorageClient
import datetime
import os
import time
import shutil

if __name__ == "__main__":
    storage_client = StorageClient()

    aggregator = StatementAggregator(storage_client)
    visualizer = SpendingVisualizer(storage_client)

    # Clean folders if they exist (They should not at this stage)
    if os.path.exists("./Transactions To Edit"):
        shutil.rmtree("./Transactions To Edit")
    if os.path.exists("./Spending"):
        shutil.rmtree("./Spending")

    # Read statements
    aggregator.read_statements()

    while True:
        # Clear the terminal
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
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

        # Show spending for this month
        if choice == 1:
            visualizer.generate_graph(datetime.datetime.now().strftime("%Y-%m"))
        # Show all time spending
        if choice == 2:
            visualizer.generate_graphs()
        # Edit transactions for a month
        if choice == 3:
            date = input("Which transactions would you like to modify? (MM-YYYY): ")
            month, year = date.split("-")
            storage_client.edit_transactions(f"{year}-{month}")
        # Exit
        if choice == 4:
            break
        time.sleep(3)
