# modules/visualizer.py

import pandas as pd
import matplotlib.pyplot as plt

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
