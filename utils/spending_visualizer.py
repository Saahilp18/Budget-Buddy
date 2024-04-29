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
            self.budget_limits = json.load(f)
            self.budget_df = pd.DataFrame(
                list(self.budget_limits.items()), columns=["Category", "Budget"]
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

        category_totals = category_totals[(category_totals["Amount"] != 0) & (~category_totals["Amount"].isna())]

        total_spent = round(category_totals["Amount"].sum(), 2)
        category_order = [cat for cat in self.budget_limits.keys() if cat in category_totals["Category"].unique()]

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
            category_order = [cat for cat in self.budget_limits.keys() if cat in category_totals["Category"].unique()]

            category_totals_filtered = category_totals[category_totals["Category"].isin(category_order)]

            # Reorder the filtered DataFrame based on category_order
            category_totals_filtered = category_totals_filtered.set_index("Category").reindex(category_order).reset_index()

            fig.add_trace(
                go.Bar(
                    x=category_totals_filtered["Category"],
                    y=category_totals_filtered["Amount"],
                    name=timeframe,
                ),
                row=row,
                col=1,
            )

            fig.update_xaxes(
                tickvals=list(range(len(category_totals_filtered))),
                ticktext=category_totals_filtered["Category"],
                row=row,
                col=1,
            )

            row += 1  # Move to next subplot row

        fig.update_layout(title="Spending Analysis", showlegend=False)

        fig.show()