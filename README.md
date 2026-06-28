<div align="center">

# ⚡ Algorithmic Crypto Trading Engine
**High-performance backtesting, live market data, and machine learning price forecasting.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-14354C?style=for-the-badge&logo=python&logoColor=white)](#)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](#)
[![Machine Learning](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](#)

</div>

<br>

> A full-stack quantitative finance dashboard built to test, simulate, and analyze crypto trading strategies against historical and real-time tick data.

---

### ✧ Core Features

* **Adaptive Trading Strategies:** Switch instantly between `Moving Average Crossover`, `RSI Momentum`, and `Pure AI Forecasting`.
* **Machine Learning Forecasts:** 7-day predictive modeling using rolling-window Linear Regression with intercept anchoring.
* **Precision Backtesting Engine:** Simulates real-world conditions, strictly managing portfolio states and deducting dynamic exchange fees.
* **Live Market Polling:** Toggleable 10-second auto-refresh loop for real-time `yfinance` price tracking.
* **Pro-Grade Visualization:** Custom Plotly charts with precise Buy/Sell execution markers overlaid directly on market action.

---

### ✧ System Architecture

The engine is decoupled into three modular components for maximum performance and readability:

| Module | Role | Core Tech Stack |
| :--- | :--- | :--- |
| 🖥️ `app.py` | UI, Orchestration & Live Loop | Streamlit, Plotly |
| ⚙️ `backtester.py` | State Machine & Portfolio Math | Pandas, NumPy |
| 📡 `data_engine.py` | API Fetching, Signals & ML | yfinance, scikit-learn |

---

### ✧ Quick Start

Get the engine running locally in under a minute.

**1. Clone the repository**
`git clone https://github.com/dhanyaemsky-commits/-Algorithmic-Crypto-Trading-Backtesting-Engine`
`cd -Algorithmic-Crypto-Trading-Backtesting-Engine`

**2. Install dependencies**
`pip install -r requirements.txt`

**3. Ignite the dashboard**
`streamlit run app.py`

---

### ✧ Performance Metrics Tracked

The dashboard calculates institutional-grade metrics to evaluate strategy viability:

* **ROI:** Absolute return versus initial capital.
* **Maximum Drawdown:** The largest peak-to-trough drop (stress-testing risk).
* **Sharpe Ratio:** Risk-adjusted return, annualized over a 365-day continuous crypto trading calendar.
* **Win/Loss Ratio:** Profitability percentage across all closed trade cycles.

---

<div align="center">
    
**Dhanya K** *B.Sc. Computer Science with Data Analytics |Dr. N.G.P. Arts and Science College*

</div>