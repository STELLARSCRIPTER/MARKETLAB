import pandas as pd
import numpy as np

def ewma_volatility(returns: pd.Series, alpha: float = 0.06) -> pd.Series:
    """Calculates EWMA volatility (RiskMetrics standard)."""
    # Ensure it's a pandas Series so .ewm() works
    if isinstance(returns, np.ndarray):
        returns = pd.Series(returns)
    
    # Calculate variance, then take square root
    ewma_var = (returns ** 2).ewm(alpha=alpha, adjust=False).mean()
    return np.sqrt(ewma_var) * np.sqrt(252)