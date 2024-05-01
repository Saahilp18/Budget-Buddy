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
-------------------------
0. Aggregate statements
1. Show spending for this month
2. Show spending for a previous month
3. Show all time spending
4. Edit transactions for a month
5. Exit
-------------------------
            """
            )
        choice = int(input("Which would you like?: "))
        # Aggregate files
        if choice == 0:
            aggregator.read_statements()
        # Show spending for this month
        elif choice == 1:
            visualizer.generate_graph(datetime.datetime.now().strftime("%Y-%m"))
        # Show spending for a previous month
        elif choice == 2:
            date = input("Which month would you like to view transactions for? (MM-YYYY): ")
            month, year = date.split("-")
            visualizer.generate_graph(f"{year}-{month}")
        # Show all time spending
        elif choice == 3:
            visualizer.generate_graphs()
        # Edit transactions for a month
        elif choice == 3:
            date = input("Which transactions would you like to modify? (MM-YYYY): ")
            month, year = date.split("-")
            storage_client.edit_transactions(f"{year}-{month}")
        # Exit
        elif choice == 4:
            break
        else:
            print("That is not a valid option. Please try again.")
        time.sleep(3)
