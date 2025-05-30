import pandas as pd
import ta

def score(df, window=14, lookback=20):
    """
    Detect bullish or bearish RSI divergence in the given price DataFrame.
    Returns:
      1 if bullish divergence found,
      -1 if bearish divergence found,
      0 if no divergence.
    """
    df = df.copy()
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=window).rsi()

    recent = df.iloc[-lookback:]

    # Find local minima and maxima for price and RSI
    price_min_idx = recent['Close'].idxmin()
    price_max_idx = recent['Close'].idxmax()
    rsi_min_idx = recent['RSI'].idxmin()
    rsi_max_idx = recent['RSI'].idxmax()

    price_min = recent.loc[price_min_idx, 'Close']
    price_max = recent.loc[price_max_idx, 'Close']
    rsi_min = recent.loc[rsi_min_idx, 'RSI']
    rsi_max = recent.loc[rsi_max_idx, 'RSI']

    # Check bullish divergence: price makes lower low, RSI makes higher low
    prev_min_idx = recent.index.get_loc(price_min_idx) - 1
    if prev_min_idx >= 0:
        prev_price_min = recent.iloc[prev_min_idx]['Close']
        prev_rsi_min = recent.iloc[prev_min_idx]['RSI']
        if price_min < prev_price_min and rsi_min > prev_rsi_min:
            return 1

    # Check bearish divergence: price makes higher high, RSI makes lower high
    prev_max_idx = recent.index.get_loc(price_max_idx) - 1
    if prev_max_idx >= 0:
        prev_price_max = recent.iloc[prev_max_idx]['Close']
        prev_rsi_max = recent.iloc[prev_max_idx]['RSI']
        if price_max > prev_price_max and rsi_max < prev_rsi_max:
            return -1

    return 0
