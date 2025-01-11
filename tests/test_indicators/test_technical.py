import pytest
import pandas as pd
import numpy as np
from src.indicators.technical import TechnicalIndicators

def test_calculate_ma():
    data = pd.Series([1, 2, 3, 4, 5])
    ti = TechnicalIndicators()
    ma = ti.calculate_ma(data, window=3)
    assert len(ma) == len(data)
    assert ma.iloc[-1] == 4.0  # (3+4+5)/3 