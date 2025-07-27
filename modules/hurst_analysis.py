from hurst import compute_Hc

def calculate_hurst_exponents(returns_df):
    hursts = {}
    for col in returns_df.columns:
        try:
            series = returns_df[col].cumsum().dropna()
            # حذف مقادیر صفر یا منفی
            series = series[series > 0]

            if len(series) < 100:
                raise ValueError("سری خیلی کوتاه است")

            H, _, _ = compute_Hc(series, kind='price')
            hursts[col] = H
        except Exception as e:
            print(f"⚠️ خطا در محاسبه Hurst برای {col}: {e}")
            hursts[col] = None
    return hursts
