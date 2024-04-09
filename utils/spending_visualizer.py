import os
import pandas as pd
import plotly.express as px

class SpendingVisualizer:
    def generate_graphs(self, time):
        file = f'{time}.csv'
        statement_path = f'./spending/{file}'
        if not os.path.exists(statement_path):
            print("There are no statements for this time period.")

        timeframe = file[:-4]
        transactions = pd.read_csv(statement_path)
        category_totals = transactions.groupby('Category')['Amount'].sum().reset_index()

        # Plot the bar graph
        fig = px.bar(category_totals, x='Category', y='Amount', title='Spending by Category')
        fig.show()