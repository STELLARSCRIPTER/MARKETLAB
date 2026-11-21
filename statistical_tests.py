import pandas as pd
from scipy import stats
from statsmodels.stats.diagnostic import het_arch

def test_normality(returns: pd.Series) -> dict:
    """Runs Jarque-Bera test for normality."""
    jb_stat, jb_p = stats.jarque_bera(returns)
    return {"stat": jb_stat, "p_value": jb_p}

def test_arch_effects(returns: pd.Series, lags: int = 5) -> dict:
    """Runs ARCH LM test for volatility clustering."""
    arch_test = het_arch(returns ** 2, nlags=lags)
    return {"lm_stat": arch_test[0], "p_value": arch_test[1]}