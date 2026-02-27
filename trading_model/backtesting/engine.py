"""
Backtesting Engine
Tests trading strategies on historical data and calculates performance metrics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class Backtester:
    """
    Backtest trading strategies and calculate performance metrics
    """
    
    def __init__(self, initial_capital=100000, transaction_cost=0.001):
        """
        Initialize backtester
        
        Parameters:
        -----------
        initial_capital : float
            Starting capital
        transaction_cost : float
            Transaction cost per trade (as fraction)
        """
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost
        self.results = {}
    
    def run(self, strategy, price_data, returns_data):
        """
        Run backtest for a strategy
        
        Parameters:
        -----------
        strategy : BaseStrategy
            Strategy object with generate_signals method
        price_data : pd.Series or pd.DataFrame
            Price data
        returns_data : pd.Series or pd.DataFrame
            Returns data
            
        Returns:
        --------
        dict
            Backtest results and metrics
        """
        print(f"\n{'='*70}")
        print(f"RUNNING BACKTEST: {strategy.name}")
        print(f"{'='*70}\n")
        
        # Handle DataFrame input
        if isinstance(price_data, pd.DataFrame):
            ticker = price_data.columns[0]
            price_series = price_data.iloc[:, 0]
            returns_series = returns_data.iloc[:, 0]
        else:
            ticker = 'Asset'
            price_series = price_data
            returns_series = returns_data
        
        # Generate signals
        signals = strategy.generate_signals(price_series)
        
        # Get positions (shifted signals)
        positions = strategy.get_positions(signals)
        
        # Align positions with returns
        positions = positions.reindex(returns_series.index).fillna(0)
        
        # Calculate strategy returns
        strategy_returns = positions * returns_series
        
        # Apply transaction costs
        trades = positions.diff().abs()
        costs = trades * self.transaction_cost
        strategy_returns = strategy_returns - costs
        
        # Calculate cumulative returns
        cumulative_returns = (1 + strategy_returns).cumprod()
        
        # Calculate buy & hold for comparison
        buy_hold_cumulative = (1 + returns_series).cumprod()
        
        # Store results
        self.results = {
            'strategy_name': strategy.name,
            'signals': signals,
            'positions': positions,
            'strategy_returns': strategy_returns,
            'cumulative_returns': cumulative_returns,
            'buy_hold_cumulative': buy_hold_cumulative,
            'price_data': price_series,
            'market_returns': returns_series
        }
        
        # Calculate metrics
        metrics = self._calculate_metrics()
        self.results['metrics'] = metrics
        
        # Print metrics
        self._print_metrics(metrics)
        
        return self.results
    
    def _calculate_metrics(self):
        """Calculate performance metrics"""
        
        returns = self.results['strategy_returns'].dropna()
        cum_returns = self.results['cumulative_returns']
        
        # Total return
        total_return = cum_returns.iloc[-1] - 1
        
        # Annualized metrics
        n_days = len(returns)
        n_years = n_days / 252
        
        # CAGR
        cagr = (1 + total_return) ** (1 / n_years) - 1 if n_years > 0 else 0
        
        # Volatility (annualized)
        volatility = returns.std() * np.sqrt(252)
        
        # Sharpe Ratio (assuming 0% risk-free rate)
        sharpe = (returns.mean() * 252) / (returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
        
        # Maximum Drawdown
        rolling_max = cum_returns.cummax()
        drawdown = (cum_returns - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        # Calmar Ratio
        calmar = cagr / abs(max_drawdown) if max_drawdown != 0 else 0
        
        # Win Rate
        wins = (returns > 0).sum()
        total_trades = (returns != 0).sum()
        win_rate = wins / total_trades if total_trades > 0 else 0
        
        # Average win/loss
        avg_win = returns[returns > 0].mean() if (returns > 0).sum() > 0 else 0
        avg_loss = returns[returns < 0].mean() if (returns < 0).sum() > 0 else 0
        win_loss_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0
        
        # Compare to buy & hold
        buy_hold_return = self.results['buy_hold_cumulative'].iloc[-1] - 1
        outperformance = total_return - buy_hold_return
        
        metrics = {
            'Total Return': total_return,
            'CAGR': cagr,
            'Volatility': volatility,
            'Sharpe Ratio': sharpe,
            'Max Drawdown': max_drawdown,
            'Calmar Ratio': calmar,
            'Win Rate': win_rate,
            'Total Trades': int(total_trades),
            'Avg Win': avg_win,
            'Avg Loss': avg_loss,
            'Win/Loss Ratio': win_loss_ratio,
            'Buy & Hold Return': buy_hold_return,
            'Outperformance': outperformance
        }
        
        return metrics
    
    def _print_metrics(self, metrics):
        """Print performance metrics"""
        
        print("="*70)
        print("PERFORMANCE METRICS")
        print("="*70)
        print(f"Total Return................ {metrics['Total Return']:.2%}")
        print(f"CAGR........................ {metrics['CAGR']:.2%}")
        print(f"Volatility (Annual)......... {metrics['Volatility']:.2%}")
        print(f"Sharpe Ratio................ {metrics['Sharpe Ratio']:.3f}")
        print(f"Max Drawdown................ {metrics['Max Drawdown']:.2%}")
        print(f"Calmar Ratio................ {metrics['Calmar Ratio']:.3f}")
        print(f"Win Rate.................... {metrics['Win Rate']:.2%}")
        print(f"Total Trades................ {metrics['Total Trades']}")
        print(f"Avg Win..................... {metrics['Avg Win']:.4f}")
        print(f"Avg Loss.................... {metrics['Avg Loss']:.4f}")
        print(f"Win/Loss Ratio.............. {metrics['Win/Loss Ratio']:.2f}")
        print("="*70)
        print(f"Buy & Hold Return........... {metrics['Buy & Hold Return']:.2%}")
        print(f"Outperformance.............. {metrics['Outperformance']:.2%}")
        print("="*70 + "\n")
    
    def plot_results(self, save_path=None):
        """
        Plot backtest results
        
        Parameters:
        -----------
        save_path : str
            Path to save plot (optional)
        """
        fig, axes = plt.subplots(4, 1, figsize=(14, 12))
        
        # Plot 1: Cumulative Returns
        axes[0].plot(self.results['cumulative_returns'].index, 
                    self.results['cumulative_returns'],
                    label='Strategy', linewidth=2, color='blue')
        axes[0].plot(self.results['buy_hold_cumulative'].index,
                    self.results['buy_hold_cumulative'],
                    label='Buy & Hold', linewidth=2, color='orange', alpha=0.7)
        axes[0].set_title('Cumulative Returns: Strategy vs Buy & Hold', 
                         fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Cumulative Return')
        axes[0].legend(loc='best')
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Drawdown
        rolling_max = self.results['cumulative_returns'].cummax()
        drawdown = (self.results['cumulative_returns'] - rolling_max) / rolling_max
        axes[1].fill_between(drawdown.index, drawdown, 0, alpha=0.3, color='red')
        axes[1].plot(drawdown.index, drawdown, color='red', linewidth=1)
        axes[1].set_title('Drawdown', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Drawdown')
        axes[1].grid(True, alpha=0.3)
        
        # Plot 3: Price with Signals
        axes[2].plot(self.results['price_data'].index, self.results['price_data'],
                    label='Price', linewidth=1.5, color='black')
        
        # Mark buy/sell signals
        buy_signals = self.results['signals'][self.results['signals'] == 1]
        sell_signals = self.results['signals'][self.results['signals'] == -1]
        
        axes[2].scatter(buy_signals.index, 
                       self.results['price_data'].loc[buy_signals.index],
                       marker='^', color='green', s=100, label='Buy', alpha=0.7)
        axes[2].scatter(sell_signals.index,
                       self.results['price_data'].loc[sell_signals.index],
                       marker='v', color='red', s=100, label='Sell', alpha=0.7)
        
        axes[2].set_title('Price with Trading Signals', fontsize=12, fontweight='bold')
        axes[2].set_ylabel('Price')
        axes[2].legend(loc='best')
        axes[2].grid(True, alpha=0.3)
        
        # Plot 4: Rolling Sharpe (6-month window)
        rolling_sharpe = (self.results['strategy_returns'].rolling(126).mean() * 252) / \
                        (self.results['strategy_returns'].rolling(126).std() * np.sqrt(252))
        axes[3].plot(rolling_sharpe.index, rolling_sharpe, linewidth=2, color='green')
        axes[3].axhline(y=0, color='black', linestyle='--', alpha=0.3)
        axes[3].set_title('Rolling Sharpe Ratio (6-month)', fontsize=12, fontweight='bold')
        axes[3].set_ylabel('Sharpe Ratio')
        axes[3].set_xlabel('Date')
        axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Plot saved to {save_path}")
        
        plt.show()
    
    def export_results(self, filepath):
        """
        Export results to CSV
        
        Parameters:
        -----------
        filepath : str
            Path to save CSV file
        """
        results_df = pd.DataFrame({
            'Date': self.results['cumulative_returns'].index,
            'Price': self.results['price_data'].values,
            'Signal': self.results['signals'].values,
            'Position': self.results['positions'].values,
            'Strategy_Returns': self.results['strategy_returns'].values,
            'Cumulative_Returns': self.results['cumulative_returns'].values,
            'Buy_Hold_Returns': self.results['buy_hold_cumulative'].values
        })
        
        results_df.to_csv(filepath, index=False)
        print(f"✓ Results exported to {filepath}")
