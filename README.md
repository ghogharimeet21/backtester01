# Indian Stock Market Strategy Backtester

A modular and extensible **Python + Flask based backtesting framework** designed specifically for the **Indian stock market**.
This project enables traders, researchers, and developers to **test algorithmic trading strategies on historical data before going live**.
It supports custom strategies, dynamic data access, and API-driven execution — making it suitable for experimentation, learning, and real-world system prototyping.

---

## 🚀 Key Features

- **Backtest Any Strategy:** Test ideas before real execution.
- **API Driven:** Each strategy can be exposed via a POST request for configuration-based testing.
- **Modular Architecture:** Easily plug in new strategies, indicators, and workflows.
- **Fast Data Access:** Historical candle data is loaded into memory at server start for quick access.
- **Object-Oriented Candle Model:** Each price candle is represented as a class instance with OHLCV attributes and metadata.
- **Customizable and Scalable:** Add new segments, instruments, data sources, or storage logic.

---

## 🧠 How It Works

1. The server loads historical market data into memory on startup.
2. Candles are stored in a structured format:
   - By **instrument** (e.g., NIFTY, BANKNIFTY, stock)
   - By **segment/timeframe** (1m, 5m, 15m, etc.)
3. Each candle becomes an **object instance**, enabling clean data handling and easier strategy logic.
4. Strategies are defined as Python modules and exposed via Flask routes.
5. Users send a POST request with parameters; the system executes the strategy and returns backtest results.

---

## 📂 Project Structure Overview

```
backtester/
│
├── strategies_container/      # Custom strategies live here
├── data_storage/             # Historical candle data (segmented/instrument-wise)
├── utils/                    # Indicators and helper utilities
├── start.py                  # Main entry point (server initializer)
├── test.py                   # For internal testing and debugging
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```
git clone https://github.com/ghogharimeet21/backtester01.git
cd backtester01
pip install -r requirements.txt
```

(Optional but recommended):

```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

---

## ▶️ Run the Server

```
python start.py
```

Server will run on:

```
http://localhost:5000
```

---

## 📡 Example API Request

**Endpoint (example):**

```
POST /api/backtest/strategy_name
```

**Sample JSON Payload:**

```json
{
  "instrument": "BANKNIFTY",
  "segment": "5m",
  "strategy_parameters": {
    "fast_ema": 9,
    "slow_ema": 21
  }
}
```

**Response Example:**

```json
{
  "status": "success",
  "total_trades": 42,
  "win_rate": "57.14%",
  "profit_loss": "+12.4%",
  "logs": []
}
```

---

## 🧩 Adding a New Strategy

Create a new file under `strategies_container`:

```python
class Strategy:
    def __init__(self, params):
        self.params = params

    def evaluate(self, candles):
        # Write custom logic here
        return "BUY" or "SELL" or None
```

Register it inside Flask routing and accept input via request body:

```python
from flask import Blueprint, request, jsonify
from strategies_container.my_strategy import Strategy

bp = Blueprint("strategy_api", __name__)

@bp.route("/api/backtest/my_strategy", methods=["POST"])
def run_strategy():
    body = request.get_json()
    params = body.get("strategy_parameters")
    instrument = body.get("instrument")
    segment = body.get("segment")

    strategy = Strategy(params)
    # fetch candles from memory (pseudo example)
    candles = get_candles(instrument, segment)

    result = strategy.evaluate(candles)
    return jsonify({"status": "completed", "result": result})
```

---

## 🔮 Future Enhancements

- Strategy performance visualization (charts, drawdown plot, win/loss curve)
- Web UI dashboard
- Live paper trading mode
- Additional technical indicators
- Broker API integration (AngelOne, Fyers, Zerodha — optional future)

---

## 👨‍💻 Author

**Meet Ghoghari**
📌 GitHub: https://github.com/ghogharimeet21
📌 LinkedIn: https://linkedin.com/in/meet-ghoghari-1a2054291

---

## 📄 License

This project currently has no formal license.
You may add one based on how you want others to use this software (MIT recommended).

---

⭐ If this project helps you, consider giving it a star!
