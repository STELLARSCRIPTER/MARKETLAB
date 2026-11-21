import os
import pandas as pd
import numpy as np
import yfinance as yf
from pathlib import Path

# Define the research universe exactly as specified
TICKERS = ["SPY", "QQQ", "IWM", "TLT", "GLD"]
START_DATE = "2015-01-01"
END_DATE = "2025-01-01"

# Set up directory paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

def ensure_directories():
    """Create data directories if they don't exist."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Directories ensured at {RAW_DIR} and {PROCESSED_DIR}")

def download_data(tickers: list, start: str, end: str) -> pd.DataFrame:
    """
    Step 01: Data Acquisition.
    Downloads historical data using yfinance.
    """
    print(f"Downloading data for {tickers} from {start} to {end}...")
    
    # Download all tickers at once (auto_adjust=False keeps raw and adj close separate)
    df = yf.download(tickers, start=start, end=end, group_by='ticker', auto_adjust=False)
    
    if df.empty:
        raise ValueError("Downloaded dataframe is empty. Check internet connection or yfinance API.")
        
    return df

def validate_and_process_data(df: pd.DataFrame, tickers: list) -> pd.DataFrame:
    """
    Step 02: Data Preparation.
    Cleans, validates, handles missing values, and calculates daily returns.
    """
    print("Validating and processing data...")
    processed_data = {}
    
    for ticker in tickers:
        if ticker not in df.columns.levels[0]:
            print(f"Warning: {ticker} not found in downloaded data.")
            continue
            
        ticker_df = df[ticker].copy()
        
        # 1. Check for duplicates in the index
        if ticker_df.index.duplicated().any():
            print(f"[{ticker}] Found duplicate dates. Removing...")
            ticker_df = ticker_df[~ticker_df.index.duplicated(keep='first')]
            
        # 2. Check for missing values (NaN)
        missing_counts = ticker_df.isna().sum()
        if missing_counts.any():
            print(f"[{ticker}] Missing values found: {missing_counts.to_dict()}")
            # Forward fill is standard for missing trading days/price gaps
            ticker_df = ticker_df.ffill()
            
        # 3. Drop any leading NaNs (before the first valid data point)
        ticker_df = ticker_df.dropna()
        
        # 4. Calculate Daily Returns using Adjusted Close
        # Formula: (P_t / P_{t-1}) - 1
        ticker_df['Daily_Return'] = ticker_df['Adj Close'].pct_change()
        
        # Drop the first row since Daily_Return will be NaN
        ticker_df = ticker_df.dropna()
        
        # 5. Basic Validation checks
        if (ticker_df['Adj Close'] <= 0).any():
            print(f"[{ticker}] WARNING: Found zero or negative prices!")
        if (ticker_df['Volume'] < 0).any():
            print(f"[{ticker}] WARNING: Found negative volume!")
            
        print(f"[{ticker}] Validated. Shape: {ticker_df.shape}. "
              f"Start: {ticker_df.index.min().date()}, End: {ticker_df.index.max().date()}")
              
        processed_data[ticker] = ticker_df

    return processed_data

def save_data(raw_df: pd.DataFrame, processed_dict: dict):
    """Saves raw and processed data to disk."""
    # Save raw multi-index dataframe
    raw_path = RAW_DIR / "raw_market_data.csv"
    raw_df.to_csv(raw_path)
    print(f"Raw data saved to {raw_path}")
    
    # Save processed data for each ticker
    for ticker, t_df in processed_dict.items():
        processed_path = PROCESSED_DIR / f"{ticker}_processed.csv"
        t_df.to_csv(processed_path)
        print(f"Processed data for {ticker} saved to {processed_path}")

def run_pipeline():
    """Main execution function."""
    ensure_directories()
    
    # 1. Acquisition
    raw_df = download_data(TICKERS, START_DATE, END_DATE)
    
    # 2. Preparation
    processed_dict = validate_and_process_data(raw_df, TICKERS)
    
    # 3. Storage
    save_data(raw_df, processed_dict)
    print("Data pipeline complete.")

if __name__ == "__main__":
    run_pipeline()