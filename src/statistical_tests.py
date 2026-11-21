import pandas as pd
from scipy import stats
from statsmodels.stats.diagnostic import het_arch
import statsmodels.api as sm

def test_normality(returns: pd.Series) -> dict:
    """Runs Jarque-Bera test for normality and returns skewness/kurtosis."""
    skew = stats.skew(returns)
    kurt = stats.kurtosis(returns, fisher=True)
    jb_stat, jb_p = stats.jarque_bera(returns)
    
    return {
        "skewness": skew, 
        "excess_kurtosis": kurt,
        "jb_stat": jb_stat, 
        "p_value": jb_p
    }

def test_autocorrelation(returns: pd.Series, lags: int = 10) -> dict:
    """Runs Ljung-Box test for autocorrelation."""
    lb_test = sm.stats.acorr_ljungbox(returns, lags=[lags], return_df=True)
    return {
        "p_value": lb_test['lb_pvalue'].values[0]
    }

def test_arch_effects(returns: pd.Series, lags: int = 5) -> dict:
    """Runs ARCH LM test for volatility clustering."""
    squared_returns = returns ** 2
    arch_test = het_arch(squared_returns, nlags=lags)
    return {
        "lm_stat": arch_test[0], 
        "p_value": arch_test[1]
    }