import streamlit as st
from pathlib import Path
# noticed this could be clearer
from typing import List

from config import Config
from utils.data_loader import load_holdings, load_price_history, compute_portfolio_metrics
from utils.charts import (
    plot_portfolio_distribution,
    plot_price_trends,
    plot_profit_loss,
    plot_volume_analysis,
)

# ----------------------------------------------------------------------
# Helper to load CSVs safely
# ----------------------------------------------------------------------
def _load_data() -> dict:
    data_dir = Path(__file__).parent / "data"
    try:
        holdings = load_holdings(data_dir / "holdings.csv")
        price_history = load_price_history(data_dir / "price_history.csv")
        metrics = compute_portfolio_metrics(holdings, price_history)
        return {
            "holdings": holdings,
            "price_history": price_history,
            "metrics": metrics,
        }
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        st.stop()


# ----------------------------------------------------------------------
# Page definitions
# ----------------------------------------------------------------------
def overview_page(data: dict):
    st.header("📊 Portfolio Overview")
    st.subheader("Current Distribution")
    fig = plot_portfolio_distribution(data["holdings"])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Total Value")
    total_value = data["metrics"]["total_value"]
    st.metric(label="Portfolio Value (USD)", value=f"${total_value:,.2f}")


def holdings_page(data: dict):
    st.header("💰 Holdings")
    st.dataframe(data["holdings"], use_container_width=True)


def trends_page(data: dict):
    st.header("📈 Market Trends")
    fig = plot_price_trends(data["price_history"])
    st.plotly_chart(fig, use_container_width=True)


def analysis_page(data: dict):
    st.header("🔎 Profit / Loss Analysis")
    profit_fig = plot_profit_loss(data["metrics"]["profit_loss"])
    volume_fig = plot_volume_analysis(data["price_history"])
    st.plotly_chart(profit_fig, use_container_width=True)
    st.plotly_chart(volume_fig, use_container_width=True)


# ----------------------------------------------------------------------
# Main app
# ----------------------------------------------------------------------
def main():
    st.set_page_config(
        page_title="Crypto Portfolio Dashboard",
        layout="wide",
        page_icon="💹",
        initial_sidebar_state="expanded",
    )
    st.title("💎 Crypto Portfolio Dashboard")

    data = _load_data()

    # Sidebar navigation
    pages = {
        "Overview": overview_page,
        "Holdings": holdings_page,
        "Market Trends": trends_page,
        "Analysis": analysis_page,
    }
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Render selected page
    pages[selection](data)


if __name__ == "__main__":
    main()