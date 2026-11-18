"""Data loading and cleaning for the wine-origin dashboard.

Load once at startup (cached by the caller); every view filters the
returned DataFrame in memory. Price NaNs are kept — price-based views
exclude them per-view so rating-only views are not distorted.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
WINE_DATA_PATH = DATA_DIR / "winemag-data-with-year.csv"
CATEGORY_DATA_PATH = DATA_DIR / "wine_category.csv"

TEXT_COLUMNS = [
    "country", "province", "region_1", "region_2",
    "variety", "winery", "designation", "description",
]
CATEGORY_ORDER = ["red", "white", "rose", "sparkling", "dessert", "other"]


def load_wine_data() -> pd.DataFrame:
    wine = pd.read_csv(WINE_DATA_PATH)
    category = pd.read_csv(CATEGORY_DATA_PATH)

    for col in TEXT_COLUMNS:
        wine[col] = wine[col].fillna("Unknown").astype(str).str.strip()

    for col in ["points", "price", "year"]:
        wine[col] = pd.to_numeric(wine[col], errors="coerce")
    # 实测存在 1000–7200 的脏年份,出界即置 NA
    wine.loc[(wine["year"] < 1980) | (wine["year"] > 2026), "year"] = pd.NA

    category["variety"] = category["variety"].astype(str).str.strip()
    category["category"] = category["category"].astype(str).str.strip().str.lower()

    merged = wine.merge(category, on="variety", how="left")
    merged["category"] = merged["category"].fillna("other")
    merged["category"] = pd.Categorical(
        merged["category"], categories=CATEGORY_ORDER, ordered=True
    )

    merged["country_display"] = (
        merged["country"].replace({"US": "United States"}).astype(str).str.strip()
    )
    merged.loc[
        merged["country_display"].isin(["", "nan", "None", "Unknown"]),
        "country_display",
    ] = "Unknown"

    return merged


def get_country_options(df: pd.DataFrame) -> list[dict[str, str]]:
    countries = (
        df.loc[df["country_display"] != "Unknown", "country_display"]
        .value_counts()
        .index.tolist()
    )
    return [{"label": c, "value": c} for c in countries]


def get_price_bounds(df: pd.DataFrame) -> tuple[float, float]:
    prices = df["price"].dropna()
    return float(prices.min()), float(prices.max())
