# workflow/fmp_bulk_fetch.py

import requests
import os
import pandas as pd
from config import FMP_API_KEY

BASE_URL = "https://financialmodelingprep.com/api/v3"

def fetch_and_save_financials(ticker):
    endpoints = {
        "income_statement": f"/income-statement/{ticker}?limit=120&apikey={FMP_API_KEY}",
        "balance_sheet": f"/balance-sheet-statement/{ticker}?limit=120&apikey={FMP_API_KEY}",
        "cash_flow": f"/cash-flow-statement/{ticker}?limit=120&apikey={FMP_API_KEY}",
    }
 
    ticker_dir = os.path.join(DATA_DIR, ticker)
    os.makedirs(ticker_dir, exist_ok=True)

    for report_type, endpoint in endpoints.items():
        url = BASE_URL + endpoint
        print(f"Fetching {report_type} for {ticker}...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if not data:
                print(f"No {report_type} data for {ticker}")
                continue

            df = pd.DataFrame(data)
            csv_path = os.path.join(ticker_dir, f"{report_type}.csv")
            df.to_csv(csv_path, index=False)
            print(f"Saved {report_type} for {ticker} to {csv_path}")
            sleep(1)  # Rate limit friendly

        except Exception as e:
            print(f"Failed to fetch {report_type} for {ticker}: {e}")

def bulk_fetch(tickers):
    for ticker in tickers:
        print(f"=== Processing ticker: {ticker} ===")
        fetch_and_save_financials(ticker)

if __name__ == "__main__":
    # Replace with your full universe of tickers or load from CSV
    tickers = ['AAPL', 'MSFT', 'GOOGL']  # Example tickers
    bulk_fetch(tickers)
