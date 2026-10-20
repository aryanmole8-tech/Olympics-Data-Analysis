
"""
Olympics Data Analysis - Overall Analysis Module

Analyzes Summer Olympics participation and
overall statistics using cleaned athlete-event data.
"""

import pandas as pd


# ============================================================
# 1. OVERALL STATISTICS
# ============================================================

def get_overall_stats(df, year=None):
    """
    Calculate overall Olympics statistics.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned Summer Olympics dataset.

    year : int or None
        Olympic year to analyze.
        None means all available years.

    Returns
    -------
    dict
        editions : number of distinct Olympic editions
        nations  : number of distinct NOC codes
        sports   : number of distinct sports
        events   : number of distinct events
        athletes : number of distinct athlete IDs
    """

    required_columns = {
        "Year", "NOC", "Sport", "Event", "ID"
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    data = df

    if year is not None:
        data = data.loc[data["Year"] == year]

    return {
        "editions": int(data["Year"].nunique()),
        "nations": int(data["NOC"].nunique()),
        "sports": int(data["Sport"].nunique()),
        "events": int(data["Event"].nunique()),
        "athletes": int(data["ID"].nunique()),
    }


# ============================================================
# 2. PARTICIPATION TREND
# ============================================================

def get_participation_trend(df):
    """
    Calculate nation and athlete participation by year.

    Athletes are counted using distinct ID values,
    rather than athlete-event records.

    Returns
    -------
    pandas.DataFrame
        Year, Nations, Athletes
    """

    required_columns = {"Year", "NOC", "ID"}

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    result_columns = ["Year", "Nations", "Athletes"]

    if df.empty:
        return pd.DataFrame({
            "Year": pd.Series(dtype="int64"),
            "Nations": pd.Series(dtype="int64"),
            "Athletes": pd.Series(dtype="int64"),
        })

    trend = (
        df.groupby("Year")
        .agg(
            Nations=("NOC", "nunique"),
            Athletes=("ID", "nunique"),
        )
        .reset_index()
    )

    trend = trend[result_columns].sort_values("Year")

    trend[result_columns] = trend[result_columns].astype(
        "int64"
    )

    return trend.reset_index(drop=True)


# ============================================================
# 3. MODULE CHECK
# ============================================================

if __name__ == "__main__":
    print("Olympics Overall Analysis module loaded.")
