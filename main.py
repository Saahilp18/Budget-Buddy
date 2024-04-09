from utils.statement_aggregator import StatementAggregator
from utils.spending_visualizer import SpendingVisualizer

aggregator = StatementAggregator().read_statements()

visualizer = SpendingVisualizer()
