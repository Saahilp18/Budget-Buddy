import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import io


class SpendingVisualizer:
    """This class will be used to display a users spending habits based on their data stored in Google Cloud Storage"""

    def __init__(self, storage_client):
        self.storage_client = storage_client

        # Create mappings of the number representation of a month to its actual value
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

        # Read the budget values
        with open("budget.json", "r") as f:
            self.budget_limits = json.load(f)
            self.budget_df = pd.DataFrame(
                list(self.budget_limits.items()), columns=["Category", "Budget"]
            )

    def generate_graph(self, time):
        """
        This function will be used to generate a graph of the spending habits for a particular month

        time (String): The specific month and year that we want to visualize
        """
        file = f"{time}.csv"
        blob = self.storage_client.get_blob(file)
        if not blob.exists():
            print("There are no statements for this time period.")
            return

        # Read transactions from Google Cloud Storage
        transactions = pd.read_csv(io.BytesIO(blob.download_as_string()))

        # Calculate the totals per category
        category_totals = transactions.groupby("Category")["Amount"].sum().reset_index()
        category_totals = pd.merge(
            category_totals, self.budget_df, on="Category", how="left"
        )
        category_totals["Formatted Amount"] = "$" + category_totals["Amount"].round(
            2
        ).astype(str)

        # Drop rows with NaN or 0 as the amount
        category_totals = category_totals[
            (category_totals["Amount"] != 0) & (~category_totals["Amount"].isna())
        ]

        # Calculate the total spent across all categories
        total_spent = round(category_totals["Amount"].sum(), 2)

        # Set the order  of the bars in the bar chart based on the order in budget.json
        category_order = [
            cat
            for cat in self.budget_limits.keys()
            if cat in category_totals["Category"].unique()
        ]

        # Plot the bar graph
        fig = px.bar(
            category_totals,
            x="Category",
            y="Amount",
            title=f"Total Amount Spent For This Month: ${total_spent}",
            color=category_totals.apply(
                lambda row: (
                    "red"
                    if row["Amount"] > row["Budget"]
                    else ("yellow" if row["Amount"] > 0.75 * row["Budget"] else "green")
                ),
                axis=1,
            ),
            color_discrete_map={
                "green": "rgba(0, 255, 0, 0.5)",  # Green if less than 3/4 of the budget has been spent
                "red": "rgba(255, 0, 0, 0.5)",  # Red if you are over budget
                "yellow": "rgba(255, 255, 0, 0.5)",  # Yellow if you are nearing close to the budget
            },
            text="Formatted Amount",
            category_orders={"Category": category_order},
        )

        # Have text values on the plot on top of the bar
        fig.update_traces(textposition="outside")

        # Hide the legend
        fig.update_layout(showlegend=False)

        # Show the plot
        fig.show()

    def get_plot_name(self, file):
        year, month = file[:7].split("-")
        return f"{self.months[month]} {year}"

    def generate_graphs(self):
        """
        This function will display the spending for all the months that the user has data for
        """

        # Retrieve all the data in the respective GCS Bucket
        blobs = self.storage_client.list_blobs()
        # Sort the blobs to show them in chronological order
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

            # If there is no data, then stop
            if not blob.exists():
                print("There are no statements for this time period.")
                return

            # Read statement from GCS bucket
            transactions = pd.read_csv(io.BytesIO(blob.download_as_string()))

            #  Calculate the total spending per category
            category_totals = (
                transactions.groupby("Category")["Amount"].sum().reset_index()
            )

            # Hide columns with no spending
            category_totals = category_totals[category_totals["Amount"] > 0]

            # Set the order of the bars in the bar chart based on the order in budget.json
            category_order = [
                cat
                for cat in self.budget_limits.keys()
                if cat in category_totals["Category"].unique()
            ]

            # Drop rows with NaN or 0 as the amount
            category_totals_filtered = category_totals[
                category_totals["Category"].isin(category_order)
            ]

            # Reorder the filtered DataFrame based on category_order
            category_totals_filtered = (
                category_totals_filtered.set_index("Category")
                .reindex(category_order)
                .reset_index()
            )

            # Add the subplot to the plot
            fig.add_trace(
                go.Bar(
                    x=category_totals_filtered["Category"],
                    y=category_totals_filtered["Amount"],
                    name=timeframe,
                ),
                row=row,
                col=1,
            )

            # Update the x-axis values
            fig.update_xaxes(
                tickvals=list(range(len(category_totals_filtered))),
                ticktext=category_totals_filtered["Category"],
                row=row,
                col=1,
            )

            row += 1  # Move to next subplot row

        # Set the plot title and hide the legend
        fig.update_layout(title="Spending Analysis", showlegend=False)

        # Show the plots
        fig.show()
