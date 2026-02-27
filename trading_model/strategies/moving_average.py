"""
Moving Average Crossover Strategy
Buy when fast MA crosses above slow MA, sell when it crosses below
"""

import pandas as pd
import numpy as np
from strategies.base import BaseStrategy

class MovingAverageCrossover(BaseStrategy):
    """
    Moving Average Crossover Strategy
    
    Generates buy signal when fast MA > slow MA
    Generates sell signal when fast MA <= slow MA
    """
    
    def __init__(self, fast=20, slow=50, name=None):
        """
        Initialize MA Crossover strategy
        
        Parameters:
        -----------
        fast : int
            Fast moving average period
        slow : int
            Slow moving average period
        name : str
            Strategy name (optional)
        """
        if name is None:
            name = f"MA Crossover ({fast}/{slow})"
        super().__init__(name)
        
        self.fast = fast
        self.slow = slow
        self.ma_fast = None
        self.ma_slow = None
    
    def generate_signals(self, data):
        """
        Generate trading signals based on MA crossover
        
        Parameters:
        -----------
        data : pd.Series or pd.DataFrame
            Price data (if DataFrame, uses first column)
            
        Returns:
        --------
        pd.Series
            Trading signals (1 = buy, -1 = sell)
        """
        # Handle DataFrame input
        if isinstance(data, pd.DataFrame):
            data = data.iloc[:, 0]
        
        # Calculate moving averages
        self.ma_fast = data.rolling(window=self.fast).mean()
        self.ma_slow = data.rolling(window=self.slow).mean()
        
        # Generate signals
        signals = pd.Series(0, index=data.index, name='signal')
        signals[self.ma_fast > self.ma_slow] = 1   # Buy
        signals[self.ma_fast <= self.ma_slow] = -1  # Sell
        
        self.signals = signals
        
        return signals
    
    def get_ma_data(self):
        """
        Get moving average data for plotting
        
        Returns:
        --------
        dict
            Dictionary containing MA data
        """
        return {
            'ma_fast': self.ma_fast,
            'ma_slow': self.ma_slow
        }

if __name__ == '__main__':
    # Example usage
    import sys
    sys.path.append('..')
    from data.collector import DataCollector
    
    # Get data
    collector = DataCollector()
    prices = collector.fetch_data('SPY', '2020-01-01', '2024-12-31')
    
    # Create strategy
    strategy = MovingAverageCrossover(fast=20, slow=50)
    signals = strategy.generate_signals(prices)
    
    # Print info
    strategy.print_info()
    
    print(f"Last 10 signals:")
    print(signals.tail(10))
