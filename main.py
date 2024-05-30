from utils.core import Core
import datetime
import os
import time

def clear():
    """
    Clears the terminal
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

if __name__ == "__main__":
    core = Core()

    while True:
        clear()
        
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

        choice = input("Which would you like?: ")
        # Aggregate files
        if choice == '0':
            core.aggregator.read_statements()
        # Show spending for this month
        elif choice == '1':
            core.visualizer.generate_graph(datetime.datetime.now().strftime("%m-%Y"))
        # Show spending for a previous month
        elif choice == '2':
            date = input("Which month would you like to view transactions for? (MM-YYYY): ")
            core.visualizer.generate_graph(date)
        # Show all time spending
        elif choice == '3':
            core.visualizer.generate_graphs()
        # Edit transactions for a month
        elif choice == '4':
            date = input("Which transactions would you like to modify? (MM-YYYY): ")
            core.storage_client.edit_transactions(date)
        # Exit
        elif choice == '5':
            break
        else:
            print("That is not a valid option. Please try again.")
        time.sleep(2)
