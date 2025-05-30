from modules import (
    divergence_detector,
    piotroski_score,
    rsi_filter,
    seasonality_score,
    fair_value_check,
    break_even_tracker,
    cot_sentiment,
    exit_signals
)
from utils import load_universe, send_telegram_alert
import yfinance as yf

def run_quantum_engine():
    universe = load_universe()
    print(f"Loaded {len(universe)} tickers to scan.")

    for ticker in universe:
        print(f"Processing {ticker}...")

        # Download historical price data (e.g., 3 months daily)
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False)
        except Exception as e:
            print(f"Failed to fetch data for {ticker}: {e}")
            continue
        if df.empty:
            print(f"No data for {ticker}")
            continue

        # Placeholder fair value (replace with actual lookup)
        fair_value = df['Close'].iloc[-1]  # Last close price

        # Calculate signal components
        scores = {
            'divergence': divergence_detector.score(df),
            'piotroski': piotroski_score.score(ticker),
            'rsi': rsi_filter.score(df),
            'seasonality': seasonality_score.get(ticker),
            'fair_value': fair_value_check.score(df, fair_value),
            'break_even': break_even_tracker.score(ticker),
            'cot_sentiment': cot_sentiment.score(ticker),
        }

        print(f"Scores for {ticker}:")
        for key, val in scores.items():
            print(f"  {key}: {val}")

        # Simple composite score: sum all component scores (adjust weights if needed)
        composite_score = sum(scores.values())
        print(f"Composite score: {composite_score}")

        # Define buy signal threshold
        BUY_THRESHOLD = 4.0  # adjust as needed
        buy_signal = composite_score >= BUY_THRESHOLD

        # Compute exit signals
        exit_signal, reasons = exit_signals.compute_exit_signals(df, fair_value)

        # Send alerts
        if buy_signal:
            message = (
                f"🔷 [Quantum Pulse]\n"
                f"📈 BUY signal for {ticker}\n"
                f"Composite Score: {composite_score:.2f}\n"
                f"Components: " + ", ".join(f"{k}={v}" for k, v in scores.items())
            )
            send_telegram_alert(message)
            print(f"Sent BUY alert for {ticker}")

        if exit_signal:
            message = (
                f"🔷 [Quantum Pulse]\n"
                f"⚠️ EXIT signal for {ticker}\n"
                f"Reasons: {', '.join(reasons)}"
            )
            send_telegram_alert(message)
            print(f"Sent EXIT alert for {ticker}")

        print("-" * 40)

if __name__ == '__main__':
    run_quantum_engine()
