from utils.statement_aggregator import StatementAggregator
from utils.spending_visualizer import SpendingVisualizer
import datetime

aggregator = StatementAggregator().read_statements()

visualizer = SpendingVisualizer()

if __name__ == "__main__":
    print(
        """ 
    1. Show spending for this month
    2. Show all time spending
    3. Show spending for a range of months
        """
    )
    # choice = int(input("Which would you like?: "))
    # if choice == 1:
    #     visualizer.generate_graph(datetime.datetime.now().strftime('%Y-%m'))
    # if choice == 2:
    #     visualizer.generate_graphs()