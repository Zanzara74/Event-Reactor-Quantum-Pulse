def score(df, fair_value):
    return 1 if df['Close'].iloc[-1] < fair_value * 0.9 else 0
