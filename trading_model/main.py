"""
Main Execution Script
Run complete trading pipeline: Data → Strategy → Backtest → Results
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules
from data.collector import DataCollector
from strategies.moving_average import MovingAverageCrossover
from strategies.mean_reversion import MeanReversionZScore
from strategies.momentum import MomentumStrategy
from backtesting.engine import Backtester
import config

def main():
    """
    Main execution function
    """
    
    print("\n" + "="*70)
    print("QUANTITATIVE TRADING MODEL PIPELINE")
    print("="*70)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    # ==================== STEP 1: DATA COLLECTION ====================
    print("STEP 1: Data Collection & Preparation")
    print("-" * 70)
    
    collector = DataCollector(
        cache_dir=config.CACHE_DIR,
        use_cache=config.USE_CACHE
    )
    
    # Fetch data
    prices = collector.fetch_data(
        tickers=config.DEFAULT_TICKERS,
        start_date=config.DATA_START_DATE,
        end_date=config.DATA_END_DATE,
        data_type='Close'
    )
    
    # Clean data
    prices = collector.clean_data()
    
    # Calculate returns
    returns = collector.calculate_returns()
    
    # Show summary stats
    stats = collector.get_summary_stats()
    
    # ==================== STEP 2: STRATEGY SELECTION ====================
    print("\n" + "="*70)
    print("STEP 2: Strategy Selection & Signal Generation")
    print("-" * 70)
    
    # Choose which strategy to run
    print("\nAvailable Strategies:")
    print("  1. Moving Average Crossover")
    print("  2. Mean Reversion (Z-Score)")
    print("  3. Momentum")
    print("  4. Run All Strategies")
    
    choice = input("\nSelect strategy (1-4) [default: 1]: ").strip() or "1"
    
    strategies = []
    
    if choice == "1" or choice == "4":
        strategies.append(MovingAverageCrossover(
            fast=config.MA_FAST,
            slow=config.MA_SLOW
        ))
    
    if choice == "2" or choice == "4":
        strategies.append(MeanReversionZScore(
            window=config.ZSCORE_WINDOW,
            threshold=config.ZSCORE_THRESHOLD
        ))
    
    if choice == "3" or choice == "4":
        strategies.append(MomentumStrategy(
            lookback=config.MOMENTUM_LOOKBACK
        ))
    
    # Choose ticker
    print(f"\nAvailable Tickers: {', '.join(config.DEFAULT_TICKERS)}")
    ticker = input(f"Select ticker [default: {config.DEFAULT_TICKERS[0]}]: ").strip() or config.DEFAULT_TICKERS[0]
    
    if ticker not in config.DEFAULT_TICKERS:
        print(f"Warning: {ticker} not in default list. Using {config.DEFAULT_TICKERS[0]}")
        ticker = config.DEFAULT_TICKERS[0]
    
    # ==================== STEP 3: BACKTESTING ====================
    print("\n" + "="*70)
    print("STEP 3: Backtesting")
    print("-" * 70)
    
    # Initialize backtester
    backtester = Backtester(
        initial_capital=config.INITIAL_CAPITAL,
        transaction_cost=config.TRANSACTION_COST
    )
    
    # Run backtest for each strategy
    all_results = []
    
    for strategy in strategies:
        results = backtester.run(
            strategy=strategy,
            price_data=prices[ticker],
            returns_data=returns[ticker]
        )
        
        all_results.append(results)
        
        # Ask to plot
        plot_choice = input("\nPlot results? (y/n) [default: y]: ").strip().lower() or 'y'
        
        if plot_choice == 'y':
            # Create plots directory if it doesn't exist
            if not os.path.exists(config.PLOT_DIR):
                os.makedirs(config.PLOT_DIR)
            
            save_path = os.path.join(
                config.PLOT_DIR,
                f"{strategy.name.replace('/', '-')}_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            
            backtester.plot_results(save_path=save_path)
        
        # Ask to export
        export_choice = input("\nExport results to CSV? (y/n) [default: n]: ").strip().lower() or 'n'
        
        if export_choice == 'y':
            # Create results directory if it doesn't exist
            if not os.path.exists(config.RESULTS_DIR):
                os.makedirs(config.RESULTS_DIR)
            
            csv_path = os.path.join(
                config.RESULTS_DIR,
                f"{strategy.name.replace('/', '-')}_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            backtester.export_results(csv_path)
        
        print("\n" + "-"*70 + "\n")
    
    # ==================== STEP 4: COMPARISON ====================
    if len(all_results) > 1:
        print("\n" + "="*70)
        print("STEP 4: Strategy Comparison")
        print("-" * 70)
        
        import pandas as pd
        
        comparison = pd.DataFrame({
            'Strategy': [r['strategy_name'] for r in all_results],
            'Total Return': [r['metrics']['Total Return'] for r in all_results],
            'CAGR': [r['metrics']['CAGR'] for r in all_results],
            'Sharpe': [r['metrics']['Sharpe Ratio'] for r in all_results],
            'Max DD': [r['metrics']['Max Drawdown'] for r in all_results],
            'Win Rate': [r['metrics']['Win Rate'] for r in all_results],
            'Outperformance': [r['metrics']['Outperformance'] for r in all_results]
        })
        
        print("\n" + comparison.to_string(index=False))
        print("\n" + "="*70)
        
        # Find best strategy
        best_sharpe_idx = comparison['Sharpe'].idxmax()
        best_strategy = comparison.loc[best_sharpe_idx, 'Strategy']
        
        print(f"\n✓ Best Strategy (by Sharpe): {best_strategy}")
        print("="*70)
    
    # ==================== COMPLETION ====================
    print("\n" + "="*70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("="*70)
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    print("Next Steps:")
    print("  - Review the backtest results and plots")
    print("  - Experiment with different parameters in config.py")
    print("  - Try different tickers and date ranges")
    print("  - Add your own custom strategies")
    print("  - When ready, move to paper trading with Alpaca API")
    print("\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Execution interrupted by user")
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
