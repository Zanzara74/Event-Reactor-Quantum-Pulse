import ta

def score(df, window=14, threshold=35):
    rsi = ta.momentum.RSIIndicator(df['Close'], window=window).rsi().iloc[-1]
    return 1 if rsi < threshold else 0
