# 📈 Quantitative Trading Model

A professional Python-based backtesting platform for developing and testing systematic trading strategies. Features a beautiful GUI, multiple built-in strategies, and comprehensive performance analytics.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🌟 Features

- **📊 Multiple Trading Strategies**
  - Moving Average Crossover
  - Mean Reversion (Z-Score)
  - Momentum Strategy
  
- **🖥️ Graphical User Interface**
  - Click-and-select interface
  - Real-time logging
  - Embedded charts
  - One-click CSV export

- **📈 Comprehensive Analytics**
  - Sharpe Ratio
  - Maximum Drawdown
  - Win Rate & Win/Loss Ratio
  - CAGR (Compound Annual Growth Rate)
  - Calmar Ratio

- **🔄 Unified Trading System**
  - Backtest strategies on stocks/indices
  - Validate performance metrics
  - Deploy to IC Markets forex trading
  - Live trading integration with MT5
  - Automated risk management

- **⚡ Smart Features**
  - Data caching for faster backtests
  - Configurable parameters
  - Transaction cost modeling
  - Multiple asset support

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/RED-Rump/Trading_model.git
cd Trading_model
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r trading_model/requirements.txt
```

### Usage

#### Option 1: GUI Application (Recommended)
```bash
cd trading_model
python gui_app.py
```

#### Option 2: Command Line
```bash
cd trading_model
python main.py
```

#### Option 3: Unified Trading System (Backtest → Validate → Deploy)
```bash
python unified_trading_system.py
```
This runs a complete workflow:
- Backtests strategy on historical stock data
- Validates profitability metrics
- Connects to IC Markets MT5
- Tests deployment (simulation)
- Ready for live forex trading

#### Option 4: Jupyter Notebook
```bash
jupyter notebook
# Open trading_model/notebooks/01_getting_started.ipynb
```

## 📁 Project Structure

```
trading_model/
├── data/                       # Data collection & management
│   └── collector.py
├── strategies/                 # Trading strategy implementations
│   ├── base.py                # Base strategy class
│   ├── moving_average.py      # MA crossover strategy
│   ├── mean_reversion.py      # Mean reversion strategy
│   └── momentum.py            # Momentum strategy
├── backtesting/               # Backtesting engine
│   └── engine.py
├── notebooks/                 # Jupyter notebooks
│   └── 01_getting_started.ipynb
├── logs/                      # Results & plots (auto-generated)
├── config.py                  # Configuration settings
├── main.py                    # CLI application
├── gui_app.py                 # GUI application
├── unified_trading_system.py  # Unified backtest → validate → deploy system
└── requirements.txt           # Python dependencies
```

## 🎯 Example Usage

### Running a Backtest via CLI

```python
from data.collector import DataCollector
from strategies.moving_average import MovingAverageCrossover
from backtesting.engine import Backtester

# Download data
collector = DataCollector()
prices = collector.fetch_data(['SPY'], '2020-01-01', '2024-12-31')
prices = collector.clean_data()
returns = collector.calculate_returns()

# Create strategy
strategy = MovingAverageCrossover(fast=20, slow=50)

# Run backtest
backtester = Backtester(initial_capital=100000)
results = backtester.run(strategy, prices['SPY'], returns['SPY'])

# View results
backtester.plot_results()
```

## 🔄 Unified Trading System

The unified trading system connects your backtesting model with IC Markets live trading:

```python
from unified_trading_system import UnifiedTradingSystem

# Create system
system = UnifiedTradingSystem(mode="BOTH")

# Run complete workflow
system.run_unified_workflow(
    strategy_name='moving_average',
    backtest_symbol='SPY',
    forex_symbol='EURUSD'
)
```

### Workflow Steps
1. **Backtest**: Test strategy on historical stock/index data
2. **Validate**: Check Sharpe ratio, returns, and drawdown metrics
3. **Connect**: Establish connection to IC Markets MT5
4. **Test Deploy**: Simulate deployment without real trades
5. **Deploy Live**: Execute real trades on forex markets (if desired)

### Key Methods
- `backtest_strategy()` - Backtest your strategy
- `is_strategy_profitable()` - Check profitability criteria
- `connect_to_forex()` - Connect to IC Markets
- `deploy_to_live()` - Deploy strategy to forex trading

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Data settings
DATA_START_DATE = '2020-01-01'
DATA_END_DATE = '2024-12-31'
DEFAULT_TICKERS = ['SPY', 'QQQ', 'IWM', 'GLD', 'TLT']

# Strategy parameters
MA_FAST = 20
MA_SLOW = 50
ZSCORE_THRESHOLD = 2.0

# Backtesting
INITIAL_CAPITAL = 100000
TRANSACTION_COST = 0.001  # 0.1% per trade
```

## 📊 Sample Results

### Moving Average Crossover on SPY (2020-2024)

```
Total Return................ 15.64%
CAGR........................ 3.12%
Sharpe Ratio................ 0.745
Max Drawdown................ -35.42%
Win Rate.................... 48.23%
```

## 🛠️ Creating Custom Strategies

Extend the `BaseStrategy` class:

```python
from strategies.base import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self, param1=10):
        super().__init__(name="My Strategy")
        self.param1 = param1
    
    def generate_signals(self, data):
        # Your logic here
        signals = pd.Series(0, index=data.index)
        # Calculate signals...
        return signals
```

## 📈 Performance Metrics Explained

| Metric | Description | Good Value |
|--------|-------------|------------|
| **CAGR** | Annualized return | > 10% |
| **Sharpe Ratio** | Risk-adjusted return | > 1.0 |
| **Max Drawdown** | Largest peak-to-trough decline | < -20% |
| **Calmar Ratio** | CAGR / Max Drawdown | > 1.0 |
| **Win Rate** | Percentage of profitable trades | > 50% |

## 🔄 Roadmap

- [ ] Add more strategies (Pairs Trading, Statistical Arbitrage)
- [ ] Machine learning strategy templates
- [ ] Live trading integration (Alpaca API)
- [ ] Portfolio optimization tools
- [ ] Walk-forward analysis
- [ ] Monte Carlo simulation
- [ ] Web-based dashboard

## ⚠️ Disclaimer

**This software is for educational and research purposes only.** 

- Past performance does not guarantee future results
- Always test strategies thoroughly before live trading
- Start with paper trading before using real capital
- Trading involves risk of loss
- The authors are not responsible for any financial losses

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

RED-Rump - [@RED_Rump](https://github.com/RED-Rump)

Project Link: [https://github.com/RED-Rump/Trading_model](https://github.com/RED-Rump/Trading_model)

## 🙏 Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) - Free market data
- [pandas](https://pandas.pydata.org/) - Data manipulation
- [matplotlib](https://matplotlib.org/) - Visualization
- [backtrader](https://www.backtrader.com/) - Backtesting framework inspiration

---

**⭐ If you find this project useful, please consider giving it a star!**
