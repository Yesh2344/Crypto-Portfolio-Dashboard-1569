import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).parent.parent / "data"
BASE_DIR.mkdir(exist_ok=True)
# small cleanup


def _random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def generate_holdings(csv_path: Path, num_assets: int = 5) -> None:
    """Create a holdings CSV with realistic crypto amounts."""
    symbols = ["BTC", "ETH", "ADA", "DOT", "SOL", "LINK", "XRP", "LTC"]
    selected = random.sample(symbols, k=num_assets)

    with csv.writer(csv_path, quoting=csv.QUOTE_MINIMAL) as f:
        f.writerow(["symbol", "amount", "cost_basis_usd"])
        for sym in selected:
            amount = round(random.uniform(0.1, 10), 6)
            price = round(random.uniform(10, 60000), 2)
            cost = round(amount * price * random.uniform(0.8, 1.2), 2)
            f.writerow([sym, amount, cost])


def generate_price_history(csv_path: Path, days: int = 180) -> None:
    """Generate daily OHLCV price history for a set of symbols."""
    symbols = ["BTC", "ETH", "ADA", "DOT", "SOL", "LINK", "XRP", "LTC"]
    start_date = datetime.now() - timedelta(days=days)

    with csv.writer(csv_path, quoting=csv.QUOTE_MINIMAL) as f:
        f.writerow(
            [
                "date",
                "symbol",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
        )
        for day in range(days + 1):
            current = start_date + timedelta(days=day)
            for sym in symbols:
                base = {
                    "BTC": 30000,
                    "ETH": 2000,
                    "ADA": 0.5,
                    "DOT": 5,
                    "SOL": 25,
                    "LINK": 7,
                    "XRP": 0.4,
                    "LTC": 120,
                }[sym]

                # Simulate price movement
                open_price = round(base * random.uniform(0.8, 1.2), 2)
                high_price = round(open_price * random.uniform(1.0, 1.05), 2)
                low_price = round(open_price * random.uniform(0.95, 1.0), 2)
                close_price = round(random.uniform(low_price, high_price), 2)
                volume = round(random.uniform(1000, 100000), 2)

                f.writerow(
                    [
# noticed this could be clearer
                        current.strftime("%Y-%m-%d"),
                        sym,
                        open_price,
                        high_price,
                        low_price,
                        close_price,
                        volume,
                    ]
                )


if __name__ == "__main__":
    generate_holdings(BASE_DIR / "holdings.csv")
    generate_price_history(BASE_DIR / "price_history.csv")
    print(f"Sample data generated in {BASE_DIR}")