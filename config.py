from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Config:
    APP_NAME: str = "Crypto Portfolio Dashboard"
    PRIMARY_COLOR: str = "#0E1117"
    SECONDARY_COLOR: str = "#1F2937"
    ACCENT_COLOR: str = "#6366F1"
    FONT: str = "sans-serif"
    PAGE_TITLES: List[str] = ("Overview", "Holdings", "Market Trends", "Analysis")
    # Plotly default template
    PLOTLY_TEMPLATE: str = "plotly_dark"


# Export a singleton for convenient import
Config = Config()