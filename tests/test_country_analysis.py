
import pandas as pd
import pytest

from src.country_analysis import (
    get_country_medal_trend,
    get_top_sports,
)


@pytest.fixture
def sample_data():
    columns = [
        "ID", "Year", "Sport", "Event",
        "NOC", "Team", "region", "Medal"
    ]

    rows = [
        # Brazil football team: one national gold.
        (1, 2016, "Football", "Football Men's Football",
         "BRA", "Brazil", "Brazil", "Gold"),
        (2, 2016, "Football", "Football Men's Football",
         "BRA", "Brazil", "Brazil", "Gold"),

        # Brazil receives an individual bronze.
        (3, 2016, "Judo", "Judo Women's Lightweight",
         "BRA", "Brazil", "Brazil", "Bronze"),

        # Brazil also participates in 2012, without a medal.
        (4, 2012, "Swimming", "Swimming Men's 100 metres",
         "BRA", "Brazil", "Brazil", None),

        # USA individual medals.
        (5, 2016, "Swimming", "Swimming Men's 100 metres",
         "USA", "United States", "USA", "Gold"),
        (6, 2016, "Swimming", "Swimming Men's 200 metres",
         "USA", "United States", "USA", "Silver"),
    ]

    return pd.DataFrame(rows, columns=columns)


def test_country_medal_trend_columns(sample_data):
    result = get_country_medal_trend(
        sample_data, region="Brazil"
    )

    assert result.columns.tolist() == [
        "Year", "Gold", "Silver", "Bronze", "Total"
    ]


def test_country_medal_trend_values(sample_data):
    result = get_country_medal_trend(
        sample_data, region="Brazil"
    )

    assert result["Year"].tolist() == [2012, 2016]

    row_2016 = result[result["Year"] == 2016].iloc[0]

    assert row_2016["Gold"] == 1
    assert row_2016["Silver"] == 0
    assert row_2016["Bronze"] == 1
    assert row_2016["Total"] == 2


def test_country_year_without_medals(sample_data):
    result = get_country_medal_trend(
        sample_data, region="Brazil"
    )

    row_2012 = result[result["Year"] == 2012].iloc[0]

    assert row_2012["Total"] == 0


def test_country_medal_trend_unknown_region(sample_data):
    result = get_country_medal_trend(
        sample_data, region="UnknownCountry"
    )

    assert result.empty
    assert result.columns.tolist() == [
        "Year", "Gold", "Silver", "Bronze", "Total"
    ]


def test_top_sports_columns(sample_data):
    result = get_top_sports(
        sample_data, region="Brazil"
    )

    assert result.columns.tolist() == [
        "Sport", "Total"
    ]


def test_top_sports_values(sample_data):
    result = get_top_sports(
        sample_data, region="Brazil"
    )

    assert set(result["Sport"]) == {"Football", "Judo"}
    assert result["Total"].sum() == 2


def test_top_sports_limit(sample_data):
    result = get_top_sports(
        sample_data, region="Brazil", top_n=1
    )

    assert len(result) == 1


def test_top_sports_unknown_region(sample_data):
    result = get_top_sports(
        sample_data, region="UnknownCountry"
    )

    assert result.empty
    assert result.columns.tolist() == [
        "Sport", "Total"
    ]


def test_invalid_top_n(sample_data):
    with pytest.raises(ValueError):
        get_top_sports(
            sample_data, region="Brazil", top_n=0
        )


def test_missing_country_columns(sample_data):
    incomplete = sample_data.drop(columns=["region"])

    with pytest.raises(ValueError):
        get_country_medal_trend(
            incomplete, region="Brazil"
        )

    with pytest.raises(ValueError):
        get_top_sports(
            incomplete, region="Brazil"
        )
