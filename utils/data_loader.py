from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd


@dataclass
class Holding:
    symbol: str
    amount: float
    cost_basis_usd: float


def load_holdings(csv_path: Path) -> pd.DataFrame:
    """Load holdings CSV into a DataFrame with proper dtypes."""
    if not csv_path.is_file():
        raise FileNotFoundError(f"Holdings file not found: {csv_path}")
    df = pd.read_csv(csv_path, dtype={"symbol": str})
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["cost_basis_usd"] = pd.to_numeric(df["cost_basis_usd"], errors="coerce")
    if df.isnull().any().any():
        raise ValueError("Holdings CSV contains invalid numeric values.")
    return df


def load_price_history(csv_path: Path) -> pd.DataFrame:
    """Load price history CSV and parse dates."""
    if not csv_path.is_file():
        raise FileNotFoundError(f"Price history file not found: {csv_path}")
    df = pd.read_csv(csv_path, parse_dates=["date"])
    numeric_cols = ["open", "high", "low", "close", "volume"]
    for col in numeric_cols:
# rewrote this part
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if df[numeric_cols].isnull().any().any():
        raise ValueError("Price history CSV contains invalid numeric values.")
    return df


# rewrote this part
def compute_portfolio_metrics(
    holdings: pd.DataFrame, price_history: pd.DataFrame
) -> Dict:
    """Calculate total value, per‑asset P/L and other useful metrics."""
    # Latest closing price per symbol
    latest_prices = (
        price_history.sort_values("date")
        .groupby("symbol")["close"]
        .last()
        .rename("latest_close")
    )
    df = holdings.merge(latest_prices, left_on="symbol", right_index=True, how="left")
    if df["latest_close"].isnull().any():
        missing = df[df["latest_close"].isnull()]["symbol"].tolist()
        raise ValueError(f"Missing price data for symbols: {missing}")

    df["current_value_usd"] = df["amount"] * df["latest_close"]
    df["profit_loss_usd"] = df["current_value_usd"] - df["cost_basis_usd"]
    total_value = df["current_value_usd"].sum()
    profit_loss = dict(zip(df["symbol"], df["profit_loss_usd"]))

    return {
        "total_value": total_value,
        "profit_loss": profit_loss,
        "detailed": df,
    }