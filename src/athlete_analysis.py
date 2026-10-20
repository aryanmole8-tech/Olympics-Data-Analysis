
"""
Olympics Data Analysis - Athlete Analysis Module

Analyze gender participation and the most decorated
athletes in historical Summer Olympics records.

Athlete medal counts differ from national medal awards:
each athlete receives credit for their own medals,
including medals earned in team events.
"""

import pandas as pd


GENDER_COLUMNS = ["Year", "Male", "Female"]

ATHLETE_COLUMNS = [
    "Name", "region", "Gold", "Silver", "Bronze", "Total"
]

MEDAL_TYPES = ["Gold", "Silver", "Bronze"]


def get_gender_participation_trend(df):
    """
    Count distinct male and female athlete IDs per year.

    Returns
    -------
    pandas.DataFrame
        Year, Male, Female
    """

    required = {"Year", "ID", "Sex"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if df.empty:
        return pd.DataFrame({
            "Year": pd.Series(dtype="int64"),
            "Male": pd.Series(dtype="int64"),
            "Female": pd.Series(dtype="int64"),
        })

    data = df.loc[
        df["Sex"].isin(["M", "F"]),
        ["Year", "ID", "Sex"]
    ].drop_duplicates()

    counts = (
        data.groupby(["Year", "Sex"])["ID"]
        .nunique()
        .unstack(fill_value=0)
    )

    counts = counts.reindex(
        columns=["M", "F"],
        fill_value=0
    )

    result = counts.rename(
        columns={"M": "Male", "F": "Female"}
    ).reset_index()

    result = result[GENDER_COLUMNS]
    result = result.sort_values("Year")

    return result.astype("int64").reset_index(drop=True)


def get_top_athletes(df, top_n=10, region=None):
    """
    Return athletes ranked by medalist records.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned Summer Olympics data.

    top_n : int
        Maximum number of athletes.

    region : str or None
        Optional country/region filter.

    Returns
    -------
    pandas.DataFrame
        Name, region, Gold, Silver, Bronze, Total

    Counting methodology
    --------------------
    Each athlete's medals are counted using athlete ID
    and distinct Olympic edition/event/medal records.

    Team-event medals count once for each athlete who
    received that medal.
    """

    required = {
        "ID", "Name", "region",
        "Year", "Event", "Medal"
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if not isinstance(top_n, int) or top_n < 1:
        raise ValueError("top_n must be a positive integer.")

    empty = pd.DataFrame({
        "Name": pd.Series(dtype="str"),
        "region": pd.Series(dtype="str"),
        "Gold": pd.Series(dtype="int64"),
        "Silver": pd.Series(dtype="int64"),
        "Bronze": pd.Series(dtype="int64"),
        "Total": pd.Series(dtype="int64"),
    })

    data = df

    if region is not None:
        data = data.loc[data["region"] == region]

    data = data.loc[
        data["Medal"].isin(MEDAL_TYPES)
    ].copy()

    if data.empty:
        return empty

    # Prevent duplicate athlete-event medals.
    data = data.drop_duplicates(
        subset=["ID", "Year", "Event", "Medal"]
    )

    # Preserve athlete ID as the grouping key so that
    # athletes with identical names are not merged.
    counts = (
        data.groupby(["ID", "Medal"])
        .size()
        .unstack(fill_value=0)
    )

    counts = counts.reindex(
        columns=MEDAL_TYPES,
        fill_value=0
    )

    counts["Total"] = counts[MEDAL_TYPES].sum(axis=1)

    # Obtain a representative name and region for each ID.
    athlete_info = (
        data.sort_values(["Year", "Event"])
        .drop_duplicates(subset=["ID"])
        .set_index("ID")[["Name", "region"]]
    )

    result = athlete_info.join(counts, how="inner")

    result = result[
        ["Name", "region", "Gold", "Silver", "Bronze", "Total"]
    ]

    result = result.sort_values(
        ["Total", "Gold", "Silver", "Bronze", "Name"],
        ascending=[False, False, False, False, True]
    )

    return result.head(top_n).reset_index(drop=True)
