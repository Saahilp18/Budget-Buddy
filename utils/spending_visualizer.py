import os
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

class SpendingVisualizer:
    def __init__(self):
        self.months = {
            '01': "January",
            '02': "February",
            '03': "March",
            '04': "April",
            '05': "May",
            '06': "June",
            '07': "July",
            '08': "August",
            '09': "September",
            '10': "October",
            '11': "November",
            '12': "December"
        }

    def generate_graph(self, time):
        file = f'{time}.csv'
        statement_path = f'./spending/{file}'
        if not os.path.exists(statement_path):
            print("There are no statements for this time period.")
            return
        timeframe = file[:-4]
        transactions = pd.read_csv(statement_path)
        category_totals = transactions.groupby('Category')['Amount'].sum().reset_index()

        # Plot the bar graph
        fig = px.bar(category_totals, x='Category', y='Amount', title='Spending by Category')
        fig.show()
    
    def get_plot_name(self, file):
        year, month = file[:7].split('-')
        return f'{self.months[month]} {year}'
    
    def generate_graphs(self):
        dir = './spending'
        files = os.listdir(dir)
        files.sort(reverse=True)

        # Create a subplot for all graphs
        
        fig = make_subplots(rows=len(files), cols=1, subplot_titles=[self.get_plot_name(file) for file in files])

        row = 1  # Initialize subplot row

        # Read all statements
        for file in files:
            year, month = file[:7].split('-')
            timeframe = f'{self.months[month]} {year}'
            statement_path = f'./{dir}/{file}'
            if not os.path.exists(statement_path):
                print("There are no statements for this time period.")
                return

            transactions = pd.read_csv(statement_path)
            category_totals = transactions.groupby('Category')['Amount'].sum().reset_index()

            # Add bar trace to subplot
            fig.add_trace(go.Bar(x=category_totals['Category'], y=category_totals['Amount'], name=timeframe), row=row, col=1)

            # Set x-axis tickvals and ticktext
            fig.update_xaxes(tickvals=list(range(len(category_totals))), ticktext=category_totals['Category'], row=row, col=1)
            
            row += 1  # Move to next subplot row

        # Update layout
        fig.update_layout(title='Spending Analysis', showlegend=False, height=5000)
        fig.update_yaxes(range=[0, 2000], tickmode='linear', tick0=0, dtick=100)

        # Show the plot
        fig.show()
