
from pathlib import Path

import pandas as pd


REQUIRED_ATHLETE_COLUMNS = {
    "ID", "Name", "Sex", "Age", "Height",
    "Weight", "Team", "NOC", "Games",
    "Year", "Season", "City", "Sport",
    "Event", "Medal"
}


def load_and_clean_data(data_dir="data", season="Summer"):
    """
    Load and preprocess historical Olympic data.

    Parameters
    ----------
    data_dir : str
        Directory containing the two CSV files.
    season : str
        Olympic season to retain. Defaults to Summer.

    Returns
    -------
    pandas.DataFrame
        Cleaned Olympic athlete-event records.
    """

    data_path = Path(data_dir)

    athletes_path = data_path / "athlete_events.csv"
    regions_path = data_path / "noc_regions.csv"

    missing_files = [
        str(path)
        for path in (athletes_path, regions_path)
        if not path.is_file()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Missing Olympics dataset files: "
            + ", ".join(missing_files)
            + "\nDownload from: "
            "https://www.kaggle.com/datasets/"
            "heesoo37/120-years-of-olympic-history-athletes-and-results"
        )

    athletes = pd.read_csv(athletes_path)
    regions = pd.read_csv(regions_path)

    missing_columns = REQUIRED_ATHLETE_COLUMNS - set(athletes.columns)

    if missing_columns:
        raise ValueError(
            f"Missing athlete columns: {sorted(missing_columns)}"
        )

    if not {"NOC", "region"}.issubset(regions.columns):
        raise ValueError(
            "noc_regions.csv must contain NOC and region columns."
        )

    if regions["NOC"].duplicated().any():
        raise ValueError("Duplicate NOC codes found in region lookup.")

    # Retain the requested Olympic season.
    df = athletes.loc[athletes["Season"] == season].copy()

    # Convert numeric columns safely.
    for column in ["ID", "Age", "Height", "Weight", "Year"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Year and ID are required for reliable analyses.
    df = df.dropna(subset=["ID", "Year"])
    df["ID"] = df["ID"].astype("int64")
    df["Year"] = df["Year"].astype("int64")

    # Preserve missing medals as null values.
    df["Medal"] = df["Medal"].replace(
        ["NA", "None", ""], pd.NA
    )

    # Remove exact duplicate records only.
    df = df.drop_duplicates().copy()

    # Join NOC codes to display regions.
    regions_lookup = regions[["NOC", "region"]]

    df = df.merge(
        regions_lookup,
        on="NOC",
        how="left",
        validate="many_to_one"
    )

    # Preserve unmatched or blank regions using NOC.
    df["region"] = (
        df["region"]
        .replace(r"^\s*$", pd.NA, regex=True)
        .fillna(df["NOC"])
    )

    return df.reset_index(drop=True)
