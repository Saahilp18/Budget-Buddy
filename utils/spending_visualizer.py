import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import io


class SpendingVisualizer:
    def __init__(self, storage_client):
        self.storage_client = storage_client

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
        blob = self.storage_client.get_blob(file)
        if not blob.exists():
            print("There are no statements for this time period.")
            return

        transactions = pd.read_csv(io.BytesIO(blob.download_as_string()))
        category_totals = transactions.groupby("Category")["Amount"].sum().reset_index()
        category_totals = pd.merge(
            category_totals, self.budget_df, on="Category", how="left"
        )
        category_totals["Formatted Amount"] = "$" + category_totals["Amount"].round(
            2
        ).astype(str)

        # Create figure
        total_spent = round(category_totals["Amount"].sum(), 2)
        category_order = [
            "Eating Out",
            "Random Purchases",
            "Groceries",
            "Personal Health",
            "Subscriptions",
            "Rent/Utilities",
            "Investments",
            "Savings",
            "401k",
        ]
        fig = px.bar(
            category_totals,
            x="Category",
            y="Amount",
            title=f"Total Amount Spent For This Month: ${total_spent}",
            color=category_totals["Amount"] < category_totals["Budget"] + 1,
            color_discrete_map={
                True: "rgba(0, 255, 0, 0.5)",
                False: "rgba(255, 0, 0, 0.5)",
            },
            text="Formatted Amount",
            category_orders={"Category": category_order},
        )

        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)

        # Show figure
        fig.show()

    def get_plot_name(self, file):
        year, month = file[:7].split("-")
        return f"{self.months[month]} {year}"

    def generate_graphs(self):
        blobs = self.storage_client.list_blobs()
        blobs.sort(key=lambda blob: blob.name, reverse=True)

        # Create a subplot for all graphs
        fig = make_subplots(
            rows=len(blobs),
            cols=1,
            subplot_titles=[self.get_plot_name(blob.name) for blob in blobs],
        )

        row = 1  # Initialize subplot row

        # Read all statements
        for blob in blobs:
            year, month = blob.name[:7].split("-")
            timeframe = f"{self.months[month]} {year}"
            if not blob.exists():
                print("There are no statements for this time period.")
                return

            transactions = pd.read_csv(io.BytesIO(blob.download_as_string()))
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
