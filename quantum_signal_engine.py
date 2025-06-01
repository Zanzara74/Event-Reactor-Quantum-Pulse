import pandas as pd
from datetime import datetime
from quantum_pulse.signals import (
    seasonality_score,
    rsi_filter,
    divergence_detector,
    fair_value_check,
    break_even_tracker,
    piotroski_score,
    cot_sentiment,
    exit_signals
)
from quantum_pulse import score_weights, logger
from utils import load_universe, get_price_data, send_telegram_alert, lookup_fair_value

def run_quantum_engine():
    universe = load_universe()
    scored_signals = []
    exit_alerts = []

    for ticker in universe:
        df = get_price_data(ticker)
        if df is None or df.empty:
            continue

        fair_value = lookup_fair_value(ticker)

        # Compute each component; now piotroski_score.score(ticker) uses real fundamentals
        components = {
            'seasonality': seasonality_score.get(ticker),
            'rsi': rsi_filter.score(df),
            'divergence': divergence_detector.score(df),
            'fair_value': fair_value_check.score(df, fair_value),
            'break_even': break_even_tracker.score(ticker),
            'piotroski': piotroski_score.score(ticker),
            'cot': cot_sentiment.score(ticker)
        }

        # Weighted sum ⇒ normalized 0–10
        score = sum(score_weights.WEIGHTS[k] * components[k] for k in components)
        max_score = sum(score_weights.WEIGHTS.values())
        normalized_score = round((score / max_score) * 10, 2)

        # Log the raw components + normalized score
        logger.log_signal(ticker, normalized_score, components)

        if normalized_score >= 8:
            scored_signals.append((ticker, normalized_score, components))

        # Exit logic unchanged
        exit_signal, reasons = exit_signals.compute_exit_signals(df, fair_value)
        if exit_signal:
            exit_alerts.append((ticker, reasons))

    # Pick top 3 buy signals
    top_signals = sorted(scored_signals, key=lambda x: x[1], reverse=True)[:3]
    for ticker, score_val, components in top_signals:
        summary = ' + '.join([k for k, v in components.items() if v > 0])
        send_telegram_alert(f"🔷 [Quantum Pulse]\n📈 BUY {ticker} | Score: {score_val}/10\nTriggers: {summary}")

    # Fire any exit alerts
    for ticker, reasons in exit_alerts:
        send_telegram_alert(f"🔷 [Quantum Pulse]\n⚠️ EXIT {ticker} | Reasons: {', '.join(reasons)}")


if __name__ == '__main__':
    run_quantum_engine()
