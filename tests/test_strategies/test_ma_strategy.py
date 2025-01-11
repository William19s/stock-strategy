import pytest
import pandas as pd
from src.strategies.ma_strategy import MAStrategy

def test_ma_strategy_initialization():
    strategy = MAStrategy("sh.600000", 20, 50)
    assert strategy.short_window == 20
    assert strategy.long_window == 50
    assert strategy.name == "MA Strategy"

def test_validate_parameters():
    strategy = MAStrategy("sh.600000", 20, 50)
    assert strategy.validate_parameters() == True
    
    strategy = MAStrategy("sh.600000", 50, 20)
    assert strategy.validate_parameters() == False 