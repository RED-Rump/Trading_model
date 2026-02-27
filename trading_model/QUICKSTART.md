# Quick Reference Guide

Fast lookup for common tasks and commands.

---

## Quick Start Commands

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Run main pipeline
python main.py

# Start Jupyter
jupyter notebook

# Install new package
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt
```

---

## Common Code Snippets

### Download Data
```python
from data.collector import DataCollector

collector = DataCollector()
prices = collector.fetch_data(['SPY', 'QQQ'], '2020-01-01', '2024-12-31')
prices = collector.clean_data()
returns = collector.calculate_returns()
```

### Run a Strategy
```python
from strategies.moving_average import MovingAverageCrossover
from backtesting.engine import Backtester

# Create strategy
strategy = MovingAverageCrossover(fast=20, slow=50)

# Backtest
backtester = Backtester(initial_capital=100000)
results = backtester.run(strategy, prices['SPY'], returns['SPY'])

# Plot
backtester.plot_results()
```

### Create Custom Strategy
```python
from strategies.base import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self, param1=10):
        super().__init__(name="My Strategy")
        self.param1 = param1
    
    def generate_signals(self, data):
        # Your logic here
        signals = pd.Series(0, index=data.index)
        # ... calculate signals ...
        self.signals = signals
        return signals
```

---

## Configuration Quick Reference

Edit `config.py` to change:

```python
# Data settings
DATA_START_DATE = '2020-01-01'
DATA_END_DATE = '2024-12-31'
DEFAULT_TICKERS = ['SPY', 'QQQ', 'IWM', 'GLD', 'TLT']

# Strategy parameters
MA_FAST = 20              # Fast MA period
MA_SLOW = 50              # Slow MA period
ZSCORE_THRESHOLD = 2.0    # Mean reversion threshold
MOMENTUM_LOOKBACK = 20    # Momentum period

# Backtesting
INITIAL_CAPITAL = 100000
TRANSACTION_COST = 0.001  # 0.1% per trade

# Risk management
MAX_DRAWDOWN_LIMIT = 0.20  # 20% max drawdown
TARGET_VOLATILITY = 0.15   # 15% target vol
```

---

## File Locations

```
Important files:
├── config.py              # Settings (EDIT THIS)
├── main.py                # Main script (RUN THIS)
├── requirements.txt       # Dependencies
│
Strategies (CREATE NEW ONES HERE):
├── strategies/
│   ├── moving_average.py
│   ├── mean_reversion.py
│   └── momentum.py
│
Data (AUTO-GENERATED):
├── data/data_cache/       # Cached downloads
└── logs/
    ├── plots/             # Chart images
    └── results/           # CSV exports
```

---

## Keyboard Shortcuts

### Jupyter Notebook
- `Shift + Enter` - Run cell and move to next
- `Ctrl + Enter` - Run cell and stay
- `A` - Insert cell above
- `B` - Insert cell below
- `D D` - Delete cell
- `M` - Convert to Markdown
- `Y` - Convert to Code

### VS Code
- `Ctrl + /` - Comment/Uncomment
- `Ctrl + Shift + P` - Command palette
- `F5` - Run/Debug
- `Ctrl + ` ` - Toggle terminal

---

## Performance Metrics Explained

| Metric | What It Means | Good Value |
|--------|---------------|------------|
| **Total Return** | Overall profit/loss | > 0% |
| **CAGR** | Annualized return | > 10% |
| **Sharpe Ratio** | Risk-adjusted return | > 1.0 |
| **Max Drawdown** | Largest peak-to-trough decline | < -20% |
| **Calmar Ratio** | CAGR / Max Drawdown | > 1.0 |
| **Win Rate** | % of profitable trades | > 50% |

---

## Troubleshooting Quick Fixes

### Data download fails
```python
collector.clear_cache()  # Clear old data
collector.use_cache = False  # Force fresh download
```

### Strategy returns empty
```python
# Check if data has enough history
print(len(prices))  # Should be > lookback period
```

### Plots not appearing
```python
import matplotlib.pyplot as plt
plt.show()  # Add this after plotting
```

### Import errors
```bash
# Reinstall packages
pip install -r requirements.txt --upgrade
```

---

## Next Level: Optimization

### Grid Search Example
```python
# Test multiple parameter combinations
fast_periods = [10, 20, 30]
slow_periods = [40, 50, 60]

best_sharpe = -999
best_params = None

for fast in fast_periods:
    for slow in slow_periods:
        strategy = MovingAverageCrossover(fast, slow)
        backtester = Backtester()
        results = backtester.run(strategy, prices['SPY'], returns['SPY'])
        
        if results['metrics']['Sharpe Ratio'] > best_sharpe:
            best_sharpe = results['metrics']['Sharpe Ratio']
            best_params = (fast, slow)

print(f"Best params: Fast={best_params[0]}, Slow={best_params[1]}")
print(f"Best Sharpe: {best_sharpe:.3f}")
```

---

## Resources

- **yfinance docs**: [pypi.org/project/yfinance](https://pypi.org/project/yfinance/)
- **pandas docs**: [pandas.pydata.org](https://pandas.pydata.org/)
- **Alpaca API**: [alpaca.markets/docs](https://alpaca.markets/docs/)

---

**Keep this file handy!** Bookmark it for quick reference. 📚
