# main.py

from modules.data_loader import fetch_data
from modules.returns_analysis import compute_log_returns, compute_cumulative_returns
from modules.hurst_analysis import calculate_hurst_exponents
from modules.optimizer import markowitz_optimization, fractal_allocation
from modules.visualizer import plot_portfolio_weights
from modules.utils import print_section
import matplotlib.pyplot as plt

def portfolio_returns(weights, returns_df):
    return returns_df @ weights

def main():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    start = '2015-01-01'
    end = '2020-01-01'

    # بخش 1: دریافت داده‌ها
    print_section("دریافت داده‌های قیمتی")
    prices = fetch_data(tickers, start, end)
    print(prices.head())

    # بخش 2: محاسبه بازده
    print_section("محاسبه بازده روزانه")
    returns = compute_log_returns(prices)
    print(returns.head())

    # بخش 3: محاسبه Hurst
    print_section("محاسبه Hurst Exponent")
    hursts = calculate_hurst_exponents(returns)
    for k, v in hursts.items():
        print(f"{k}: {v:.4f}")

    # بخش 4: بهینه‌سازی پرتفوی
    print_section("پرتفوی Markowitz")
    weights_markowitz = markowitz_optimization(returns)
    print(weights_markowitz)

    print_section("پرتفوی فراکتالی (بر پایه Hurst)")
    weights_fractal = fractal_allocation(hursts)
    print(weights_fractal)

    # بخش 5: ترسیم نمودار وزن پرتفوها
    print_section("نمودار مقایسه‌ای وزن پرتفوی‌ها")
    plot_portfolio_weights({
        'Markowitz': weights_markowitz,
        'Fractal': weights_fractal
    })

    # بخش 6: محاسبه بازده تجمعی
    print_section("ترسیم بازده تجمعی")
    returns_markowitz = portfolio_returns(weights_markowitz, returns)
    returns_fractal = portfolio_returns(weights_fractal, returns)

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
    plt.show()

if __name__ == "__main__":
    main()