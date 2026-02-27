"""
Momentum Strategy
Buy when momentum is positive, sell when negative
"""

import pandas as pd
import numpy as np
from strategies.base import BaseStrategy

class MomentumStrategy(BaseStrategy):
    """
    Momentum Strategy
    
    Generates buy signal when price momentum is positive
    Generates sell signal when price momentum is negative
    """
    
    def __init__(self, lookback=20, name=None):
        """
        Initialize Momentum strategy
        
        Parameters:
        -----------
        lookback : int
            Lookback period for momentum calculation
        name : str
            Strategy name (optional)
        """
        if name is None:
            name = f"Momentum ({lookback}d)"
        super().__init__(name)
        
        self.lookback = lookback
        self.momentum = None
    
    def generate_signals(self, data):
        """
        Generate trading signals based on momentum
        
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
        
        # Calculate momentum (percentage change over lookback period)
        self.momentum = data.pct_change(periods=self.lookback)
        
        # Generate signals
        signals = pd.Series(0, index=data.index, name='signal')
        signals[self.momentum > 0] = 1   # Positive momentum - buy
        signals[self.momentum <= 0] = -1  # Negative momentum - sell
        
        self.signals = signals
        
        return signals
    
    def get_momentum_data(self):
        """
        Get momentum data for plotting
        
        Returns:
        --------
        dict
            Dictionary containing momentum data
        """
        return {
            'momentum': self.momentum,
            'lookback': self.lookback
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
    strategy = MomentumStrategy(lookback=20)
    signals = strategy.generate_signals(prices)
    
    # Print info
    strategy.print_info()
    
    print(f"Last 10 signals:")
    print(signals.tail(10))
