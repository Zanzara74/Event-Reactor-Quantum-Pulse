import ta

def score(df, window=14, threshold=35):
    """
    Returns 1 if RSI < threshold (oversold), else 0.
    """
    rsi = ta.momentum.RSIIndicator(df['Close'], window=window).rsi().iloc[-1]
    return 1 if rsi < threshold else 0
