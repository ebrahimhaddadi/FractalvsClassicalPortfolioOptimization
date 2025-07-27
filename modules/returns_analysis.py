# modules/returns_analysis.py

import numpy as np

def compute_log_returns(price_df):
    """
    محاسبه بازده لگاریتمی روزانه
    """
    return np.log(price_df / price_df.shift(1)).dropna()
# modules/returns_analysis.py

def compute_cumulative_returns(returns_df):
    """
    محاسبه بازده تجمعی (برای نمودار خطی)
    """
    return (1 + returns_df).cumprod()
