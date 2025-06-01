import pandas as pd
import requests
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

def send_telegram_alert(message: str):
    """
    Send a message via Telegram bot. Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
    to be set in environment (via config.py).
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not set!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"Telegram API error: {response.text}")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

if __name__ == '__main__':
    universe = load_universe()
    print(f"Total tickers loaded: {len(universe)}")
    print("Sample tickers:", universe[:10])
