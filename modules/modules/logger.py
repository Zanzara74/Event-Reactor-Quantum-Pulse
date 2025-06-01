# modules/logger.py

import csv
from datetime import datetime

def log_signal(ticker, score, components, path='data/quantum_daily_log.csv'):
    """
    Append one line to the running CSV log (date, ticker, normalized score,
    each raw component value, plus a summary of which components were “positive”).
    """
    # Ensure the CSV file’s folder exists before writing; if you don’t already
    # have a "data/" directory in your repo, create it or update `path` as needed.
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d'),
            ticker,
            round(score, 2),
            # Round each raw component to two decimal places
            *[round(v, 2) for v in components.values()],
            # Build a “Triggers” string: join the names of all keys whose value > 0
            ' + '.join([k for k, v in components.items() if v > 0])
        ])
