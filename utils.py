import pandas as pd
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def load_universe():
    ftse250 = pd.read_csv('data/ftse_250_tickers.csv')
    tickers_ftse = ftse250['ticker'].tolist()

    etfs = pd.read_csv('data/etf_tickers.csv')
    tickers_etf = etfs['ticker'].tolist()

    sp500 = (
        pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
        ["Symbol"]
        .str.replace(r"\.", "-", regex=True)
        .tolist()
    )

    universe = list(set(tickers_ftse + tickers_etf + sp500))
    return universe

def send_telegram_alert(message: str):
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
