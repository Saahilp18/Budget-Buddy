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
    dates = defaultdict(lambda: f'{datetime.date.today().year-1}-01-01',json.load(file))


dir = './statements'
files = os.listdir(dir)

aggregated_transactions = pd.DataFrame(columns=['Transaction Date', 'Description', 'Amount', 'Category'])

# Read all statements
for i, file in enumerate(files):
    statement_path = f'./statements/{file}'
    bank, card = file[:-4].split('-')
    transactions = pd.read_csv(statement_path)
    
    # Convert the Transaction date to datetime and format it correctly
    transactions['Transaction Date'] = pd.to_datetime(transactions['Transaction Date']).dt.strftime('%Y-%m-%d')

    # Filter out dates that have already been read
    transactions = transactions[transactions['Transaction Date'] > dates[bank]]

    transactions['Card'] = card

    # Parse the transactions
    transactions = ReaderFactory().getReader(bank).parseTransactions(transactions)

    # Allocate the data to the correct JSON file by year-month
    for date in transactions['Transaction Date'].str[:7].unique():
        filename = f'./spending/{date}.csv'
        if os.path.exists(filename):
            with open(filename, 'a') as f:
                transactions[transactions['Transaction Date'].str[:7] == date].to_csv(f, header=False, index=False)
        else:
            transactions[transactions['Transaction Date'].str[:7] == date].to_csv(filename, index=False)

    # Update the most recent date viewed
    most_recent_date = transactions['Transaction Date'].max()
    if not pd.isna(most_recent_date):
         dates[bank] = most_recent_date

    #os.remove(statement_path)


with open('dates.json', 'w') as json_file:
    json.dump(dates, json_file, indent=4)

    