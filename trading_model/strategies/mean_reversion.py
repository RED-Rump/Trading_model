"""
Mean Reversion Strategy using Z-Score
Buy when price is oversold (low z-score), sell when overbought (high z-score)
"""

import pandas as pd
import numpy as np
from strategies.base import BaseStrategy

class MeanReversionZScore(BaseStrategy):
    """
    Mean Reversion Strategy using Z-Score
    
    Generates signals based on how many standard deviations 
    the price is from its moving average
    """
    
    def __init__(self, window=20, threshold=2.0, name=None):
        """
        Initialize Mean Reversion strategy
        
        Parameters:
        -----------
        window : int
            Rolling window for mean and std calculation
        threshold : float
            Z-score threshold for signals (typically 2.0)
        name : str
            Strategy name (optional)
        """
        if name is None:
            name = f"Mean Reversion (Z={threshold})"
        super().__init__(name)
        
        self.window = window
        self.threshold = threshold
        self.zscore = None
        self.rolling_mean = None
        self.rolling_std = None
    
    def generate_signals(self, data):
        """
        Generate trading signals based on z-score
        
        Parameters:
        -----------
        data : pd.Series or pd.DataFrame
            Price data (if DataFrame, uses first column)
            
        Returns:
        --------
        pd.Series
            Trading signals (1 = buy, -1 = sell, 0 = neutral)
        """
        # Handle DataFrame input
        if isinstance(data, pd.DataFrame):
            data = data.iloc[:, 0]
        
        # Calculate rolling statistics
        self.rolling_mean = data.rolling(window=self.window).mean()
        self.rolling_std = data.rolling(window=self.window).std()
        
        # Calculate z-score
        self.zscore = (data - self.rolling_mean) / self.rolling_std
        
        # Generate signals
        signals = pd.Series(0, index=data.index, name='signal')
        signals[self.zscore > self.threshold] = -1   # Overbought - sell
        signals[self.zscore < -self.threshold] = 1   # Oversold - buy
        
        self.signals = signals
        
        return signals
    
    def get_zscore_data(self):
        """
        Get z-score data for plotting
        
        Returns:
        --------
        dict
            Dictionary containing z-score and thresholds
        """
        return {
            'zscore': self.zscore,
            'threshold': self.threshold,
            'rolling_mean': self.rolling_mean,
            'rolling_std': self.rolling_std
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
    strategy = MeanReversionZScore(window=20, threshold=2.0)
    signals = strategy.generate_signals(prices)
    
    # Print info
    strategy.print_info()
    
    print(f"Last 10 signals:")
    print(signals.tail(10))
