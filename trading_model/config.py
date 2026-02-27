"""
Configuration file for trading model
Centralized settings for easy customization
"""

from datetime import datetime, timedelta

# ==================== DATA SETTINGS ====================
DATA_START_DATE = '2020-01-01'
DATA_END_DATE = '2024-12-31'

# Default ticker universe
DEFAULT_TICKERS = [
    'SPY',   # S&P 500 ETF
    'QQQ',   # Nasdaq 100 ETF
    'IWM',   # Russell 2000 ETF
    'GLD',   # Gold ETF
    'TLT',   # 20+ Year Treasury Bond ETF
]

# Data caching
CACHE_DIR = 'data/data_cache'
USE_CACHE = True  # Set to False to always download fresh data

# ==================== STRATEGY SETTINGS ====================

# Moving Average Strategy
MA_FAST = 20
MA_SLOW = 50

# Mean Reversion Strategy
ZSCORE_WINDOW = 20
ZSCORE_THRESHOLD = 2.0

# Momentum Strategy
MOMENTUM_LOOKBACK = 20

# RSI Strategy
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

# ==================== BACKTESTING SETTINGS ====================

# Initial capital
INITIAL_CAPITAL = 100000

# Transaction costs
TRANSACTION_COST = 0.001  # 0.1% per trade (includes commission + slippage)
SLIPPAGE = 0.0005         # 0.05% slippage

# Execution
REBALANCE_FREQUENCY = 'daily'  # Options: 'daily', 'weekly', 'monthly'

# ==================== RISK MANAGEMENT ====================

# Position sizing
MAX_POSITION_SIZE = 1.0      # Maximum 100% in single asset
MIN_POSITION_SIZE = 0.0      # Minimum 0%
TARGET_VOLATILITY = 0.15     # Target 15% annual volatility

# Risk limits
MAX_DRAWDOWN_LIMIT = 0.20    # Stop trading if DD exceeds 20%
VAR_CONFIDENCE = 0.95        # 95% confidence for VaR
KELLY_FRACTION = 0.5         # Use 50% of full Kelly (fractional Kelly)

# ==================== PORTFOLIO SETTINGS ====================

# Optimization method
# Options: 'equal_weight', 'min_variance', 'max_sharpe', 'risk_parity'
DEFAULT_ALLOCATION_METHOD = 'max_sharpe'

# Constraints
ALLOW_SHORT = False          # No short selling
MAX_WEIGHT_PER_ASSET = 0.40  # Max 40% in any single asset
MIN_WEIGHT_PER_ASSET = 0.05  # Min 5% in any asset (if allocated)

# ==================== OUTPUT SETTINGS ====================

# Logging
LOG_LEVEL = 'INFO'  # Options: 'DEBUG', 'INFO', 'WARNING', 'ERROR'
LOG_FILE = 'logs/trading.log'

# Results storage
RESULTS_DIR = 'logs/results'
SAVE_PLOTS = True
PLOT_DIR = 'logs/plots'

# ==================== API SETTINGS (for live trading) ====================

# Alpaca API (leave empty for backtesting only)
ALPACA_API_KEY = ''
ALPACA_SECRET_KEY = ''
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading

# ==================== ADVANCED SETTINGS ====================

# Performance calculation
RISK_FREE_RATE = 0.02  # 2% annual risk-free rate
TRADING_DAYS_PER_YEAR = 252

# Monte Carlo simulation
MC_SIMULATIONS = 1000
MC_CONFIDENCE = 0.95

# Optimization
OPTIMIZE_PARAMETERS = False  # Enable parameter optimization
OPTIMIZATION_METHOD = 'grid_search'  # Options: 'grid_search', 'random_search'

# Multi-processing
USE_MULTIPROCESSING = False  # Enable for faster backtests
N_JOBS = -1  # -1 uses all available cores

# ==================== HELPER FUNCTIONS ====================

def get_date_range():
    """Return start and end dates as datetime objects"""
    return datetime.strptime(DATA_START_DATE, '%Y-%m-%d'), \
           datetime.strptime(DATA_END_DATE, '%Y-%m-%d')

def print_config():
    """Print current configuration"""
    print("="*60)
    print("CURRENT CONFIGURATION")
    print("="*60)
    print(f"Data Range: {DATA_START_DATE} to {DATA_END_DATE}")
    print(f"Tickers: {', '.join(DEFAULT_TICKERS)}")
    print(f"Initial Capital: ${INITIAL_CAPITAL:,}")
    print(f"Transaction Cost: {TRANSACTION_COST:.2%}")
    print(f"Allocation Method: {DEFAULT_ALLOCATION_METHOD}")
    print(f"Max Drawdown Limit: {MAX_DRAWDOWN_LIMIT:.0%}")
    print("="*60)

if __name__ == '__main__':
    print_config()
