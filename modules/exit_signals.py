import ta

def compute_exit_signals(df, fair_value):
    df = df.copy()
    df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    df['ema_20'] = df['Close'].ewm(span=20).mean()
    df['macd_diff'] = ta.trend.MACD(df['Close']).macd_diff()
    latest = df.iloc[-1]
    reasons = []
    if latest['rsi'] > 70: reasons.append("RSI overbought")
    if latest['Close'] >= fair_value * 1.1: reasons.append("Near/exceeds fair value")
    if latest['macd_diff'] < 0: reasons.append("MACD bearish crossover")
    if latest['Close'] < latest['ema_20']: reasons.append("Below 20 EMA")
    return len(reasons) >= 2, reasons
