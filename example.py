import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def calculate_score(srs, N=25):
    """Return 10,000 times the slope of normalized prices times R squared."""
    if srs.shape[0] < N:
        return np.nan
    x = np.arange(1, N + 1)
    y = srs.values / srs.values[0]
    lr = LinearRegression().fit(x.reshape(-1, 1), y)
    slope = lr.coef_[0]
    r_squared = lr.score(x.reshape(-1, 1), y)
    score = 10000 * slope * r_squared
    return score

if __name__ == "__main__":
    score = calculate_score(pd.Series(np.arange(100., 125.)))
    assert np.isclose(score, 100.)
    print(f"Trend score: {score:.2f}")
