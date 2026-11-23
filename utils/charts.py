from typing import Dict, List

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def plot_portfolio_distribution(holdings: pd.DataFrame) -> go.Figure:
    """Pie chart of portfolio value distribution."""
    df = holdings.copy()
    df["value_usd"] = df["amount"] * (df["cost_basis_usd"] / df["amount"])
    fig = px.pie(
        df,
        names="symbol",
        values="value_usd",
        title="Portfolio Distribution",
        hole=0.4,
    )
    fig.update_traces(textinfo="percent+label")
    return fig


def plot_price_trends(price_history: pd.DataFrame) -> go.Figure:
    """Line chart of closing prices for each symbol."""
    df = price_history.copy()
    fig = px.line(
        df,
        x="date",
        y="close",
        color="symbol",
        title="Price Trends (Closing Prices)",
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
    return fig


def plot_profit_loss(profit_loss: Dict[str, float]) -> go.Figure:
    """Bar chart of profit/loss per asset."""
    df = pd.DataFrame(
        list(profit_loss.items()), columns=["symbol", "pnl_usd"]
    )
    fig = px.bar(
        df,
        x="symbol",
        y="pnl_usd",
        color="pnl_usd",
        title="Profit / Loss by Asset",
        color_continuous_scale=px.colors.sequential.Viridis,
    )
    fig.update_layout(yaxis_title="P/L (USD)")
    return fig


def plot_volume_analysis(price_history: pd.DataFrame) -> go.Figure:
    """Stacked area chart of daily volume per asset."""
    df = price_history.copy()
    df_grouped = df.pivot(index="date", columns="symbol", values="volume").fillna(0)
    fig = go.Figure()
    for sym in df_grouped.columns:
        fig.add_trace(
            go.Scatter(
                name=sym,
                x=df_grouped.index,
                y=df_grouped[sym],
                mode="lines",
                stackgroup="one",
            )
        )
    fig.update_layout(
        title="Daily Trading Volume",
        xaxis_title="Date",
        yaxis_title="Volume",
    )
    return fig