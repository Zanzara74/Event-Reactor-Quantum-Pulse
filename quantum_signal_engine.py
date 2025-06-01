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

    failed_downloads = []  # will hold tickers that returned no data
    total_checked = 0
    buy_signals = []
    exit_signals_list = []

    for ticker in universe:
        total_checked += 1
        # Attempt to fetch 3 months of daily data
        try:
            df = yf.download(ticker, period="3mo", interval="1d", progress=False)
        except Exception as e:
            failed_downloads.append((ticker, f"download error: {e}"))
            continue

        if df is None or df.empty:
            failed_downloads.append((ticker, "no data for 3mo"))
            continue

        # If we reach this point, we have a non‐empty DataFrame
        fair_value = df['Close'].iloc[-1]  # placeholder for actual fair‐value logic

        # Gather all component scores
        scores = {
            'divergence': divergence_detector.score(df),
            'piotroski': piotroski_score.score(ticker),
            'rsi': rsi_filter.score(df),
            'seasonality': seasonality_score.get(ticker),
            'fair_value': fair_value_check.score(df, fair_value),
            'break_even': break_even_tracker.score(ticker),
            'cot_sentiment': cot_sentiment.score(ticker),
        }

        composite_score = sum(scores.values())

        BUY_THRESHOLD = 4.0
        if composite_score >= BUY_THRESHOLD:
            # queue up a buy‐alert; we’ll send all buy alerts after the loop
            buy_signals.append((ticker, composite_score, scores))

        # Check exit conditions
        exit_flag, reasons = exit_signals.compute_exit_signals(df, fair_value)
        if exit_flag:
            exit_signals_list.append((ticker, reasons))

    # 1) Print summary of how many tickers failed download
    print(f"\nFinished scanning {total_checked} tickers.")
    print(f"{len(failed_downloads)} tickers returned no data:")
    if len(failed_downloads) <= 20:
        # If the number is small, show which ones
        for t, reason in failed_downloads:
            print(f"  - {t}: {reason}")
    else:
        # Otherwise, just show the first 10 and say “and X more”
        print("  (Showing first 10 missing tickers)")
        for t, reason in failed_downloads[:10]:
            print(f"  - {t}: {reason}")
        print(f"  ... and {len(failed_downloads) - 10} more")

    # 2) Send BUY alerts (if any)
    for ticker, comp_score, comp_scores in buy_signals:
        summary = ", ".join(f"{k}={v}" for k, v in comp_scores.items())
        message = (
            f"🔷 [Quantum Pulse]\n"
            f"📈 BUY {ticker}\n"
            f"Composite Score: {comp_score:.2f}\n"
            f"Components: {summary}"
        )
        send_telegram_alert(message)
        print(f"Sent BUY alert for {ticker}")

    # 3) Send EXIT alerts (if any)
    for ticker, reasons in exit_signals_list:
        message = (
            f"🔷 [Quantum Pulse]\n"
            f"⚠️ EXIT {ticker}\n"
            f"Reasons: {', '.join(reasons)}"
        )
        send_telegram_alert(message)
        print(f"Sent EXIT alert for {ticker}")

    print("\nDone.")

if __name__ == "__main__":
    run_quantum_engine()
