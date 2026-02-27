"""
Trading Model GUI Application
Professional graphical interface for backtesting trading strategies
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkfont
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.collector import DataCollector
from strategies.moving_average import MovingAverageCrossover
from strategies.mean_reversion import MeanReversionZScore
from strategies.momentum import MomentumStrategy
from backtesting.engine import Backtester
import config

class TradingModelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Model - Backtesting Platform")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.collector = None
        self.prices = None
        self.returns = None
        self.results = None
        
        # Create main layout
        self.create_menu()
        self.create_main_layout()
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Results", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_main_layout(self):
        """Create main application layout"""
        
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_font = tkfont.Font(family="Arial", size=18, weight="bold")
        title_label = tk.Label(title_frame, text="📈 Trading Model Backtesting Platform", 
                              font=title_font, bg='#2c3e50', fg='white')
        title_label.pack(pady=15)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, bg='white', width=350, relief=tk.RAISED, borderwidth=1)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right panel - Results
        right_panel = tk.Frame(main_container, bg='white', relief=tk.RAISED, borderwidth=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Build panels
        self.build_control_panel(left_panel)
        self.build_results_panel(right_panel)
        
    def build_control_panel(self, parent):
        """Build left control panel"""
        
        # Header
        header = tk.Label(parent, text="Control Panel", font=("Arial", 14, "bold"),
                         bg='white', fg='#2c3e50')
        header.pack(pady=15)
        
        # Scrollable frame for controls
        canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Step 1: Data Settings
        self.create_section(scrollable_frame, "1️⃣ Data Settings")
        
        # Ticker selection
        tk.Label(scrollable_frame, text="Select Ticker:", bg='white', 
                font=("Arial", 10)).pack(anchor='w', padx=20, pady=(10, 5))
        
        self.ticker_var = tk.StringVar(value=config.DEFAULT_TICKERS[0])
        ticker_dropdown = ttk.Combobox(scrollable_frame, textvariable=self.ticker_var,
                                      values=config.DEFAULT_TICKERS, state='readonly', width=25)
        ticker_dropdown.pack(padx=20, pady=(0, 10))
        
        # Date range
        tk.Label(scrollable_frame, text="Start Date:", bg='white',
                font=("Arial", 10)).pack(anchor='w', padx=20, pady=(5, 2))
        self.start_date_var = tk.StringVar(value=config.DATA_START_DATE)
        tk.Entry(scrollable_frame, textvariable=self.start_date_var, width=28).pack(padx=20)
        
        tk.Label(scrollable_frame, text="End Date:", bg='white',
                font=("Arial", 10)).pack(anchor='w', padx=20, pady=(10, 2))
        self.end_date_var = tk.StringVar(value=config.DATA_END_DATE)
        tk.Entry(scrollable_frame, textvariable=self.end_date_var, width=28).pack(padx=20)
        
        # Download button
        download_btn = tk.Button(scrollable_frame, text="📥 Download Data",
                                command=self.download_data, bg='#3498db', fg='white',
                                font=("Arial", 10, "bold"), cursor="hand2", width=25)
        download_btn.pack(pady=15, padx=20)
        
        # Step 2: Strategy Selection
        self.create_section(scrollable_frame, "2️⃣ Strategy Selection")
        
        self.strategy_var = tk.StringVar(value="moving_average")
        
        strategies = [
            ("Moving Average Crossover", "moving_average"),
            ("Mean Reversion (Z-Score)", "mean_reversion"),
            ("Momentum", "momentum")
        ]
        
        for text, value in strategies:
            rb = tk.Radiobutton(scrollable_frame, text=text, variable=self.strategy_var,
                              value=value, bg='white', font=("Arial", 10))
            rb.pack(anchor='w', padx=30, pady=5)
        
        # Step 3: Strategy Parameters
        self.create_section(scrollable_frame, "3️⃣ Parameters")
        
        # MA parameters
        self.ma_fast_var = tk.IntVar(value=config.MA_FAST)
        self.ma_slow_var = tk.IntVar(value=config.MA_SLOW)
        
        tk.Label(scrollable_frame, text="MA Fast Period:", bg='white',
                font=("Arial", 9)).pack(anchor='w', padx=30, pady=(5, 2))
        tk.Entry(scrollable_frame, textvariable=self.ma_fast_var, width=28).pack(padx=30)
        
        tk.Label(scrollable_frame, text="MA Slow Period:", bg='white',
                font=("Arial", 9)).pack(anchor='w', padx=30, pady=(10, 2))
        tk.Entry(scrollable_frame, textvariable=self.ma_slow_var, width=28).pack(padx=30)
        
        # Z-score parameters
        self.zscore_window_var = tk.IntVar(value=config.ZSCORE_WINDOW)
        self.zscore_threshold_var = tk.DoubleVar(value=config.ZSCORE_THRESHOLD)
        
        tk.Label(scrollable_frame, text="Z-Score Window:", bg='white',
                font=("Arial", 9)).pack(anchor='w', padx=30, pady=(10, 2))
        tk.Entry(scrollable_frame, textvariable=self.zscore_window_var, width=28).pack(padx=30)
        
        tk.Label(scrollable_frame, text="Z-Score Threshold:", bg='white',
                font=("Arial", 9)).pack(anchor='w', padx=30, pady=(10, 2))
        tk.Entry(scrollable_frame, textvariable=self.zscore_threshold_var, width=28).pack(padx=30)
        
        # Momentum parameters
        self.momentum_lookback_var = tk.IntVar(value=config.MOMENTUM_LOOKBACK)
        
        tk.Label(scrollable_frame, text="Momentum Lookback:", bg='white',
                font=("Arial", 9)).pack(anchor='w', padx=30, pady=(10, 2))
        tk.Entry(scrollable_frame, textvariable=self.momentum_lookback_var, width=28).pack(padx=30)
        
        # Step 4: Run Backtest
        self.create_section(scrollable_frame, "4️⃣ Run Backtest")
        
        run_btn = tk.Button(scrollable_frame, text="▶️ Run Backtest",
                           command=self.run_backtest, bg='#27ae60', fg='white',
                           font=("Arial", 12, "bold"), cursor="hand2", width=25, height=2)
        run_btn.pack(pady=15, padx=20)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def build_results_panel(self, parent):
        """Build right results panel"""
        
        # Header
        header = tk.Label(parent, text="Results & Metrics", font=("Arial", 14, "bold"),
                         bg='white', fg='#2c3e50')
        header.pack(pady=15)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Metrics
        metrics_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(metrics_frame, text="📊 Metrics")
        
        self.metrics_text = scrolledtext.ScrolledText(metrics_frame, wrap=tk.WORD,
                                                      font=("Courier", 10), height=20)
        self.metrics_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 2: Chart
        chart_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(chart_frame, text="📈 Chart")
        
        self.chart_container = chart_frame
        
        # Tab 3: Log
        log_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(log_frame, text="📝 Log")
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD,
                                                  font=("Courier", 9), height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log("Welcome to Trading Model Backtesting Platform!")
        self.log("Step 1: Download data for your selected ticker")
        self.log("Step 2: Choose a strategy")
        self.log("Step 3: Adjust parameters if needed")
        self.log("Step 4: Click 'Run Backtest' to see results")
        
    def create_section(self, parent, title):
        """Create a section header"""
        frame = tk.Frame(parent, bg='#ecf0f1', height=35)
        frame.pack(fill=tk.X, pady=(15, 10))
        frame.pack_propagate(False)
        
        label = tk.Label(frame, text=title, font=("Arial", 11, "bold"),
                        bg='#ecf0f1', fg='#2c3e50')
        label.pack(pady=7, padx=10, anchor='w')
        
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"[{self.get_timestamp()}] {message}\n")
        self.log_text.see(tk.END)
        
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
        
    def download_data(self):
        """Download market data"""
        self.log("Starting data download...")
        
        # Run in thread to avoid freezing UI
        thread = threading.Thread(target=self._download_data_thread)
        thread.daemon = True
        thread.start()
        
    def _download_data_thread(self):
        """Thread function for downloading data"""
        try:
            ticker = self.ticker_var.get()
            start_date = self.start_date_var.get()
            end_date = self.end_date_var.get()
            
            self.log(f"Downloading {ticker} from {start_date} to {end_date}...")
            
            # Initialize collector
            self.collector = DataCollector(use_cache=True)
            
            # Fetch data
            self.prices = self.collector.fetch_data([ticker], start_date, end_date, 'Close')
            self.prices = self.collector.clean_data()
            self.returns = self.collector.calculate_returns()
            
            self.log(f"✓ Data downloaded successfully! ({len(self.prices)} rows)")
            self.log(f"Date range: {self.prices.index[0]} to {self.prices.index[-1]}")
            
            messagebox.showinfo("Success", f"Data downloaded successfully!\n{len(self.prices)} rows")
            
        except Exception as e:
            self.log(f"✗ Error downloading data: {e}")
            messagebox.showerror("Error", f"Failed to download data:\n{e}")
            
    def run_backtest(self):
        """Run backtest"""
        if self.prices is None:
            messagebox.showwarning("No Data", "Please download data first!")
            return
            
        self.log("Starting backtest...")
        
        # Run in thread
        thread = threading.Thread(target=self._run_backtest_thread)
        thread.daemon = True
        thread.start()
        
    def _run_backtest_thread(self):
        """Thread function for running backtest"""
        try:
            ticker = self.ticker_var.get()
            strategy_type = self.strategy_var.get()
            
            # Create strategy
            if strategy_type == "moving_average":
                strategy = MovingAverageCrossover(
                    fast=self.ma_fast_var.get(),
                    slow=self.ma_slow_var.get()
                )
            elif strategy_type == "mean_reversion":
                strategy = MeanReversionZScore(
                    window=self.zscore_window_var.get(),
                    threshold=self.zscore_threshold_var.get()
                )
            else:  # momentum
                strategy = MomentumStrategy(
                    lookback=self.momentum_lookback_var.get()
                )
            
            self.log(f"Running {strategy.name} on {ticker}...")
            
            # Run backtest
            backtester = Backtester(
                initial_capital=config.INITIAL_CAPITAL,
                transaction_cost=config.TRANSACTION_COST
            )
            
            self.results = backtester.run(
                strategy=strategy,
                price_data=self.prices[ticker],
                returns_data=self.returns[ticker]
            )
            
            self.log("✓ Backtest completed!")
            
            # Display results
            self.display_results()
            
            messagebox.showinfo("Success", "Backtest completed successfully!")
            
        except Exception as e:
            self.log(f"✗ Error running backtest: {e}")
            messagebox.showerror("Error", f"Failed to run backtest:\n{e}")
            
    def display_results(self):
        """Display backtest results"""
        if self.results is None:
            return
            
        # Clear metrics text
        self.metrics_text.delete(1.0, tk.END)
        
        # Format metrics
        metrics = self.results['metrics']
        
        text = "="*60 + "\n"
        text += "BACKTEST RESULTS\n"
        text += "="*60 + "\n\n"
        text += f"Strategy: {self.results['strategy_name']}\n"
        text += f"Ticker: {self.ticker_var.get()}\n\n"
        text += "="*60 + "\n"
        text += "PERFORMANCE METRICS\n"
        text += "="*60 + "\n"
        text += f"Total Return................ {metrics['Total Return']:.2%}\n"
        text += f"CAGR........................ {metrics['CAGR']:.2%}\n"
        text += f"Volatility (Annual)......... {metrics['Volatility']:.2%}\n"
        text += f"Sharpe Ratio................ {metrics['Sharpe Ratio']:.3f}\n"
        text += f"Max Drawdown................ {metrics['Max Drawdown']:.2%}\n"
        text += f"Calmar Ratio................ {metrics['Calmar Ratio']:.3f}\n"
        text += f"Win Rate.................... {metrics['Win Rate']:.2%}\n"
        text += f"Total Trades................ {metrics['Total Trades']}\n"
        text += f"Avg Win..................... {metrics['Avg Win']:.4f}\n"
        text += f"Avg Loss.................... {metrics['Avg Loss']:.4f}\n"
        text += f"Win/Loss Ratio.............. {metrics['Win/Loss Ratio']:.2f}\n"
        text += "="*60 + "\n"
        text += f"Buy & Hold Return........... {metrics['Buy & Hold Return']:.2%}\n"
        text += f"Outperformance.............. {metrics['Outperformance']:.2%}\n"
        text += "="*60 + "\n"
        
        self.metrics_text.insert(1.0, text)
        
        # Create chart
        self.create_chart()
        
        # Switch to metrics tab
        self.notebook.select(0)
        
    def create_chart(self):
        """Create performance chart"""
        # Clear existing chart
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        
        # Create figure
        fig = Figure(figsize=(10, 8), dpi=100)
        
        # Plot 1: Cumulative returns
        ax1 = fig.add_subplot(3, 1, 1)
        ax1.plot(self.results['cumulative_returns'].index,
                self.results['cumulative_returns'],
                label='Strategy', linewidth=2, color='blue')
        ax1.plot(self.results['buy_hold_cumulative'].index,
                self.results['buy_hold_cumulative'],
                label='Buy & Hold', linewidth=2, color='orange', alpha=0.7)
        ax1.set_title('Cumulative Returns: Strategy vs Buy & Hold', fontweight='bold')
        ax1.set_ylabel('Cumulative Return')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Drawdown
        ax2 = fig.add_subplot(3, 1, 2)
        rolling_max = self.results['cumulative_returns'].cummax()
        drawdown = (self.results['cumulative_returns'] - rolling_max) / rolling_max
        ax2.fill_between(drawdown.index, drawdown, 0, alpha=0.3, color='red')
        ax2.plot(drawdown.index, drawdown, color='red', linewidth=1)
        ax2.set_title('Drawdown', fontweight='bold')
        ax2.set_ylabel('Drawdown')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Price with signals
        ax3 = fig.add_subplot(3, 1, 3)
        ax3.plot(self.results['price_data'].index, self.results['price_data'],
                linewidth=1.5, color='black', label='Price')
        
        # Buy/sell signals
        buy_signals = self.results['signals'][self.results['signals'] == 1]
        sell_signals = self.results['signals'][self.results['signals'] == -1]
        
        if len(buy_signals) > 0:
            ax3.scatter(buy_signals.index,
                       self.results['price_data'].loc[buy_signals.index],
                       marker='^', color='green', s=50, label='Buy', alpha=0.7)
        if len(sell_signals) > 0:
            ax3.scatter(sell_signals.index,
                       self.results['price_data'].loc[sell_signals.index],
                       marker='v', color='red', s=50, label='Sell', alpha=0.7)
        
        ax3.set_title('Price with Trading Signals', fontweight='bold')
        ax3.set_ylabel('Price')
        ax3.set_xlabel('Date')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def export_results(self):
        """Export results to CSV"""
        if self.results is None:
            messagebox.showwarning("No Results", "Please run a backtest first!")
            return
            
        try:
            from tkinter import filedialog
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filepath:
                import pandas as pd
                results_df = pd.DataFrame({
                    'Date': self.results['cumulative_returns'].index,
                    'Price': self.results['price_data'].values,
                    'Signal': self.results['signals'].values,
                    'Position': self.results['positions'].values,
                    'Strategy_Returns': self.results['strategy_returns'].values,
                    'Cumulative_Returns': self.results['cumulative_returns'].values,
                })
                results_df.to_csv(filepath, index=False)
                
                self.log(f"✓ Results exported to {filepath}")
                messagebox.showinfo("Success", f"Results exported to:\n{filepath}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export results:\n{e}")
            
    def show_about(self):
        """Show about dialog"""
        about_text = """
        Trading Model Backtesting Platform
        Version 1.0
        
        A professional tool for backtesting
        quantitative trading strategies.
        
        Features:
        • Multiple trading strategies
        • Customizable parameters
        • Performance metrics
        • Visual charts
        • CSV export
        
        © 2026 - Built with Python & Tkinter
        """
        messagebox.showinfo("About", about_text)

def main():
    """Main function"""
    root = tk.Tk()
    app = TradingModelGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
