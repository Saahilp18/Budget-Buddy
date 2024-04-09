from utils.statement_aggregator import StatementAggregator
from utils.spending_visualizer import SpendingVisualizer

StatementAggregator().read_statements()

SpendingVisualizer().generate_graphs('2023-06')