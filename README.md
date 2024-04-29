<p align="center">
  <img src="https://github.com/Saahilp18/Budget-Buddy/assets/40773540/4533dfb4-ee08-42e5-9f85-3f44fd1a5dfc" width="300" height="300">
</p>

# Budget Buddy
A tool that will allow users to track their spending and habits by regularly uploading their credit card statements. These statements will be normalized and aggregated to provide a cumulative, month-by-month analysis of spending habits. With this project, I aim to provide a robust, no-cost solution to help users manage their finances and promote responsible spending.

# Setup
1. Install relevant Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a Google Cloud Project and a Bucket in Google Cloud Storage where your transactions will be stored.
4. Create a `secrets.json` file in your `root` directory with the following fields:
   - `project_id` - The Project ID of your Google Cloud Project, which can be found on the Dashboard.
   - `bucket` - The name of your Bucket in Google Cloud Storage.
5. Adjust the values in `budget.json` to fit your budget.

## How to use:
1. Download credit/debit card statements
2. Upload statements to the `./Statements` directory.
3. Rename statements using the naming conventions listed below in this format: **<bank>-<card_name>**
4. Run the `main.py` script from the `root` directory:
   ```bash
   python main.py
   ```
5. Follow the instructions in the CLI.

## Naming conventions of supported banks
- Capital One - **capone**
- Chase - **chase**
- Discover - **discover**
