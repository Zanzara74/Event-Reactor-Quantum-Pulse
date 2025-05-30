# Event Reactor | Quantum Pulse

Integrated trading signal engine combining event-driven triggers (Event Reactor) with quantitative and seasonal analysis (Quantum Pulse).

## Overview

- **Event Reactor:** Monitors real-time market events such as earnings, CEO changes, layoffs, and market selloffs.
- **Quantum Pulse:** Provides quantitative signals based on seasonality, technical indicators, fundamental scores (like Piotroski), fair value, and macro sentiment.

Together, they generate robust entry and exit trading signals for stocks across multiple universes (FTSE 250, S&P 500, ETFs, etc.).

## Repository Structure

```
EventReactor-Quantum-Pulse/
│
├── data/                 # Raw and processed data files
├── models/               # Machine learning models and serialized objects
├── modules/              # Signal calculation modules (e.g. divergence_detector.py)
├── workflow/             # Scripts for data ingestion, training, and inference
├── utils.py              # Helper functions (data fetching, alerts, etc.)
├── config.py             # Configuration parameters and API keys
├── quantum_signal_engine.py  # Main signal generation engine
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Getting Started

1. Clone this repo.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure API keys and parameters in `config.py`.
4. Run the main engine:

```bash
python quantum_signal_engine.py
```

## Contribution

Contributions and improvements are welcome! Please open issues or pull requests.

---

*Generated and maintained by Alfredo Carta with AI assistance.*
