import numpy as np

def ewma_volatility(returns: np.ndarray, alpha: float = 0.06) -> np.ndarray:
    """Calculates EWMA volatility (RiskMetrics standard)."""
    return np.sqrt(np.exp(np.log(returns ** 2).ewm(alpha=alpha, adjust=False).mean()))