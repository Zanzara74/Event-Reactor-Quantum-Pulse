import pandas as pd
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID  # you'll create config.py

def load_universe():
    """
    Load ticker universe combining:
    - FTSE 250 from CSV
    - ETFs from CSV
    - S&P 500 live from Wikipedia
    Returns a deduplicated list of tickers.
    """
    # Load FTSE 250 tickers
    ftse250 = pd.read_csv('data/ftse_250_tickers.csv')
    tickers_ftse = ftse250['ticker'].tolist()

    # Load ETF tickers
    etfs = pd.read_csv('data/etf_tickers.csv')
    tickers_etf = etfs['ticker'].tolist()

    # Fetch S&P 500 tickers live from Wikipedia
    sp500 = (
        pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
        ["Symbol"]
        .str.replace(r"\.", "-", regex=True)
        .tolist()
    )

    # Combine and deduplicate
    universe = list(set(tickers_ftse + tickers_etf + sp500))
    return universe

def send_telegram_alert(message: str):
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
