# modules/hurst_analysis.py

from hurst import compute_Hc

def calculate_hurst_exponents(returns_df):
    hursts = {}
    for col in returns_df.columns:
        try:
            clean_series = returns_df[col].cumsum().dropna()
            H, _, _ = compute_Hc(clean_series, kind='price')
            hursts[col] = H
        except Exception as e:
            print(f"⚠️ خطا در محاسبه Hurst برای {col}: {e}")
            hursts[col] = None
    return hursts
