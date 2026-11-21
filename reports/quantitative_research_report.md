# MARKETLAB: Financial Market Behaviour & Predictability Research

**Quantitative Research Report**

## 1. Executive Summary
This project investigated whether historical market information reveals statistically meaningful patterns in future financial market behaviour, and whether those patterns survive on unseen data. We tested six experiments across a 2015–2024 dataset of SPY, QQQ, IWM, TLT, and GLD. 

Our findings confirmed that while daily returns are largely unpredictable (Experiment C), volatility exhibits strong clustering (Experiment A). By exploiting this clustering (Experiment B), we built a strategy that successfully improved risk-adjusted returns and drastically reduced drawdown durations out-of-sample (Experiments E & F).

## 2. Dataset & Methodology
- **Data:** Daily OHLCV and Adjusted Close for 5 liquid ETFs (SPY, QQQ, IWM, TLT, GLD) spanning 2015–2024.
- **Validation:** Strict chronological train/test split (Train: 2015–2021, Test: 2022–2024) to prevent look-ahead bias.
- **Rigor:** All complex models were compared against naive baselines. Transaction costs (1 basis point) were explicitly included in the backtest.

## 3. The Experiments

### A. Return Behaviour
- **Methodology:** Jarque-Bera, Ljung-Box, ARCH tests.
- **Result:** Returns are heavily non-normal (fat tails). Volatility clusters strongly (ARCH effects p-value ≈ 0). This provided the statistical foundation to predict volatility.

### B. Volatility Prediction (H1)
- **Methodology:** Rolling Baseline, EWMA, GARCH(1,1) walk-forward validation.
- **Result:** EWMA was the best predictor out-of-sample (MAE: 0.0363). While GARCH(1,1) is mathematically more complex, its rolling re-estimation overfitted to recent noise. EWMA generalized better, proving that complexity does not always equal superiority.

### C. Momentum & Return Predictability
- **Methodology:** Linear, Ridge, Random Forest models using 5/10/20-day momentum features.
- **Result:** All models failed out-of-sample (R² < 0). Momentum features could not predict 5-day forward returns in SPY. The naive baseline (historical mean) was the strongest predictor. We honestly reject the momentum hypothesis.

### D. Cross-Asset Relationships
- **Methodology:** Rolling 63-day correlations.
- **Result:** Correlations are not static. The SPY-TLT hedge broke down in 2022 (correlation flipped from -0.32 to +0.07). Regime-aware hedging is strictly necessary for portfolio construction.

### E. Strategy Validation
- **Methodology:** Long SPY if EWMA Vol < 50-day median; otherwise Cash. 1 bps transaction costs.
- **Result:** The EWMA strategy outperformed Buy & Hold out-of-sample (2022-2024) with a Sharpe Ratio of **0.84** (vs 0.57) and Max Drawdown of **-11.1%** (vs -24.5%). It generated a higher total return (31.1% vs 28.9%) with only 34 trades over 3 years.

### F. Drawdown Topology Analysis
- **Methodology:** Analysis of underwater equity curves to measure duration and depth of capital loss.
- **Result:** Buy & Hold suffered a maximum depth of -24.50% lasting **488 trading days** (nearly two years). The EWMA Strategy suffered a maximum depth of -11.11% lasting only **116 trading days**. The volatility filter successfully cut the drawdown duration by 76%.

## 4. Limitations & Future Work
- **Data Limitations:** Free Yahoo Finance data may contain minor adjusted-price anomalies or missing ticks.
- **Execution Assumptions:** The backtest assumes perfect liquidity at the daily close price. It does not model market impact or slippage beyond the 1 bps fee.
- **Future Work:** Transition to high-frequency Limit Order Book (LOB) data to model adverse selection. Furthermore, implement Bayesian online updating for real-time regime detection rather than rolling windows.

## 5. Conclusion
Historical volatility is a persistent, predictable feature of financial markets. By utilizing a simple, robust EWMA model, we demonstrated that quantitative strategies can successfully navigate market regimes and protect capital without overfitting to noise. The project validates the research pipeline: hypothesis → falsification attempt → evidence → honest conclusion.