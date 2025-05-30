def score(df, fair_value):
    """
    Returns 1 if latest close price is less than 90% of fair value.
    """
    return 1 if df['Close'].iloc[-1] < fair_value * 0.9 else 0
