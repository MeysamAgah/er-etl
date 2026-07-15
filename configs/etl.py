from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "data" / "tgju.db"

DATABASE_PATH.parent.mkdir(exist_ok=True)

ER_TYPE = "price_dollar_rl"

TABLE_NAME = "market_data"

COLUMNS = [
    "open",
    "high",
    "low",
    "close",
    "change",
    "change_percent",
    "gregorian_date",
    "jalali_date",
]


API_LENGTH = 100