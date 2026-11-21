# MARKETLAB: Financial Market Behaviour & Predictability Research

**Quantitative Research Report**

## 1. Executive Summary
This project investigated whether historical market information reveals statistically meaningful patterns in future financial market behaviour, and whether those patterns survive on unseen data. We tested six experiments across a 2015–2024 dataset of SPY, QQQ, IWM, TLT, and GLD. 

Our findings confirmed that while daily returns are largely unpredictable (Experiment C), volatility exhibits strong clustering (Experiment A). By exploiting this clustering (Experiment B), we built a strategy that successfully improved risk-adjusted returns and drastically reduced drawdown durations out-of-sample (Experiments E & F).

The results indicate that daily returns exhibit limited linear predictability in the tested experiments, while volatility demonstrates statistically significant clustering. The EWMA volatility model provided useful out-of-sample volatility estimates. A volatility-filtered SPY strategy also showed improved historical risk-adjusted performance and lower maximum drawdown than Buy & Hold during the selected 2022–2024 test period. These findings are specific to the tested assets, sample and execution assumptions and require further validation.

## 2. Dataset & Methodology
- **Data:** Daily OHLCV and Adjusted Close for 5 liquid ETFs (SPY, QQQ, IWM, TLT, GLD) spanning 2015–2024.
- **Validation:** Strict chronological train/test split (Train: 2015–2021, Test: 2022–2024) to prevent look-ahead bias.
- **Rigor:** All complex models were compared against naive baselines. Transaction costs (1 basis point) were explicitly included in the backtest.

## 3. The Experiments

### A. Return Behaviour
- **Methodology:** Jarque-Bera, Ljung-Box, ARCH tests.
- **Result:** Daily returns exhibited significant deviations from normality across all five ETFs. The Ljung–Box test detected statistically significant autocorrelation at lag 10 in SPY, QQQ, IWM and TLT, while GLD showed no statistically significant autocorrelation at the tested lag. ARCH tests provided strong evidence of conditional heteroskedasticity across all five assets, supporting further investigation of volatility models such as GARCH.

### B. Volatility Prediction (H1)
- **Methodology:** Rolling Baseline, EWMA, GARCH(1,1) walk-forward validation.
- **Result:** EWMA was the best predictor out-of-sample (MAE: 0.0363). While GARCH(1,1) is mathematically more complex, its rolling re-estimation overfitted to recent noise. EWMA generalized better, proving that complexity does not always equal superiority.

### C. Momentum & Return Predictability
- **Methodology:** Linear, Ridge, Random Forest models using 5/10/20-day momentum features.
- **Result:** All models failed out-of-sample (R² < 0). Momentum features could not predict 5-day forward returns in SPY. The naive baseline (historical mean) was the strongest predictor. We honestly reject the momentum hypothesis.

### D. Cross-Asset Relationships
- **Methodology:** Rolling 63-day correlations.
- **Result:** Correlations are not static. The SPY-TLT hedge broke down in 2022 (correlation flipped from -0.32 to +0.07). The changing correlations indicate that historical diversification relationships can vary across market periods. Portfolio construction should therefore consider the possibility of changing cross-asset relationships rather than assuming correlations remain constant.

### E. Strategy Validation
- **Methodology:** Long SPY if EWMA Vol < 50-day median; otherwise Cash. 1 bps transaction costs.
- **Result:** The EWMA volatility-filtered strategy demonstrated improved historical risk-adjusted performance and lower maximum drawdown relative to Buy & Hold during the selected out-of-sample period (2022–2024). However, these results are specific to the tested asset and period. Further validation across different market regimes, transaction-cost assumptions, slippage and alternative assets is required before establishing the robustness or economic significance of the strategy.

### F. Drawdown Profile Analysis
- **Methodology:** Analysis of underwater equity curves to measure maximum drawdown depth, time to trough, recovery duration and total underwater duration. Durations are measured in calendar days.
- **Result:** 
  - **Buy & Hold:** Deepest drawdown of **-24.50%**. Time to trough was 282 days, with a recovery duration of 427 days, resulting in a longest total underwater period of **709 calendar days**.
  - **EWMA Strategy:** Deepest drawdown of **-11.10%**. Time to trough was 67 days, with a recovery duration of 63 days, resulting in a total underwater period of **130 calendar days** for its deepest drawdown. The longest completed underwater period for the strategy was **170 calendar days**.

The results compare the historical severity and duration of drawdowns under the two approaches. Unrecovered drawdowns at the end of the sample are treated as right-censored and are not assigned a completed recovery duration.

## 4. Limitations & Future Work
- **Data Limitations:** Free Yahoo Finance data may contain minor adjusted-price anomalies or missing ticks.
- **Execution Assumptions:** The backtest assumes perfect liquidity at the daily close price. It does not model market impact or slippage beyond the 1 bps fee.
- **Future Work:** Transition to high-frequency Limit Order Book (LOB) data to model adverse selection. Furthermore, implement Bayesian online updating for real-time regime detection rather than rolling windows.

## 5. Conclusion
Historical volatility demonstrated measurable persistence in the tested ETF data, while the return-prediction experiments did not establish reliable out-of-sample momentum predictability.

The EWMA volatility-filtered strategy showed improved historical risk-adjusted performance and lower drawdown severity than the Buy & Hold benchmark during the selected 2022–2024 evaluation period. These findings do not establish future profitability or universal robustness.

The project demonstrates a quantitative research workflow built around hypothesis formulation, falsification, out-of-sample validation and honest reporting of negative results.