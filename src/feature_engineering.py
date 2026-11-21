import pandas as pd
import numpy as np

def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates daily returns from adjusted close."""
    df['Daily_Return'] = df['Adj Close'].pct_change()
    return df.dropna()

def calculate_rolling_volatility(df: pd.DataFrame, window: int = 21) -> pd.Series:
    """Calculates annualized rolling volatility."""
    return df['Daily_Return'].rolling(window=window).std() * np.sqrt(252)