import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import datetime


class SpendingVisualizer:
    def __init__(self):
        self.months = {
            "01": "January",
            "02": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December",
        }

        with open("budget.json", "r") as f:
            budget_limits = json.load(f)
            self.budget_df = pd.DataFrame(
                list(budget_limits.items()), columns=["Category", "Budget"]
            )

    def generate_graph(self, time):
        file = f"{time}.csv"
        statement_path = f"./spending/{file}"
        if not os.path.exists(statement_path):
            print("There are no statements for this time period.")
            return

        transactions = pd.read_csv(statement_path)
        category_totals = transactions.groupby("Category")["Amount"].sum().reset_index()
        category_totals = pd.merge(
            category_totals, self.budget_df, on="Category", how="left"
        )
        category_totals['Formatted Amount'] = '$' + category_totals['Amount'].round(2).astype(str)

        # Create figure
        total_spent = category_totals['Amount'].sum()

        fig = px.bar(
            category_totals,
            x="Category",
            y="Amount",
            title=f"Total Amount Spent For This Month: ${total_spent}",
            color=category_totals["Amount"] < category_totals["Budget"],
            color_discrete_map={True: "rgba(0, 255, 0, 0.5)", False: "rgba(255, 0, 0, 0.5)"},
            text="Formatted Amount",
        )

        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)

        # Show figure
        fig.show()

    def get_plot_name(self, file):
        year, month = file[:7].split("-")
        return f"{self.months[month]} {year}"

    def generate_graphs(self):
        dir = "./spending"
        files = os.listdir(dir)
        files.sort(reverse=True)

        # Create a subplot for all graphs

        fig = make_subplots(
            rows=len(files),
            cols=1,
            subplot_titles=[self.get_plot_name(file) for file in files],
        )

        row = 1  # Initialize subplot row

        # Read all statements
        for file in files:
            year, month = file[:7].split("-")
            timeframe = f"{self.months[month]} {year}"
            statement_path = f"./{dir}/{file}"
            if not os.path.exists(statement_path):
                print("There are no statements for this time period.")
                return

            transactions = pd.read_csv(statement_path)
            category_totals = (
                transactions.groupby("Category")["Amount"].sum().reset_index()
            )

            # Add bar trace to subplot
            fig.add_trace(
                go.Bar(
                    x=category_totals["Category"],
                    y=category_totals["Amount"],
                    name=timeframe,
                ),
                row=row,
                col=1,
            )
            
            # Set x-axis tickvals and ticktext
            fig.update_xaxes(
                tickvals=list(range(len(category_totals))),
                ticktext=category_totals["Category"],
                row=row,
                col=1,
            )

            row += 1  # Move to next subplot row

        # Update layout
        fig.update_layout(title="Spending Analysis", showlegend=False, height=5000)
        fig.update_yaxes(range=[0, 2000], tickmode="linear", tick0=0, dtick=100)

        # Show the plot
        fig.show()

    def get_dates_in_between(self, start_date_str, end_date_str):
        start_month, start_year = map(int, start_date_str.split("-"))
        end_month, end_year = map(int, end_date_str.split("-"))

        start_date = datetime.date(start_year, start_month, 1)
        end_date = datetime.date(end_year, end_month, 1)

        dates_between = []
        current_date = start_date
        while current_date <= end_date:
            dates_between.append(current_date.strftime("%Y-%m"))
            if current_date.month == 12:
                current_date = datetime.date(current_date.year + 1, 1, 1)
            else:
                current_date = datetime.date(
                    current_date.year, current_date.month + 1, 1
                )

        return dates_between

    def generate_timerange_graphs(self, start, end):
        dates = self.get_dates_in_between(start, end)

        # Create a list of dataframes using list comprehension
        files = [f"spending/{date}.csv" for date in dates]
        dfs = [pd.read_csv(file) for file in files if os.path.exists(file)]

        # Concatenate all dataframes into a single dataframe
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df = combined_df.sort_values(by="Transaction Date", ascending=False)

        category_totals = combined_df.groupby("Category")["Amount"].sum().reset_index()

        # Plot the bar graph
        fig = px.bar(
            category_totals, x="Category", y="Amount", title="Spending by Category"
        )
        fig.update_layout(title="Spending Analysis", showlegend=False, height=2000)
        largest_amount = combined_df["Amount"].max() + 200
        largest_amount = (largest_amount + 50) // 100 * 100
        fig.update_yaxes(
            range=[0, largest_amount], tickmode="linear", tick0=0, dtick=10
        )
        fig.show()
