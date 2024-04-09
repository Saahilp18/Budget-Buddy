import os
import pandas as pd
import json
from collections import defaultdict
import datetime
from readers.reader_factory import ReaderFactory

if not os.path.exists('dates.json'):
        with open('dates.json', 'w') as file:
            json.dump({}, file)

with open('dates.json', 'r') as file:
    dates = defaultdict(lambda: f'{datetime.date.today().year}-01-01',json.load(file))


dir = './statements'
files = os.listdir(dir)

aggregated_transactions = pd.DataFrame(columns=['Transaction Date', 'Description', 'Amount', 'Category'])

# Read all statements
for i, file in enumerate(files):
    statement_path = f'./statements/{file}'
    bank, card = file[:-4].split('-')
    transactions = pd.read_csv(statement_path)

    # Filter out dates that have already been read
    transactions = transactions[transactions['Transaction Date'] > dates[bank]]
    # Convert the Transaction date to datetime and format it correctly
    transactions['Transaction Date'] = pd.to_datetime(transactions['Transaction Date']).dt.strftime('%Y-%m-%d')

    # Parse the transactions
    parsed_transactions = ReaderFactory().getReader(bank).parseTransactions(transactions)


    most_recent_date = parsed_transactions['Transaction Date'].max()
    if not pd.isna(most_recent_date):
         dates[bank] = most_recent_date



    # os.remove(statement_path)

# aggregated_transactions.sort_values(by='Transaction Date', ascending=False).to_csv('transactions.csv', index=False)

with open('dates.json', 'w') as json_file:
    json.dump(dates, json_file, indent=4)

    