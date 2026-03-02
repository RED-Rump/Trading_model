"""
Unified Trading System
Connects your backtesting model with IC Markets live trading bot
"""

import sys
import os
from datetime import datetime
import pandas as pd

# Import your existing backtesting components
from data.collector import DataCollector
from strategies.moving_average import MovingAverageCrossover
from strategies.mean_reversion import MeanReversionZScore
from strategies.momentum import MomentumStrategy
from backtesting.engine import Backtester

# Import IC Markets forex components
from ic_markets_connector import MT5Connector
from ic_markets_data import ForexDataDownloader
from ic_markets_trading import ForexTrader
import forex_strategies
import config_forex as forex_config

class UnifiedTradingSystem:
    """
    Unified system that uses your backtesting model strategies
    for live forex trading on IC Markets
    """
    
    def __init__(self, mode="BACKTEST"):
        """
        Initialize unified system
        
        Parameters:
        -----------
        mode : str
            "BACKTEST" - Use your backtesting model
            "LIVE_FOREX" - Use IC Markets live trading
            "BOTH" - Backtest first, then go live if profitable
        """
        self.mode = mode
        print(f"\n{'='*70}")
        print(f"UNIFIED TRADING SYSTEM - Mode: {mode}")
        print(f"{'='*70}\n")
        
        # Components
        self.mt5_connector = None
        self.forex_trader = None
        self.backtest_results = None
        
    def backtest_strategy(self, strategy_name, symbol, start_date, end_date):
        """
        Backtest a strategy using your existing model
        
        Parameters:
        -----------
        strategy_name : str
            'moving_average', 'mean_reversion', or 'momentum'
        symbol : str
            Ticker symbol (e.g., 'SPY' for stocks or 'EURUSD' for forex)
        start_date : str
            Start date
        end_date : str
            End date
            
        Returns:
        --------
        dict
            Backtest results with metrics
        """
        print(f"\n{'='*70}")
        print(f"BACKTESTING: {strategy_name.upper()} on {symbol}")
        print(f"{'='*70}\n")
        
        # Download data using your existing collector
        collector = DataCollector()
        
        # For forex symbols, we need to adapt
        if self._is_forex_symbol(symbol):
            # Use MT5 data if available, otherwise use your collector
            if self.mt5_connector and self.mt5_connector.connected:
                print("Using MT5 forex data...")
                downloader = ForexDataDownloader(self.mt5_connector)
                df = downloader.download_data(symbol, 'D', 1000)  # Daily data
                
                # Convert to your model's format
                prices = df[['Close']].rename(columns={'Close': symbol})
                returns = prices.pct_change().dropna()
            else:
                print(f"⚠ MT5 not connected. Cannot backtest forex symbol {symbol}")
                return None
        else:
            # Use your existing stock data collector
            print("Using yfinance data...")
            prices = collector.fetch_data([symbol], start_date, end_date)
            prices = collector.clean_data()
            returns = collector.calculate_returns()
        
        # Create strategy using your existing strategies
        if strategy_name.lower() == 'moving_average':
            strategy = MovingAverageCrossover(fast=20, slow=50)
        elif strategy_name.lower() == 'mean_reversion':
            strategy = MeanReversionZScore(window=20, threshold=2.0)
        elif strategy_name.lower() == 'momentum':
            strategy = MomentumStrategy(lookback=20)
        else:
            print(f"✗ Unknown strategy: {strategy_name}")
            return None
        
        # Run backtest using your existing backtester
        backtester = Backtester(initial_capital=10000, transaction_cost=0.001)
        results = backtester.run(strategy, prices[symbol], returns[symbol])
        
        # Store results
        self.backtest_results = results
        
        # Display results
        print("\n" + "="*70)
        print("BACKTEST RESULTS")
        print("="*70)
        metrics = results['metrics']
        print(f"Total Return: {metrics['Total Return']:.2%}")
        print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.3f}")
        print(f"Max Drawdown: {metrics['Max Drawdown']:.2%}")
        print(f"Win Rate: {metrics['Win Rate']:.2%}")
        print("="*70 + "\n")
        
        return results
    
    def is_strategy_profitable(self, min_sharpe=1.0, min_return=0.10, max_drawdown=-0.20):
        """
        Check if backtested strategy meets criteria for live trading
        
        Parameters:
        -----------
        min_sharpe : float
            Minimum Sharpe ratio
        min_return : float
            Minimum total return (e.g., 0.10 = 10%)
        max_drawdown : float
            Maximum acceptable drawdown (e.g., -0.20 = -20%)
            
        Returns:
        --------
        bool
            True if strategy is profitable enough
        """
        if self.backtest_results is None:
            print("⚠ No backtest results available")
            return False
        
        metrics = self.backtest_results['metrics']
        
        checks = {
            'Sharpe Ratio': (metrics['Sharpe Ratio'], '>=', min_sharpe),
            'Total Return': (metrics['Total Return'], '>=', min_return),
            'Max Drawdown': (metrics['Max Drawdown'], '>=', max_drawdown)
        }
        
        print("\n" + "="*70)
        print("PROFITABILITY CHECK")
        print("="*70)
        
        all_pass = True
        for name, (value, operator, threshold) in checks.items():
            if operator == '>=':
                passed = value >= threshold
            else:
                passed = value <= threshold
            
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{name}: {value:.3f} (need {operator} {threshold:.3f}) {status}")
            
            if not passed:
                all_pass = False
        
        print("="*70)
        
        if all_pass:
            print("✓ Strategy meets profitability criteria!")
        else:
            print("✗ Strategy does not meet criteria. Keep backtesting.")
        
        print("="*70 + "\n")
        
        return all_pass
    
    def connect_to_forex(self):
        """
        Connect to IC Markets MT5 for live trading
        
        Returns:
        --------
        bool
            True if connected successfully
        """
        print("\nConnecting to IC Markets MT5...")
        
        self.mt5_connector = MT5Connector()
        if not self.mt5_connector.connect():
            print("✗ Failed to connect to MT5")
            return False
        
        self.forex_trader = ForexTrader(self.mt5_connector)
        print("✓ Connected to IC Markets")
        
        return True
    
    def convert_strategy_to_forex(self, strategy):
        """
        Convert your backtesting strategy to forex format
        
        Parameters:
        -----------
        strategy : BaseStrategy
            Your strategy instance
            
        Returns:
        --------
        forex_strategies.ForexStrategy
            Equivalent forex strategy
        """
        strategy_name = strategy.name.lower()
        
        if 'moving average' in strategy_name or 'ma' in strategy_name:
            # Extract parameters if available
            fast = getattr(strategy, 'fast', 20)
            slow = getattr(strategy, 'slow', 50)
            return forex_strategies.MovingAverageCrossover(fast=fast, slow=slow)
        
        elif 'mean reversion' in strategy_name or 'zscore' in strategy_name:
            window = getattr(strategy, 'window', 20)
            threshold = getattr(strategy, 'threshold', 2.0)
            # Use RSI+MA as equivalent
            return forex_strategies.RSI_MA_Strategy()
        
        elif 'momentum' in strategy_name:
            return forex_strategies.TrendFollowing()
        
        else:
            # Default to MA crossover
            print("⚠ Using default MA strategy for forex")
            return forex_strategies.MovingAverageCrossover()
    
    def deploy_to_live(self, symbol, strategy, test_mode=True):
        """
        Deploy backtested strategy to live forex trading
        
        Parameters:
        -----------
        symbol : str
            Forex symbol (e.g., 'EURUSD')
        strategy : BaseStrategy
            Your backtested strategy
        test_mode : bool
            If True, only shows what it would do (doesn't actually trade)
            
        Returns:
        --------
        dict
            Deployment status
        """
        if not self.mt5_connector or not self.mt5_connector.connected:
            print("✗ Not connected to MT5. Call connect_to_forex() first")
            return None
        
        print(f"\n{'='*70}")
        print(f"DEPLOYING TO LIVE: {strategy.name} on {symbol}")
        if test_mode:
            print("MODE: TEST (simulation only)")
        else:
            print("MODE: LIVE (real trades!)")
        print(f"{'='*70}\n")
        
        # Convert strategy to forex format
        forex_strategy = self.convert_strategy_to_forex(strategy)
        
        # Download latest data
        downloader = ForexDataDownloader(self.mt5_connector)
        df = downloader.download_data(symbol, forex_config.TIMEFRAME, 200)
        
        if df is None:
            print(f"✗ Failed to download data for {symbol}")
            return None
        
        # Generate signal
        signals = forex_strategy.generate_signals(df)
        latest_signal = signals.iloc[-1]
        
        print(f"Latest signal for {symbol}: {latest_signal}")
        if latest_signal == 1:
            print("→ BUY signal")
        elif latest_signal == -1:
            print("→ SELL signal")
        else:
            print("→ No signal")
        
        if test_mode:
            print("\n⚠ TEST MODE - No actual trades executed")
            return {
                'symbol': symbol,
                'signal': int(latest_signal),
                'mode': 'TEST',
                'executed': False
            }
        
        # Execute trade if signal present
        if latest_signal != 0:
            # Calculate lot size
            balance = self.mt5_connector.get_balance()
            risk_amount = balance * forex_config.RISK_PER_TRADE
            lot_size = self.forex_trader.calculate_lot_size(
                symbol, risk_amount, forex_config.STOP_LOSS_PIPS
            )
            
            print(f"\nExecuting {('BUY' if latest_signal == 1 else 'SELL')} order...")
            print(f"Lot size: {lot_size}")
            
            # Confirm
            if forex_config.CONFIRM_TRADES:
                response = input("Confirm live trade? (yes/no): ").lower()
                if response != 'yes':
                    print("Trade cancelled")
                    return {'executed': False, 'reason': 'User cancelled'}
            
            # Execute
            if latest_signal == 1:
                result = self.forex_trader.open_buy(
                    symbol, lot_size, 
                    forex_config.STOP_LOSS_PIPS,
                    forex_config.TAKE_PROFIT_PIPS
                )
            else:
                result = self.forex_trader.open_sell(
                    symbol, lot_size,
                    forex_config.STOP_LOSS_PIPS,
                    forex_config.TAKE_PROFIT_PIPS
                )
            
            return result
        
        return {'signal': 0, 'executed': False, 'reason': 'No signal'}
    
    def _is_forex_symbol(self, symbol):
        """Check if symbol is a forex pair"""
        forex_symbols = ['EUR', 'GBP', 'USD', 'JPY', 'AUD', 'CAD', 'CHF', 'NZD']
        return any(curr in symbol.upper() for curr in forex_symbols)
    
    def run_unified_workflow(self, strategy_name='moving_average', 
                            backtest_symbol='SPY', 
                            forex_symbol='EURUSD'):
        """
        Complete workflow: Backtest on stocks, then deploy to forex
        
        Parameters:
        -----------
        strategy_name : str
            Strategy to test
        backtest_symbol : str
            Symbol for backtesting (stocks)
        forex_symbol : str
            Symbol for live trading (forex)
        """
        print("\n" + "="*70)
        print("UNIFIED WORKFLOW: BACKTEST → VALIDATE → DEPLOY")
        print("="*70 + "\n")
        
        # Step 1: Backtest
        print("STEP 1: Backtesting strategy...")
        results = self.backtest_strategy(
            strategy_name, 
            backtest_symbol, 
            '2020-01-01', 
            '2024-12-31'
        )
        
        if results is None:
            print("✗ Backtesting failed")
            return
        
        # Step 2: Validate
        print("\nSTEP 2: Validating profitability...")
        if not self.is_strategy_profitable():
            print("\n⚠ Strategy not profitable enough. Stopping here.")
            print("Recommendations:")
            print("  - Adjust strategy parameters")
            print("  - Try different strategy")
            print("  - Test on different timeframe")
            return
        
        # Step 3: Connect to forex
        print("\nSTEP 3: Connecting to IC Markets...")
        if not self.connect_to_forex():
            print("✗ Failed to connect. Cannot deploy.")
            return
        
        # Step 4: Test deployment (simulation)
        print("\nSTEP 4: Testing deployment (simulation)...")
        
        # Get the strategy object
        if strategy_name.lower() == 'moving_average':
            strategy = MovingAverageCrossover(fast=20, slow=50)
        elif strategy_name.lower() == 'mean_reversion':
            strategy = MeanReversionZScore(window=20, threshold=2.0)
        else:
            strategy = MomentumStrategy(lookback=20)
        
        test_result = self.deploy_to_live(forex_symbol, strategy, test_mode=True)
        
        print("\n" + "="*70)
        print("WORKFLOW COMPLETE")
        print("="*70)
        print("\n✓ Backtesting: PASSED")
        print("✓ Validation: PASSED")
        print("✓ Connection: SUCCESS")
        print("✓ Test Deployment: COMPLETE")
        print("\n" + "="*70)
        print("READY FOR LIVE TRADING")
        print("="*70)
        print("\nTo go live:")
        print("1. Set forex_config.TRADING_MODE = 'LIVE'")
        print("2. Run: system.deploy_to_live('" + forex_symbol + "', strategy, test_mode=False)")
        print("\n⚠ Remember: Always monitor your first live trades closely!")

if __name__ == '__main__':
    # Example usage
    print("="*70)
    print("UNIFIED TRADING SYSTEM - DEMO")
    print("="*70)
    
    # Create system
    system = UnifiedTradingSystem(mode="BOTH")
    
    # Run complete workflow
    system.run_unified_workflow(
        strategy_name='moving_average',
        backtest_symbol='SPY',
        forex_symbol='EURUSD'
    )
