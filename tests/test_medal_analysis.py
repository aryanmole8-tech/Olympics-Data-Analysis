
import pandas as pd
import pytest

from src.medal_analysis import (
    get_medal_tally,
    is_team_event,
)


@pytest.fixture
def sample_data():
    """Create sample team and individual medal records."""

    records = [
        # Three players from one gold-winning team.
        (1, 2016, "Football",
         "Football Men's Football",
         "BRA", "Brazil", "Brazil", "Gold"),

        (2, 2016, "Football",
         "Football Men's Football",
         "BRA", "Brazil", "Brazil", "Gold"),

        (3, 2016, "Football",
         "Football Men's Football",
         "BRA", "Brazil", "Brazil", "Gold"),

        # Two distinct individual gold medals.
        (4, 2016, "Athletics",
         "Athletics Men's 100 metres",
         "JAM", "Jamaica", "Jamaica", "Gold"),

        (5, 2016, "Swimming",
         "Swimming Men's 200 metres Freestyle",
         "USA", "United States", "USA", "Gold"),

        # Individual silver and bronze.
        (6, 2016, "Athletics",
         "Athletics Men's 100 metres",
         "USA", "United States", "USA", "Silver"),

        (7, 2016, "Athletics",
         "Athletics Men's 100 metres",
         "CAN", "Canada", "Canada", "Bronze"),

        # A second year for filtering.
        (8, 2012, "Badminton",
         "Badminton Men's Singles",
         "CHN", "China", "China", "Gold"),
    ]

    columns = [
        "ID", "Year", "Sport", "Event",
        "NOC", "Team", "region", "Medal"
    ]

    return pd.DataFrame(records, columns=columns)


def test_team_event_classification():
    assert is_team_event(
        "Football", "Football Men's Football"
    )

    assert is_team_event(
        "Swimming",
        "Swimming Men's 4 x 100 metres Freestyle Relay"
    )

    assert is_team_event(
        "Rowing", "Rowing Women's Double Sculls"
    )

    assert is_team_event(
        "Rhythmic Gymnastics",
        "Rhythmic Gymnastics Women's Group"
    )

    assert is_team_event(
        "Sailing", "Sailing Men's Skiff"
    )


def test_individual_event_classification():
    assert not is_team_event(
        "Athletics", "Athletics Men's 100 metres"
    )

    assert not is_team_event(
        "Swimming", "Swimming Women's 100 metres Freestyle"
    )


def test_team_medals_count_once(sample_data):
    result = get_medal_tally(
        sample_data, year=2016, region="Brazil"
    )

    assert len(result) == 1
    assert result.iloc[0]["Gold"] == 1
    assert result.iloc[0]["Total"] == 1


def test_individual_medals(sample_data):
    result = get_medal_tally(
        sample_data, year=2016, region="USA"
    )

    assert result.iloc[0]["Gold"] == 1
    assert result.iloc[0]["Silver"] == 1
    assert result.iloc[0]["Total"] == 2


def test_year_filter(sample_data):
    result = get_medal_tally(sample_data, year=2012)

    assert len(result) == 1
    assert result.iloc[0]["region"] == "China"
    assert result.iloc[0]["Gold"] == 1


def test_region_filter(sample_data):
    result = get_medal_tally(sample_data, region="Jamaica")

    assert len(result) == 1
    assert result.iloc[0]["Gold"] == 1


def test_empty_result(sample_data):
    result = get_medal_tally(sample_data, year=1900)

    assert result.empty
    assert result.columns.tolist() == [
        "region", "Gold", "Silver", "Bronze", "Total"
    ]


def test_total_equals_medal_sum(sample_data):
    result = get_medal_tally(sample_data)

    assert (
        result["Total"]
        == result[["Gold", "Silver", "Bronze"]].sum(axis=1)
    ).all()


def test_missing_columns(sample_data):
    incomplete = sample_data.drop(columns=["Medal"])

    with pytest.raises(ValueError):
        get_medal_tally(incomplete)


def test_distinct_individual_medals_same_country():
    """Two individual awards must not be merged."""

    data = pd.DataFrame([
        (1, 1904, "Gymnastics",
         "Gymnastics Men's Horse Vault",
         "USA", "United States", "USA", "Gold"),
        (2, 1904, "Gymnastics",
         "Gymnastics Men's Horse Vault",
         "USA", "United States", "USA", "Gold"),
    ], columns=[
        "ID", "Year", "Sport", "Event",
        "NOC", "Team", "region", "Medal"
    ])

    result = get_medal_tally(data)

    assert result.iloc[0]["Gold"] == 2
