from utils import load_universe
import yfinance as yf
import os

DATA_DIR = "data/prices"

def download_price_data(tickers):
    os.makedirs(DATA_DIR, exist_ok=True)
    for ticker in tickers:
        print(f"Downloading price data for {ticker}...")
        try:
            df = yf.download(ticker, period="5y", interval="1d", progress=False)
            if not df.empty:
                df.to_csv(f"{DATA_DIR}/{ticker}.csv")
                print(f"Saved {ticker} price data.")
            else:
                print(f"No data for {ticker}")
        except Exception as e:
            print(f"Error downloading {ticker}: {e}")

if __name__ == "__main__":
    universe = load_universe()
    download_price_data(universe)
 Ingestion script placeholder
