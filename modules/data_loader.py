# modules/data_loader.py

import yfinance as yf
import pandas as pd

def fetch_data(tickers, start, end):
    """
    دریافت قیمت‌های تاریخی از Yahoo Finance
    """
    data = yf.download(tickers, start=start, end=end)
    if 'Adj Close' in data.columns:
        data = data['Adj Close']
    else:
        data = data['Close']
    return data.dropna()
