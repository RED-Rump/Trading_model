"""
Data Collection Module
Handles downloading, caching, and preprocessing market data
"""

import yfinance as yf
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import pickle

class DataCollector:
    """
    Handles market data collection and preprocessing
    """
    
    def __init__(self, cache_dir='data/data_cache', use_cache=True):
        """
        Initialize data collector
        
        Parameters:
        -----------
        cache_dir : str
            Directory to cache downloaded data
        use_cache : bool
            Whether to use cached data if available
        """
        self.cache_dir = cache_dir
        self.use_cache = use_cache
        self.data = {}
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def fetch_data(self, tickers, start_date, end_date, data_type='Adj Close'):
        """
        Download historical data for given tickers
        
        Parameters:
        -----------
        tickers : list or str
            Ticker symbol(s)
        start_date : str
            Start date in 'YYYY-MM-DD' format
        end_date : str
            End date in 'YYYY-MM-DD' format
        data_type : str
            Type of data to fetch ('Adj Close', 'Close', 'Volume', etc.)
            
        Returns:
        --------
        pd.DataFrame
            Price data with tickers as columns
        """
        # Convert single ticker to list
        if isinstance(tickers, str):
            tickers = [tickers]
        
        print(f"\n{'='*60}")
        print(f"FETCHING DATA FOR {len(tickers)} ASSET(S)")
        print(f"{'='*60}")
        print(f"Date Range: {start_date} to {end_date}")
        print(f"Data Type: {data_type}\n")
        
        all_data = {}
        
        for ticker in tickers:
            # Check cache first
            cache_file = self._get_cache_filename(ticker, start_date, end_date, data_type)
            
            if self.use_cache and os.path.exists(cache_file):
                print(f"  ✓ {ticker}: Loading from cache")
                with open(cache_file, 'rb') as f:
                    all_data[ticker] = pickle.load(f)
            else:
                # Download data
                try:
                    print(f"  ⬇ {ticker}: Downloading...", end='')
                    df = yf.download(ticker, start=start_date, end=end_date, 
                                    progress=False)
                    
                    if len(df) == 0:
                        print(f" ✗ No data available")
                        continue
                    if isinstance(df, pd.Series):
                       data_series = df[data_type]
                    elif data_type in df.columns:
                       data_series = df[data_type]
                    else:
                        # Fallback to Close column
                       data_series = df['Close'] if 'Close' in df.columns else df.iloc[:, 0]
                    all_data[ticker] = data_series
                    
                    # Cache the data
                    with open(cache_file, 'wb') as f:
                        pickle.dump(data_series, f)
                    
                    print(f" ✓ {len(df)} rows")
                    
                except Exception as e:
                    print(f" ✗ Error: {e}")
                    continue
        
        # Combine into DataFrame
        if len(all_data) == 0:
            raise ValueError("No data was successfully downloaded")

        # Combine into DataFrame, ensuring proper alignment
        self.price_data = pd.concat(all_data, axis=1)
        self.price_data.columns = list(all_data.keys())
        
        print(f"\n{'='*60}")
        print(f"✓ Data fetched successfully")
        print(f"  Shape: {self.price_data.shape}")
        print(f"  Date range: {self.price_data.index[0]} to {self.price_data.index[-1]}")
        print(f"{'='*60}\n")
        
        return self.price_data
    
    def clean_data(self, method='ffill'):
        """
        Clean data by handling missing values
        
        Parameters:
        -----------
        method : str
            Method to handle missing values ('ffill', 'bfill', 'drop')
            
        Returns:
        --------
        pd.DataFrame
            Cleaned price data
        """
        print("Cleaning data...")
        
        # Check for missing values
        missing_before = self.price_data.isnull().sum()
        total_missing = missing_before.sum()
        
        if total_missing > 0:
            print(f"  Missing values found: {total_missing}")
            print(f"  {missing_before[missing_before > 0]}\n")
        
        if method == 'ffill':
            self.price_data = self.price_data.ffill().bfill()
        elif method == 'bfill':
            self.price_data = self.price_data.bfill().ffill()
        elif method == 'drop':
            self.price_data = self.price_data.dropna()
        
        # Final check
        remaining_missing = self.price_data.isnull().sum().sum()
        if remaining_missing > 0:
            print(f"  ⚠ Warning: {remaining_missing} missing values remain")
            print("  Dropping rows with missing values...")
            self.price_data = self.price_data.dropna()
        
        print(f"  ✓ Data cleaned. Final shape: {self.price_data.shape}\n")
        
        return self.price_data
    
    def calculate_returns(self, method='simple'):
        """
        Calculate returns from price data
        
        Parameters:
        -----------
        method : str
            'simple' for simple returns, 'log' for log returns
            
        Returns:
        --------
        pd.DataFrame
            Daily returns
        """
        if method == 'simple':
            self.returns = self.price_data.pct_change().dropna()
        elif method == 'log':
            self.returns = np.log(self.price_data / self.price_data.shift(1)).dropna()
        
        print(f"✓ Returns calculated ({method}). Shape: {self.returns.shape}\n")
        
        return self.returns
    
    def get_summary_stats(self):
        """
        Display summary statistics
        
        Returns:
        --------
        dict
            Dictionary containing summary statistics
        """
        stats = {
            'price': self.price_data.describe(),
            'returns': self.returns.describe() if hasattr(self, 'returns') else None
        }
        
        print("\n" + "="*70)
        print("PRICE DATA SUMMARY STATISTICS")
        print("="*70)
        print(stats['price'])
        
        if stats['returns'] is not None:
            print("\n" + "="*70)
            print("RETURNS SUMMARY STATISTICS")
            print("="*70)
            print(stats['returns'])
            
            print("\n" + "="*70)
            print("ANNUALIZED METRICS")
            print("="*70)
            annual_return = stats['returns'].loc['mean'] * 252
            annual_vol = stats['returns'].loc['std'] * np.sqrt(252)
            sharpe = annual_return / annual_vol
            
            metrics_df = pd.DataFrame({
                'Annual Return': annual_return,
                'Annual Volatility': annual_vol,
                'Sharpe Ratio': sharpe
            })
            print(metrics_df)
        
        print("="*70 + "\n")
        
        return stats
    
    def _get_cache_filename(self, ticker, start_date, end_date, data_type):
        """Generate cache filename"""
        safe_data_type = data_type.replace(' ', '_')
        filename = f"{ticker}_{start_date}_{end_date}_{safe_data_type}.pkl"
        return os.path.join(self.cache_dir, filename)
    
    def clear_cache(self):
        """Clear all cached data"""
        if os.path.exists(self.cache_dir):
            for file in os.listdir(self.cache_dir):
                os.remove(os.path.join(self.cache_dir, file))
            print("✓ Cache cleared")

if __name__ == '__main__':
    # Example usage
    collector = DataCollector()
    
    # Download data
    tickers = ['SPY', 'QQQ', 'GLD']
    prices = collector.fetch_data(tickers, '2020-01-01', '2024-12-31')
    
    # Clean data
    prices = collector.clean_data()
    
    # Calculate returns
    returns = collector.calculate_returns()
    
    # Show summary stats
    stats = collector.get_summary_stats()
