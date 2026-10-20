
"""
Olympics Data Analysis - Country Analysis Module

Provides country-specific medal trends and top sports
using cleaned Summer Olympics records.

Medal counts are dataset-derived estimates, not
independently verified official historical totals.
"""

import pandas as pd

from src.medal_analysis import get_medal_tally


TREND_COLUMNS = ["Year", "Gold", "Silver", "Bronze", "Total"]
SPORT_COLUMNS = ["Sport", "Total"]


def get_country_medal_trend(df, region):
    """
    Return a country's medal totals for each Olympic year.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned Summer Olympics data.

    region : str
        Country/region display name.

    Returns
    -------
    pandas.DataFrame
        Year, Gold, Silver, Bronze, Total
    """

    required = {"Year", "region"}

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if region is None:
        raise ValueError("A region must be provided.")

    years = sorted(
        df.loc[df["region"] == region, "Year"]
        .dropna()
        .unique()
    )

    records = []

    for year in years:
        tally = get_medal_tally(
            df,
            year=int(year),
            region=region,
        )

        if tally.empty:
            values = {
                "Gold": 0,
                "Silver": 0,
                "Bronze": 0,
                "Total": 0,
            }
        else:
            values = {
                medal: int(tally.iloc[0][medal])
                for medal in [
                    "Gold", "Silver", "Bronze", "Total"
                ]
            }

        records.append({
            "Year": int(year),
            **values,
        })

    if not records:
        return pd.DataFrame({
            col: pd.Series(dtype="int64")
            for col in TREND_COLUMNS
        })

    return pd.DataFrame(
        records,
        columns=TREND_COLUMNS,
    ).astype("int64")


def get_top_sports(df, region, top_n=10):
    """
    Return sports ranked by estimated medal awards.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned Summer Olympics data.

    region : str
        Country/region display name.

    top_n : int
        Maximum number of sports to return.

    Returns
    -------
    pandas.DataFrame
        Sport, Total
    """

    required = {"Sport", "region"}

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if region is None:
        raise ValueError("A region must be provided.")

    if not isinstance(top_n, int) or top_n < 1:
        raise ValueError("top_n must be a positive integer.")

    country_data = df.loc[df["region"] == region]

    if country_data.empty:
        return pd.DataFrame({
            "Sport": pd.Series(dtype="str"),
            "Total": pd.Series(dtype="int64"),
        })

    records = []

    for sport in sorted(country_data["Sport"].dropna().unique()):
        sport_data = country_data.loc[
            country_data["Sport"] == sport
        ]

        tally = get_medal_tally(
            sport_data,
            region=region,
        )

        total = (
            int(tally["Total"].sum())
            if not tally.empty
            else 0
        )

        if total > 0:
            records.append({
                "Sport": sport,
                "Total": total,
            })

    if not records:
        return pd.DataFrame({
            "Sport": pd.Series(dtype="str"),
            "Total": pd.Series(dtype="int64"),
        })

    result = pd.DataFrame(
        records,
        columns=SPORT_COLUMNS,
    )

    result = result.sort_values(
        ["Total", "Sport"],
        ascending=[False, True],
    ).head(top_n)

    return result.reset_index(drop=True)
