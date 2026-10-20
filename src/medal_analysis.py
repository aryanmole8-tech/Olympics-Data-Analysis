
"""
Olympics Data Analysis - Medal Analysis Module

Purpose:
    Calculate estimated country medal awards using
    cleaned Olympics athlete-event records.

Important:
    Team-event medals are counted once per recorded team,
    while individual medalist records remain separate.

    Historical results are dataset-derived estimates,
    not independently verified official medal totals.
"""

import re

import pandas as pd


# ============================================================
# 1. CONSTANTS
# ============================================================

MEDALS = ["Gold", "Silver", "Bronze"]

MEDAL_COLUMNS = [
    "region",
    "Gold",
    "Silver",
    "Bronze",
    "Total",
]


# Sports treated as team competitions in this dataset.
TEAM_SPORTS = {
    "Baseball",
    "Basketball",
    "Beach Volleyball",
    "Cricket",
    "Football",
    "Handball",
    "Hockey",
    "Ice Hockey",
    "Lacrosse",
    "Polo",
    "Rugby",
    "Rugby Sevens",
    "Softball",
    "Tug-Of-War",
    "Volleyball",
    "Water Polo",
}


# Recognizable team or multi-athlete event descriptions.
TEAM_EVENT_PATTERN = re.compile(
    r"\b("
    r"team|teams|doubles|pairs|pair|"
    r"relay|synchroni[sz]ed|"
    r"four|fours|eight|eights|"
    r"quadruple|coxless|coxed|"
    r"madison|tandem"
    r")\b",
    re.IGNORECASE,
)


# Examples:
# 4 x 100 metres
# 4 x 200 metres
MULTI_ATHLETE_PATTERN = re.compile(
    r"\b(?:2|3|4|8)\s*x\s*\d+",
    re.IGNORECASE,
)


CREW_PATTERN = re.compile(
    r"\b(?:two|double|four|eight)[- ]"
    r"(?:person|man|men|woman|women)\b",
    re.IGNORECASE,
)


# ============================================================
# 2. IDENTIFY TEAM EVENTS
# ============================================================

def is_team_event(sport, event):
    """
    Identify recognizable team or multi-athlete events.

    Parameters
    ----------
    sport : str
        Olympic sport name.

    event : str
        Olympic event name.

    Returns
    -------
    bool
        True if the event is classified as a team event.
    """

    sport = str(sport)
    event = str(event)

    # Entire sports treated as team competitions.
    if sport in TEAM_SPORTS:
        return True

    # Event names containing team-related descriptions.
    if TEAM_EVENT_PATTERN.search(event):
        return True

    # Relay patterns such as 4 x 100 metres.
    if MULTI_ATHLETE_PATTERN.search(event):
        return True

    # Crew-related event descriptions.
    if CREW_PATTERN.search(event):
        return True

    # Rowing double sculls involve two athletes.
    if sport == "Rowing" and "Double Sculls" in event:
        return True

    # Rhythmic gymnastics group competitions.
    if sport == "Rhythmic Gymnastics" and "Group" in event:
        return True

    # Sailing skiff competitions involve a crew.
    if sport == "Sailing" and "Skiff" in event:
        return True

    return False


# ============================================================
# 3. CREATE AN EMPTY MEDAL TABLE
# ============================================================

def empty_medal_tally():
    """
    Return an empty DataFrame with the required schema.
    """

    return pd.DataFrame({
        "region": pd.Series(dtype="str"),
        "Gold": pd.Series(dtype="int64"),
        "Silver": pd.Series(dtype="int64"),
        "Bronze": pd.Series(dtype="int64"),
        "Total": pd.Series(dtype="int64"),
    })


# ============================================================
# 4. COUNTRY MEDAL TALLY
# ============================================================

def get_medal_tally(df, year=None, region=None):
    """
    Calculate estimated national Olympic medal awards.

    Parameters
    ----------
    df : pandas.DataFrame
        Cleaned Summer Olympics DataFrame.

    year : int or None
        Olympic year. None selects all years.

    region : str or None
        Country/region name. None selects all regions.

    Returns
    -------
    pandas.DataFrame
        Columns:
        region, Gold, Silver, Bronze, Total

    Counting methodology
    --------------------
    1. Remove records without awarded medals.
    2. Identify team-event records.
    3. Count a recorded team award once per
       Year, Event, NOC, Team and Medal.
    4. Preserve distinct individual medalist records.
    5. Aggregate by region and medal category.

    Limitations
    -----------
    Team classification uses documented heuristics.
    Historical results require reference validation.
    """

    # --------------------------------------------------------
    # Validate required columns
    # --------------------------------------------------------

    required_columns = {
        "ID",
        "Year",
        "Sport",
        "Event",
        "NOC",
        "Team",
        "Medal",
        "region",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            f"{sorted(missing_columns)}"
        )

    # --------------------------------------------------------
    # Apply optional filters
    # --------------------------------------------------------

    data = df

    if year is not None:
        data = data.loc[data["Year"] == year]

    if region is not None:
        data = data.loc[data["region"] == region]

    # --------------------------------------------------------
    # Keep awarded medals only
    # --------------------------------------------------------

    data = data.loc[
        data["Medal"].isin(MEDALS)
    ].copy()

    if data.empty:
        return empty_medal_tally()

    # --------------------------------------------------------
    # Identify team events
    # --------------------------------------------------------

    team_mask = pd.Series(
        [
            is_team_event(sport, event)
            for sport, event in zip(
                data["Sport"],
                data["Event"],
            )
        ],
        index=data.index,
        dtype=bool,
    )

    team_records = data.loc[team_mask].copy()

    individual_records = data.loc[
        ~team_mask
    ].copy()

    # --------------------------------------------------------
    # Deduplicate team medal awards
    # --------------------------------------------------------

    team_awards = team_records.drop_duplicates(
        subset=[
            "Year",
            "Event",
            "NOC",
            "Team",
            "Medal",
        ]
    )

    # Individual medalists count separately.
    # Exact source duplicates were already removed during
    # preprocessing.
    individual_awards = individual_records

    # --------------------------------------------------------
    # Combine national medal awards
    # --------------------------------------------------------

    awards = pd.concat(
        [
            team_awards,
            individual_awards,
        ],
        ignore_index=True,
    )

    # --------------------------------------------------------
    # Group by region and medal
    # --------------------------------------------------------

    counts = (
        awards.groupby(
            ["region", "Medal"]
        )
        .size()
        .unstack(fill_value=0)
    )

    counts = counts.reindex(
        columns=MEDALS,
        fill_value=0,
    )

    counts["Total"] = counts[MEDALS].sum(axis=1)

    # --------------------------------------------------------
    # Format final medal table
    # --------------------------------------------------------

    result = counts.reset_index()

    result = result[MEDAL_COLUMNS]

    result[[
        "Gold",
        "Silver",
        "Bronze",
        "Total",
    ]] = result[[
        "Gold",
        "Silver",
        "Bronze",
        "Total",
    ]].astype("int64")

    result = result.sort_values(
        by=[
            "Gold",
            "Silver",
            "Bronze",
            "region",
        ],
        ascending=[
            False,
            False,
            False,
            True,
        ],
    )

    return result.reset_index(drop=True)


# ============================================================
# 5. MODULE INFORMATION
# ============================================================

if __name__ == "__main__":
    print(
        "Olympics Medal Analysis module loaded.\n"
        "Import get_medal_tally() to analyze medal awards."
    )
