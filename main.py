
from modules.data_loader import fetch_data
from modules.returns_analysis import compute_log_returns, compute_cumulative_returns
from modules.hurst_analysis import calculate_hurst_exponents
from modules.optimizer import markowitz_optimization, fractal_allocation
from modules.visualizer import plot_portfolio_weights, plot_stacked_weights
from modules.utils import print_section
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def portfolio_returns(weights, returns_df):
    return returns_df @ weights

def variation_coefficient(series):
    mean = np.mean(series)
    std = np.std(series)
    return std / mean if mean != 0 else None

def main():
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA',
        'INTC', 'ORCL', 'IBM', 'ADBE', 'NFLX', 'CRM', 'CSCO'
    ]
    start = '2012-01-01'
    end = '2024-01-01'

    os.makedirs("outputs/figures", exist_ok=True)
    os.makedirs("outputs/tables", exist_ok=True)

    print_section("دریافت داده‌های قیمتی")
    prices = fetch_data(tickers, start, end)
    print(prices.head())

    print_section("محاسبه بازده روزانه")
    returns = compute_log_returns(prices)
    print(returns.head())

    print_section("محاسبه وزن‌های پرتفو به‌صورت ماهانه")
    monthly_weights = []
    for date in returns.index[::21]:
        subset = returns.loc[:date].tail(60)
        if subset.shape[0] < 30:
            continue
        w = markowitz_optimization(subset)
        row = w.to_dict()
        row['Date'] = date
        monthly_weights.append(row)

    weights_df = pd.DataFrame(monthly_weights)
    if 'Date' in weights_df.columns:
        weights_df = weights_df.set_index('Date')
    else:
        print("❌ خطا: ستونی با نام 'Date' در weights_df یافت نشد.")
        weights_df = pd.DataFrame()

    print_section("محاسبه Hurst Exponent")
    hursts = calculate_hurst_exponents(returns)
    for k, v in hursts.items():
        if v is not None:
            print(f"{k}: {v:.4f}")
        else:
            print(f"{k}: محاسبه نشد")

    print_section("پرتفوی Markowitz")
    weights_markowitz = markowitz_optimization(returns)
    print(weights_markowitz)

    print_section("پرتفوی فراکتالی (بر پایه Hurst)")
    filtered_hursts = {k: v for k, v in hursts.items() if v is not None}
    if len(filtered_hursts) == 0:
        print("❌ هیچ مقدار معتبری از Hurst برای پرتفوی فراکتالی وجود ندارد.")
        weights_fractal = pd.Series([1 / len(tickers)] * len(tickers), index=tickers)
    else:
        weights_fractal = fractal_allocation(filtered_hursts)
    print(weights_fractal)

    print_section("نمودار مقایسه‌ای وزن پرتفوی‌ها")
    aligned_assets = [t for t in tickers if t in weights_markowitz.index and t in weights_fractal.index]
    df = pd.DataFrame({
        'Markowitz': weights_markowitz[aligned_assets],
        'Fractal': weights_fractal[aligned_assets]
    }).T
    df.plot(kind='bar', stacked=True, colormap='tab20', figsize=(10, 5))
    plt.title("Portfolio Weights Comparison")
    plt.ylabel("Weight")
    plt.tight_layout()
    plt.savefig("outputs/figures/weights_comparison.png")
    plt.close()

    print_section("ترسیم بازده تجمعی")
    common_assets = [a for a in returns.columns if a in weights_fractal.index]
    aligned_returns = returns[common_assets]
    aligned_weights_fractal = weights_fractal[common_assets]

    returns_markowitz = portfolio_returns(weights_markowitz, returns)
    returns_fractal = portfolio_returns(aligned_weights_fractal, aligned_returns)

    cumulative_m = compute_cumulative_returns(returns_markowitz)
    cumulative_f = compute_cumulative_returns(returns_fractal)

    plt.figure(figsize=(10, 5))
    plt.plot(cumulative_m, label='Markowitz', linestyle='--')
    plt.plot(cumulative_f, label='Fractal', linestyle='-')
    plt.title("Cumulative Portfolio Returns")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("outputs/figures/cumulative_returns.png")
    plt.close()

    print_section("نمودار تجمعی به تفکیک")
    df = pd.DataFrame({
        'Fractal': cumulative_f,
        'Markowitz': cumulative_m
    })
    df.to_csv("outputs/tables/cumulative_comparison.csv")

    fig, ax = plt.subplots(figsize=(12, 6))
    df.plot(ax=ax)
    ax.set_title("Cumulative Returns: Fractal vs Markowitz")
    ax.set_ylabel("Cumulative Return")
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("outputs/figures/figure_fractal_vs_markowitz_curve.png")
    plt.close()

    print_section("محاسبه ضریب تغییرات برای Table 5")
    valid_assets_for_table = [t for t in tickers if t in returns.columns]
    table5 = pd.DataFrame({
        'VC_Fractal': [variation_coefficient(returns[t] * weights_fractal.get(t, 0)) for t in valid_assets_for_table],
        'VC_Markowitz': [variation_coefficient(returns[t] * weights_markowitz.get(t, 0)) for t in
                         valid_assets_for_table]
    }, index=valid_assets_for_table)
    table5['Lower VC'] = np.where(table5['VC_Fractal'] < table5['VC_Markowitz'], 'Fractal', 'Markowitz')
    table5.to_csv("outputs/tables/table5_variation_coefficients.csv")
    print(table5)

    if not weights_df.empty:
        print_section("نمودار stacked weights")
        plt.figure(figsize=(12, 6))
        plt.stackplot(weights_df.index, weights_df.T.values, labels=weights_df.columns)
        plt.title("Portfolio Weights Over Time")
        plt.ylabel("Weight")
        plt.ylim(0, 1)
        plt.legend(loc='upper left', ncol=3)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.savefig("outputs/figures/stacked_weights.png")
        plt.close()

        print_section("نمودار سه‌بعدی بازده در زمان")
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        X = np.arange(len(weights_df.columns))
        Y = mdates.date2num(weights_df.index)
        X, Y = np.meshgrid(X, Y)
        Z = weights_df.values
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.set_xticks(np.arange(len(weights_df.columns)))
        ax.set_xticklabels(weights_df.columns, rotation=90)
        # ax.set_yticklabels([d.strftime('%Y') for d in weights_df.index[::max(1,len(weights_df)//10)]])
        ytick_locs = weights_df.index[::max(1, len(weights_df) // 10)]
        ytick_vals = mdates.date2num(ytick_locs)
        ax.set_yticks(ytick_vals)
        ax.set_yticklabels([d.strftime('%Y') for d in ytick_locs])

        ax.set_xlabel("Asset")
        ax.set_ylabel("Year")
        ax.set_zlabel("Weight")
        plt.tight_layout()
        plt.savefig("outputs/figures/3d_weights_surface.png")
        plt.close()

if __name__ == "__main__":
    main()
