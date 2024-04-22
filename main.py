from utils.statement_aggregator import StatementAggregator
from utils.spending_visualizer import SpendingVisualizer
import datetime
import json

aggregator = StatementAggregator()
aggregator.read_statements()

visualizer = SpendingVisualizer()

if __name__ == "__main__":
    pass
    # print(
    #     """ 
    # 1. Show spending for this month
    # 2. Show all time spending
    # 3. Show spending for a range of months
    # 4. Exit
    #     """
    # )
    # while True:
    #     choice = int(input("Which would you like?: "))
    #     if choice == 1:
    #         visualizer.generate_graph(datetime.datetime.now().strftime('%Y-%m'))
    #     if choice == 2:
    #         visualizer.generate_graphs()
    #     if choice == 3:
    #         time1 = input("Start time (MM-YYYY): ")
    #         time2 = input("End Time: ")
    #         visualizer.generate_timerange_graphs(time1, time2)
    #     if choice == 4:
    #         break