import pandas as pd
import numpy as np

def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0) -> float:
    """Calculates annualized Sharpe Ratio."""
    return (returns.mean() - risk_free_rate) / returns.std() * np.sqrt(252)

def calculate_max_drawdown(cumulative_returns: pd.Series) -> float:
    """Calculates maximum drawdown."""
    rolling_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns / rolling_max) - 1
    return drawdown.min()