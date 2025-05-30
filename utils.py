import pandas as pd

def load_universe():
    # Load FTSE 250 tickers from CSV
    ftse250 = pd.read_csv('data/ftse250.csv')
    tickers_ftse = ftse250['Ticker'].tolist()

    # Load ETF tickers from CSV
    etfs = pd.read_csv('data/etf_list.csv')
    tickers_etf = etfs['Ticker'].tolist()

    # Fetch live S&P 500 tickers from Wikipedia
    sp500 = (
        pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
        ["Symbol"]
        .str.replace(r"\.", "-", regex=True)
        .tolist()
    )

    # Combine all tickers into one list and remove duplicates
    universe = list(set(tickers_ftse + tickers_etf + sp500))

    return universe
# Utility functions placeholder
