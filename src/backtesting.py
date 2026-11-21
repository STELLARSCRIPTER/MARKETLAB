import pandas as pd
import numpy as np

def generate_ewma_strategy(df: pd.DataFrame, alpha: float = 0.06, window: int = 50, tc: float = 0.0001) -> pd.DataFrame:
    """Generates the EWMA volatility-targeting strategy."""
    df = df.copy()
    
    # 1. EWMA Volatility
    df['EWMA_Vol'] = df['Daily_Return'].ewm(alpha=alpha, adjust=False).std() * np.sqrt(252)
    
    # 2. Signal & Position
    df['Vol_Threshold'] = df['EWMA_Vol'].rolling(window=window).median()
    df['Signal'] = np.where(df['EWMA_Vol'] < df['Vol_Threshold'], 1, 0)
    
    # Shift signal to represent the ACTUAL position held today
    df['Position'] = df['Signal'].shift(1)
    
    # 3. Returns & Aligned Transaction Costs
    df['Strategy_Return'] = df['Position'] * df['Daily_Return']
    df['Trade_Change'] = df['Position'].diff().abs()
    df['TC'] = df['Trade_Change'] * tc
    df['Net_Strategy_Return'] = df['Strategy_Return'] - df['TC']
    
    return df.dropna()

def analyze_drawdown_metrics(cumulative_returns: pd.Series, label: str):
    """
    Calculates rigorous drawdown metrics: Depth, Time to Trough, Recovery Duration, Total Underwater.
    """
    rolling_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns / rolling_max) - 1
    
    # Identify when we hit a new high water mark
    is_new_high = cumulative_returns == rolling_max
    high_water_dates = cumulative_returns[is_new_high].index
    
    is_underwater = drawdown < 0
    underwater_groups = (is_underwater != is_underwater.shift()).cumsum()
    
    results = []
    
    for group_id, group_data in drawdown.groupby(underwater_groups):
        if not (group_data < 0).any():
            continue
            
        # The start of this underwater period
        underwater_start_date = group_data.index[0]
        
        # Find the actual Peak Date: the most recent High Water Mark BEFORE this period
        prior_highs = high_water_dates[high_water_dates < underwater_start_date]
        peak_date = prior_highs[-1] if len(prior_highs) > 0 else underwater_start_date
        
        trough_date = group_data.idxmin()
        max_depth = group_data.min()
        
        # Find recovery date (if any)
        post_drawdown = drawdown.loc[trough_date:]
        recovered_days = post_drawdown[post_drawdown >= 0]
        
        if len(recovered_days) > 0:
            recovery_date = recovered_days.index[0]
            total_underwater = (recovery_date - peak_date).days
            recovery_duration = (recovery_date - trough_date).days
        else:
            recovery_date = None
            total_underwater = np.nan # Right-censored
            recovery_duration = np.nan
            
        time_to_trough = (trough_date - peak_date).days
        
        results.append({
            'peak_date': peak_date,
            'trough_date': trough_date,
            'max_depth': max_depth,
            'time_to_trough': time_to_trough,
            'recovery_duration': recovery_duration,
            'total_underwater': total_underwater,
            'is_recovered': recovery_date is not None
        })
        
    df_results = pd.DataFrame(results)
    
    print(f"=== {label.upper()} DRAWDOWN PROFILE ===")
    if df_results.empty:
        print("No drawdowns found.\n")
        return df_results
        
    deepest = df_results.loc[df_results['max_depth'].idxmin()]
    print(f"Deepest Drawdown: {deepest['max_depth']*100:.2f}%")
    print(f"  Time to Trough:    {deepest['time_to_trough']} calendar days")
    
    if deepest['is_recovered']:
        print(f"  Recovery Duration: {deepest['recovery_duration']} calendar days")
        print(f"  Total Underwater:  {deepest['total_underwater']} calendar days")
    else:
        print(f"  Status:            UNRECOVERED at end of sample.")
        
    longest = df_results.dropna(subset=['total_underwater'])
    if not longest.empty:
        max_duration = longest['total_underwater'].max()
        print(f"Longest Completed Underwater Period: {max_duration} calendar days")
    print("\n")
    
    return df_results