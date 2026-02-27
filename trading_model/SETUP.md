# Setup Instructions

Complete guide to setting up the trading model on your local machine.

---

## Prerequisites

- **Python 3.8 or higher** installed
- **pip** package manager
- **Git** (optional, for version control)

---

## Installation Steps

### 1. Check Python Installation

Open Terminal (Mac/Linux) or Command Prompt (Windows) and run:

```bash
python --version
```

If you see `Python 3.8.x` or higher, you're good to go!

**Don't have Python?** Download from [python.org](https://www.python.org/downloads/)

---

### 2. Create Project Directory

Navigate to where you want to store the project:

```bash
# Example locations:
# Windows: cd C:\Users\YourName\Documents
# Mac/Linux: cd ~/Documents

# Create and enter project folder
mkdir trading_model
cd trading_model
```

---

### 3. Set Up Virtual Environment (RECOMMENDED)

Virtual environments keep your project dependencies isolated.

#### On Windows:
```cmd
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# You should see (venv) in your command prompt
```

#### On Mac/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your terminal
```

**To deactivate later:** Just type `deactivate`

---

### 4. Install Dependencies

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

This will install:
- pandas (data manipulation)
- numpy (numerical computing)
- matplotlib & seaborn (visualization)
- yfinance (free market data)
- jupyter (interactive notebooks)
- and more...

**Note:** This may take 2-5 minutes depending on your internet speed.

---

### 5. Verify Installation

Run this quick test:

```bash
python -c "import pandas, numpy, yfinance; print('✓ All packages installed successfully!')"
```

---

## Running the Model

### Option 1: Command Line (Simple)

Run the complete pipeline:

```bash
python main.py
```

Follow the prompts to:
1. Select a strategy
2. Choose a ticker
3. View results and plots

### Option 2: Jupyter Notebook (Interactive)

Start Jupyter:

```bash
jupyter notebook
```

This will open in your browser. Navigate to:
```
notebooks/01_getting_started.ipynb
```

Run cells step-by-step to explore!

### Option 3: Python Scripts

Create your own scripts:

```python
from data.collector import DataCollector
from strategies.moving_average import MovingAverageCrossover
from backtesting.engine import Backtester

# Your code here...
```

---

## Project Structure

```
trading_model/
├── data/                  # Data collection
│   └── collector.py      
├── strategies/           # Trading strategies
│   ├── base.py
│   ├── moving_average.py
│   ├── mean_reversion.py
│   └── momentum.py
├── backtesting/         # Backtest engine
│   └── engine.py
├── notebooks/           # Jupyter notebooks
│   └── 01_getting_started.ipynb
├── logs/                # Results and plots (created automatically)
├── config.py            # Settings
├── main.py              # Main script
└── requirements.txt     # Dependencies
```

---

## Common Issues & Solutions

### Issue: "pip not found"
**Solution:** Use `python -m pip` instead of `pip`

### Issue: "Permission denied"
**Solution (Windows):** Run Command Prompt as Administrator
**Solution (Mac/Linux):** Add `sudo` before commands

### Issue: "Module not found"
**Solution:** Make sure virtual environment is activated and packages are installed

### Issue: Downloads are slow
**Solution:** yfinance downloads can be slow. The data is cached after first download.

### Issue: Plots not showing
**Solution (Jupyter):** Add `%matplotlib inline` at the top of your notebook
**Solution (Scripts):** Make sure you have `plt.show()` after plot commands

---

## Next Steps

1. ✅ Run `python main.py` to test the full pipeline
2. ✅ Open Jupyter notebook for interactive exploration
3. ✅ Customize `config.py` with your preferences
4. ✅ Try different tickers and strategies
5. ✅ Create your own strategies

---

## Getting Help

- **Check config.py**: Most settings can be adjusted there
- **Read the code**: Everything is well-commented
- **Start simple**: Begin with the getting started notebook
- **Experiment**: Try different parameters and see what happens!

---

## Recommended Editor Setup

For the best coding experience:

### VS Code (Recommended)
1. Download from [code.visualstudio.com](https://code.visualstudio.com/)
2. Install Python extension
3. Open the trading_model folder
4. Select your virtual environment as Python interpreter

### PyCharm Community Edition
1. Download from [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)
2. Open project
3. Configure Python interpreter to use venv

### Jupyter Lab
```bash
pip install jupyterlab
jupyter lab
```

---

**You're all set!** Start with `python main.py` or open a notebook. Happy trading! 🚀
