import tempfile
from pathlib import Path

import pandas as pd
import pytest

from utils.data_loader import load_holdings, load_price_history, compute_portfolio_metrics


@pytest.fixture
def sample_holdings(tmp_path: Path) -> Path:
    csv = tmp_path / "holdings.csv"
    csv.write_text(
        "symbol,amount,cost_basis_usd\n"
        "BTC,0.5,15000\n"
        "ETH,2,4000\n"
    )
    return csv


@pytest.fixture
def sample_price_history(tmp_path: Path) -> Path:
    csv = tmp_path / "price_history.csv"
    csv.write_text(
        "date,symbol,open,high,low,close,volume\n"
        "2024-01-01,BTC,30000,31000,29500,30500,50000\n"
        "2024-01-01,ETH,2000,2100,1950,2050,120000\n"
    )
    return csv


def test_load_holdings(sample_holdings: Path):
    df = load_holdings(sample_holdings)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2
    assert set(df["symbol"]) == {"BTC", "ETH"}


def test_load_price_history(sample_price_history: Path):
    df = load_price_history(sample_price_history)
    assert isinstance(df, pd.DataFrame)
    assert "date" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_compute_metrics(sample_holdings: Path, sample_price_history: Path):
    holdings = load_holdings(sample_holdings)
    price_hist = load_price_history(sample_price_history)
    metrics = compute_portfolio_metrics(holdings, price_hist)

    assert "total_value" in metrics
    assert "profit_loss" in metrics
    # BTC profit = (0.5 * 30500) - 15000 = 15250 - 15000 = 250
    assert round(metrics["profit_loss"]["BTC"], 2) == 250.0
    # ETH profit = (2 * 2050) - 4000 = 4100 - 4000 = 100
    assert round(metrics["profit_loss"]["ETH"], 2) == 100.0