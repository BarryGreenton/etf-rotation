"""Cross-sectional rotation using a panel of daily closing prices."""
import argparse
import pandas as pd
from example import calculate_score

def backtest(prices, method):
    if method == "momentum":
        scores = prices.pct_change(21, fill_method=None)
    elif method == "trend":
        scores = prices.rolling(25).apply(calculate_score)
    else:
        raise ValueError("Use momentum or trend")
    winners = scores.dropna().idxmax(axis=1).reindex(prices.index).shift(1)
    returns = prices.pct_change(fill_method=None)
    selected = pd.Series({day: returns.at[day, fund] for day, fund in winners.dropna().items()})
    return pd.DataFrame({"held": winners, "return": selected, "wealth": (1 + selected).cumprod()}).dropna()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="Date in first column, one close-price column per fund")
    parser.add_argument("--method", choices=["momentum", "trend"], default="trend")
    args = parser.parse_args()
    prices = pd.read_csv(args.csv, parse_dates=[0], index_col=0).sort_index()
    print(backtest(prices, args.method).tail())
