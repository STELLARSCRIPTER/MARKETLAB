import pandas as pd
import numpy as np

def generate_ewma_strategy(df: pd.DataFrame, alpha: float = 0.06, window: int = 50, tc: float = 0.0001) -> pd.DataFrame:
    """
    Generates the EWMA volatility-targeting strategy.
    Handles signal generation, position shifting, and transaction costs consistently.
    """
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
    
    # Isolate drawdown episodes
    is_underwater = drawdown < 0
    underwater_groups = (is_underwater != is_underwater.shift()).cumsum()
    
    results = []
    
    # Iterate through each drawdown group
    for group_id, group_data in drawdown.groupby(underwater_groups):
        if not (group_data < 0).any():
            continue # Skip groups where we aren't underwater
            
        peak_date = group_data.index[0] - pd.Timedelta(days=1) # Approx date of previous peak
        trough_date = group_data.idxmin()
        max_depth = group_data.min()
        
        # Find recovery date (if any)
        recovery_date = None
        post_drawdown = drawdown.loc[trough_date:]
        recovered_days = post_drawdown[post_drawdown >= 0]
        
        if len(recovered_days) > 0:
            recovery_date = recovered_days.index[0]
            total_underwater = (recovery_date - peak_date).days
        else:
            recovery_date = None
            total_underwater = np.nan # Right-censored
            
        time_to_trough = (trough_date - peak_date).days
        
        results.append({
            'max_depth': max_depth,
            'time_to_trough': time_to_trough,
            'recovery_date': recovery_date,
            'total_underwater': total_underwater,
            'trough_date': trough_date,
            'is_recovered': recovery_date is not None
        })
        
    df_results = pd.DataFrame(results)
    
    print(f"=== {label.upper()} DRAWDOWN PROFILE ===")
    if df_results.empty:
        print("No drawdowns found.\n")
        return df_results
        
    deepest = df_results.loc[df_results['max_depth'].idxmin()]
    print(f"Deepest Drawdown: {deepest['max_depth']*100:.2f}%")
    print(f"Time to Trough:   {deepest['time_to_trough']} days")
    
    if deepest['is_recovered']:
        print(f"Recovery Duration:{deepest['total_underwater'] - deepest['time_to_trough']} days")
        print(f"Total Underwater: {deepest['total_underwater']} days (Peak to Recovery)")
    else:
        print(f"Status:           UNRECOVERED at end of sample.")
        
    longest = df_results.dropna(subset=['total_underwater'])
    if not longest.empty:
        max_duration = longest['total_underwater'].max()
        print(f"Longest Underwater Period: {max_duration} days")
    print("\n")
    
    return df_results