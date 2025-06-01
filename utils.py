# utils.py

import os
import pandas as pd
import requests
import yfinance as yf

# Your existing import of Telegram credentials from config.py
# (make sure config.py defines TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID as strings)
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def fetch_ftse250_tickers():
    """
    Scrape current FTSE 250 component symbols from Wikipedia.
    Returns a list of tickers (e.g. ['ABF.L', 'ADM.L', ...]).
    """
    url = "https://en.wikipedia.org/wiki/FTSE_250_Index"
    tables = pd.read_html(url, attrs={"class": "wikitable"})
    df = tables[0]

    # Look for a column named “EPIC” or “Ticker”
    if "EPIC" in df.columns:
        tickers = df["EPIC"].astype(str)
    elif "Ticker" in df.columns:
        tickers = df["Ticker"].astype(str)
    else:
        # Fallback to first column if header has changed
        tickers = df.iloc[:, 0].astype(str)

    # Convert any dots to dashes for yfinance compatibility
    return tickers.str.replace(".", "-", regex=False).tolist()


def fetch_etf_tickers_from_github():
    """
    Download a curated ETF ticker list from a public GitHub CSV.
    Adjust raw_csv_url if you choose a different source.
    """
    raw_csv_url = "https://raw.githubusercontent.com/rcastrejon/etf_list/master/etf.csv"
    df = pd.read_csv(raw_csv_url)

    # Look for a column named “Symbol” or “Ticker”
    if "Symbol" in df.columns:
        tickers = df["Symbol"].astype(str)
    elif "Ticker" in df.columns:
        tickers = df["Ticker"].astype(str)
    else:
        tickers = df.iloc[:, 0].astype(str)

    return tickers.str.upper().tolist()


def fetch_sp500_tickers():
    """
    Scrape current S&P 500 component symbols from Wikipedia.
    Returns a list of tickers (e.g. ['AAPL', 'MSFT', ...]).
    """
    df = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    sp500 = df["Symbol"].str.replace(r"\.", "-", regex=True).tolist()
    return sp500


def load_universe():
    """
    Load a dynamic universe combining:
      - FTSE 250 from Wikipedia
      - ETFs from a GitHub-hosted CSV
      - S&P 500 from Wikipedia
    Returns a deduplicated list of tickers.
    """
    try:
        ftse250 = fetch_ftse250_tickers()
    except Exception as e:
        print(f"Warning: could not fetch FTSE 250 from Wikipedia: {e}")
        ftse250 = []

    try:
        etfs = fetch_etf_tickers_from_github()
    except Exception as e:
        print(f"Warning: could not fetch ETF list from GitHub: {e}")
        etfs = []

    try:
        sp500 = fetch_sp500_tickers()
    except Exception as e:
        print(f"Warning: could not fetch S&P 500 from Wikipedia: {e}")
        sp500 = []

    universe = list(set(ftse250 + etfs + sp500))
    return universe


def get_price_data(ticker: str) -> pd.DataFrame | None:
    """
    Download ~6 months of daily price data for `ticker` using yfinance.
    Returns a Pandas DataFrame, or None if download fails or lacks 'Close'.
    """
    try:
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        # yfinance sometimes returns an empty DataFrame if ticker is invalid
        if df is None or df.empty or "Close" not in df.columns:
            return None
        return df
    except Exception:
        return None


def send_telegram_alert(message: str):
    """
    Send a message via Telegram bot.
    Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to be set in config.py.
    If not set, it will print the message instead.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[Telegram stub] {message}")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data, timeout=10)
        if response.status_code != 200:
            print(f"Telegram API error: {response.text}")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")


def lookup_fair_value(ticker: str) -> float:
    """
    Fetch a "fair value" for a given ticker from FinancialModelingPrep (FMP).
    Expects FMP_API_KEY in environment. Returns 0.0 if lookup fails.
    """
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        return 0.0

    try:
        # Example endpoint: company profile (which includes a "price" field).
        url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={api_key}"
        response = requests.get(url, timeout=10)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            fair_value = data[0].get("price")
            return float(fair_value) if fair_value else 0.0
    except Exception:
        pass

    return 0.0


if __name__ == "__main__":
    # Quick sanity check: load a small subset of tickers and print
    universe = load_universe()
    print(f"Total tickers loaded: {len(universe)}")
    print("Sample tickers:", universe[:10])
