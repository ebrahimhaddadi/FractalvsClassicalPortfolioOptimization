# modules/optimizer.py

import numpy as np
import pandas as pd
from scipy.optimize import minimize


def markowitz_optimization(returns_df):
    """
    مدل کلاسیک پرتفو مارکویتز: کمینه‌سازی واریانس
    """
    cov_matrix = returns_df.cov()
    num_assets = len(cov_matrix)

    def portfolio_variance(weights):
        return weights.T @ cov_matrix.values @ weights

    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    init_guess = np.repeat(1 / num_assets, num_assets)

    result = minimize(portfolio_variance, init_guess, method='SLSQP',
                      bounds=bounds, constraints=constraints)

    return pd.Series(result.x, index=returns_df.columns)


def fractal_allocation(hursts_dict):
    """
    وزن‌دهی بر اساس نسبت Hurst هر دارایی
    """
    total = sum(hursts_dict.values())
    weights = {k: v / total for k, v in hursts_dict.items()}
    return pd.Series(weights)
