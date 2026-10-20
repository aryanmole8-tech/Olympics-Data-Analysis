
import pandas as pd
import pytest

from src.overall_analysis import (
    get_overall_stats,
    get_participation_trend,
)


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Year": [2012, 2012, 2012, 2016, 2016],
        "NOC": ["IND", "IND", "USA", "IND", "USA"],
        "Sport": [
            "Badminton", "Badminton", "Swimming",
            "Badminton", "Swimming"
        ],
        "Event": [
            "Singles", "Doubles", "Freestyle",
            "Singles", "Freestyle"
        ],
        "ID": [1, 1, 2, 1, 3],
    })


def test_overall_stats(sample_data):
    stats = get_overall_stats(sample_data)

    assert stats == {
        "editions": 2,
        "nations": 2,
        "sports": 2,
        "events": 3,
        "athletes": 3,
    }


def test_year_filter(sample_data):
    stats = get_overall_stats(sample_data, year=2012)

    assert stats["editions"] == 1
    assert stats["athletes"] == 2
    assert stats["nations"] == 2


def test_unique_athlete_count(sample_data):
    stats = get_overall_stats(sample_data)

    # Athlete ID 1 appears in multiple records.
    assert stats["athletes"] == 3


def test_participation_trend(sample_data):
    result = get_participation_trend(sample_data)

    assert result.columns.tolist() == [
        "Year", "Nations", "Athletes"
    ]

    assert result["Year"].tolist() == [2012, 2016]
    assert result["Nations"].tolist() == [2, 2]
    assert result["Athletes"].tolist() == [2, 2]


def test_empty_dataset(sample_data):
    empty = sample_data.iloc[0:0]

    stats = get_overall_stats(empty)

    assert all(value == 0 for value in stats.values())

    trend = get_participation_trend(empty)

    assert trend.empty
    assert trend.columns.tolist() == [
        "Year", "Nations", "Athletes"
    ]


def test_nonexistent_year(sample_data):
    stats = get_overall_stats(sample_data, year=2000)

    assert all(value == 0 for value in stats.values())


def test_missing_required_columns(sample_data):
    incomplete = sample_data.drop(columns=["ID"])

    with pytest.raises(ValueError):
        get_overall_stats(incomplete)

    with pytest.raises(ValueError):
        get_participation_trend(incomplete)
