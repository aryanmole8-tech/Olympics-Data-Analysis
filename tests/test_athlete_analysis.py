
import pandas as pd
import pytest

from src.athlete_analysis import (
    get_gender_participation_trend,
    get_top_athletes,
)


@pytest.fixture
def sample_data():
    columns = [
        "ID", "Name", "Sex", "Year",
        "Event", "Medal", "region"
    ]

    rows = [
        # Same athlete, two events, one Olympic year.
        (1, "Athlete A", "F", 2016,
         "Swimming 100m", "Gold", "India"),
        (1, "Athlete A", "F", 2016,
         "Swimming 200m", "Silver", "India"),

        # Another female athlete in the same year.
        (2, "Athlete B", "F", 2016,
         "Swimming Relay", "Gold", "India"),

        # Male athlete receives an individual medal.
        (3, "Athlete C", "M", 2016,
         "Wrestling", "Bronze", "USA"),

        # Athlete A competes again in 2012.
        (1, "Athlete A", "F", 2012,
         "Swimming 100m", None, "India"),

        # Athlete with no medals.
        (4, "Athlete D", "M", 2012,
         "Athletics", None, "USA"),
    ]

    return pd.DataFrame(rows, columns=columns)


def test_gender_columns(sample_data):
    result = get_gender_participation_trend(sample_data)

    assert result.columns.tolist() == [
        "Year", "Male", "Female"
    ]


def test_gender_unique_athletes(sample_data):
    result = get_gender_participation_trend(sample_data)

    row_2016 = result[result["Year"] == 2016].iloc[0]

    assert row_2016["Male"] == 1
    assert row_2016["Female"] == 2


def test_gender_year_sorting(sample_data):
    result = get_gender_participation_trend(sample_data)

    assert result["Year"].tolist() == [2012, 2016]


def test_top_athlete_columns(sample_data):
    result = get_top_athletes(sample_data)

    assert result.columns.tolist() == [
        "Name", "region", "Gold",
        "Silver", "Bronze", "Total"
    ]


def test_multiple_athlete_medals(sample_data):
    result = get_top_athletes(sample_data)

    athlete = result[result["Name"] == "Athlete A"].iloc[0]

    assert athlete["Gold"] == 1
    assert athlete["Silver"] == 1
    assert athlete["Total"] == 2


def test_region_filter(sample_data):
    result = get_top_athletes(
        sample_data, region="India"
    )

    assert set(result["region"]) == {"India"}
    assert len(result) == 2


def test_top_n_limit(sample_data):
    result = get_top_athletes(sample_data, top_n=1)

    assert len(result) == 1
    assert result.iloc[0]["Name"] == "Athlete A"


def test_empty_dataset(sample_data):
    empty = sample_data.iloc[0:0]

    assert get_gender_participation_trend(empty).empty
    assert get_top_athletes(empty).empty


def test_unknown_region(sample_data):
    result = get_top_athletes(
        sample_data, region="UnknownCountry"
    )

    assert result.empty


def test_invalid_top_n(sample_data):
    with pytest.raises(ValueError):
        get_top_athletes(sample_data, top_n=0)


def test_missing_columns(sample_data):
    incomplete = sample_data.drop(columns=["ID"])

    with pytest.raises(ValueError):
        get_gender_participation_trend(incomplete)

    with pytest.raises(ValueError):
        get_top_athletes(incomplete)


def test_duplicate_athlete_event_medal():
    data = pd.DataFrame({
        "ID": [1, 1],
        "Name": ["Athlete A", "Athlete A"],
        "region": ["India", "India"],
        "Year": [2016, 2016],
        "Event": ["Swimming Relay", "Swimming Relay"],
        "Medal": ["Gold", "Gold"],
    })

    result = get_top_athletes(data)

    assert result.iloc[0]["Gold"] == 1
    assert result.iloc[0]["Total"] == 1
