"""
data_logger.py
──────────────
Logs fare results to a CSV file for fare history tracking.
"""

import csv
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
HISTORY_FILE = DATA_DIR / "fare_history.csv"

COLUMNS = [
    "timestamp", "pickup", "destination",
    "platform", "ride_type", "fare", "fare_min", "fare_max", "eta", "status"
]


def log_fares(pickup: str, destination: str, results: list[dict]):
    """
    Append fare results to CSV history file.

    Args:
        pickup:      Pickup location string
        destination: Destination location string
        results:     List of fare result dicts from scrapers
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = []
    for r in results:
        rows.append({
            "timestamp":   timestamp,
            "pickup":      pickup,
            "destination": destination,
            "platform":    r.get("platform", ""),
            "ride_type":   r.get("ride_type", ""),
            "fare":        r.get("fare", ""),
            "fare_min":    r.get("fare_min", 0),
            "fare_max":    r.get("fare_max", 0),
            "eta":         r.get("eta", ""),
            "status":      r.get("status", ""),
        })

    file_exists = HISTORY_FILE.exists()
    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)

    logger.info(f"Logged {len(rows)} fare records to history")


def load_history() -> pd.DataFrame:
    """Load fare history from CSV. Returns empty DataFrame if no history."""
    if not HISTORY_FILE.exists():
        return pd.DataFrame(columns=COLUMNS)
    try:
        df = pd.read_csv(HISTORY_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except Exception as e:
        logger.error(f"Error loading history: {e}")
        return pd.DataFrame(columns=COLUMNS)


def clear_history():
    """Delete the fare history CSV."""
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
        logger.info("Fare history cleared")


def history_exists() -> bool:
    return HISTORY_FILE.exists() and HISTORY_FILE.stat().st_size > 0
