from modules import divergence_detector, piotroski_score, rsi_filter, seasonality_score, fair_value_check, break_even_tracker, cot_sentiment, exit_signals
from utils import load_universe
import yfinance as yf

def run_quantum_engine():
    universe = load_universe()
    print(f"Loaded {len(universe)} tickers to scan.")

    for ticker in universe:
        print(f"Processing {ticker}...")

        # Download historical price data (e.g. 3 months daily)
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False)
        except Exception as e:
            print(f"Failed to fetch data for {ticker}: {e}")
            continue
        if df.empty:
            print(f"No data for {ticker}")
            continue

        # Placeholder fair value (replace with actual lookup)
        fair_value = df['Close'][-1]  # Simple placeholder using last close price

        # Calculate signal components
        divergence_score = divergence_detector.score(df)
        piotroski_score_val = piotroski_score.score(ticker)
        rsi_score = rsi_filter.score(df)
        seasonality_score_val = seasonality_score.get(ticker)
        fair_value_score = fair_value_check.score(df, fair_value)
        break_even_score = break_even_tracker.score(ticker)
        cot_sentiment_score = cot_sentiment.score(ticker)

        print(f"Scores for {ticker}:")
        print(f"  Divergence: {divergence_score}")
        print(f"  Piotroski: {piotroski_score_val}")
        print(f"  RSI: {rsi_score}")
        print(f"  Seasonality: {seasonality_score_val}")
        print(f"  Fair Value: {fair_value_score}")
        print(f"  Break Even: {break_even_score}")
        print(f"  COT Sentiment: {cot_sentiment_score}")

        # Compute exit signals (example)
        exit_signal, reasons = exit_signals.compute_exit_signals(df, fair_value)
        if exit_signal:
            print(f"Exit signal for {ticker} due to: {', '.join(reasons)}")

        print("-" * 40)

if __name__ == '__main__':
    run_quantum_engine()
