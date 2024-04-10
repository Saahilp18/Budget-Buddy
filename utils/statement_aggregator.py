import os
import pandas as pd
from readers.reader_factory import ReaderFactory

class StatementAggregator:
    def __init__(self):
        if not os.path.exists('spending'):
            os.makedirs('spending')
                
    def read_statements(self):

        dir = './statements'
        files = os.listdir(dir)

        # Read all statements
        for file in files:
            statement_path = f'./{dir}/{file}'
            bank, card = file[:-4].split('-')
            transactions = pd.read_csv(statement_path)

            # Convert the Transaction date to datetime and format it correctly
            transactions['Transaction Date'] = pd.to_datetime(transactions['Transaction Date']).dt.strftime('%Y-%m-%d')

            transactions['Card'] = card

            # Filter out dates that have already been read
            unique_dates = pd.to_datetime(transactions['Transaction Date']).dt.strftime('%Y-%m').unique()
            dfs = [pd.read_csv(f'spending/{date}.csv') for date in unique_dates if os.path.exists(f'spending/{date}.csv')]
            

            # Parse the transactions
            transactions = ReaderFactory().getReader(bank).parseTransactions(transactions)

            if dfs:
                combined_dfs = pd.concat(dfs, ignore_index=True)
                # Merge transactions and combined_dfs on all columns
                merged = pd.merge(transactions, combined_dfs, how='left', indicator=True)

                # Filter out rows present in both DataFrames
                transactions = merged[merged['_merge'] == 'left_only'].copy()

                # Drop the '_merge' column as it's no longer needed
                transactions.drop(columns='_merge', inplace=True)

            # Allocate the data to the correct JSON file by year-month
            for date in transactions['Transaction Date'].str[:7].unique():
                filename = f'./spending/{date}.csv'
                if os.path.exists(filename):
                    with open(filename, 'a') as f:
                        transactions[transactions['Transaction Date'].str[:7] == date].to_csv(f, header=False, index=False)
                else:
                    transactions[transactions['Transaction Date'].str[:7] == date].to_csv(filename, index=False)

            os.remove(statement_path)

