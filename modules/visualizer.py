# modules/visualizer.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_portfolio_weights(weights_dict):
    """
    ترسیم نمودار مقایسه وزن‌های پرتفوی‌ها
    """
    df = pd.DataFrame(weights_dict).T
    df.plot(kind='bar', stacked=True, figsize=(10, 5), colormap='tab20')
    plt.title('Portfolio Weights Comparison')
    plt.ylabel('Weight')
    plt.xlabel('Portfolio Type')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
def plot_stacked_weights(weights_df):
    """
    ترسیم نمودار stacked area از وزن پرتفو در طول زمان
    """
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
    plt.show()