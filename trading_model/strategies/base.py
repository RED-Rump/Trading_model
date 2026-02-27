"""
Base Strategy Class
All trading strategies inherit from this base class
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies
    
    All strategies must implement:
    - generate_signals(): Create buy/sell signals
    """
    
    def __init__(self, name="Base Strategy"):
        """
        Initialize base strategy
        
        Parameters:
        -----------
        name : str
            Strategy name
        """
        self.name = name
        self.signals = None
        self.positions = None
        
    @abstractmethod
    def generate_signals(self, data):
        """
        Generate trading signals
        
        Must be implemented by child classes
        
        Parameters:
        -----------
        data : pd.DataFrame or pd.Series
            Price data
            
        Returns:
        --------
        pd.Series
            Trading signals (1 = buy, -1 = sell, 0 = neutral)
        """
        pass
    
    def get_positions(self, signals):
        """
        Convert signals to positions
        
        Parameters:
        -----------
        signals : pd.Series
            Trading signals
            
        Returns:
        --------
        pd.Series
            Positions (shifted signals for next-day execution)
        """
        # Use previous day's signal for execution
        self.positions = signals.shift(1).fillna(0)
        return self.positions
    
    def calculate_returns(self, positions, market_returns):
        """
        Calculate strategy returns
        
        Parameters:
        -----------
        positions : pd.Series
            Position sizes
        market_returns : pd.Series
            Market returns
            
        Returns:
        --------
        pd.Series
            Strategy returns
        """
        return positions * market_returns
    
    def print_info(self):
        """Print strategy information"""
        print(f"\n{'='*60}")
        print(f"Strategy: {self.name}")
        print(f"{'='*60}")
        
        if self.signals is not None:
            unique_signals = self.signals.value_counts()
            print(f"\nSignal Distribution:")
            print(unique_signals)
            
            # Calculate some basic stats
            if 1 in unique_signals.index:
                buy_pct = unique_signals[1] / len(self.signals) * 100
                print(f"\nBuy signals: {buy_pct:.1f}%")
            if -1 in unique_signals.index:
                sell_pct = unique_signals[-1] / len(self.signals) * 100
                print(f"Sell signals: {sell_pct:.1f}%")
        
        print(f"{'='*60}\n")
