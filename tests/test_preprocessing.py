
import pandas as pd
import pytest

from src.preprocessing import load_and_clean_data


@pytest.fixture(scope="module")
def cleaned_data():
    return load_and_clean_data(
        data_dir="data",
        season="Summer"
    )


def test_required_columns(cleaned_data):
    required = {
        "ID", "Name", "Sex", "Age", "Height",
        "Weight", "Team", "NOC", "Games",
        "Year", "Season", "City", "Sport",
        "Event", "Medal", "region"
    }

    assert required.issubset(cleaned_data.columns)


def test_only_summer_olympics(cleaned_data):
    assert set(cleaned_data["Season"].unique()) == {"Summer"}


def test_no_exact_duplicates(cleaned_data):
    assert cleaned_data.duplicated().sum() == 0


def test_no_missing_required_values(cleaned_data):
    assert cleaned_data["ID"].notna().all()
    assert cleaned_data["Year"].notna().all()
    assert cleaned_data["region"].notna().all()


def test_correct_data_types(cleaned_data):
    assert pd.api.types.is_integer_dtype(cleaned_data["ID"])
    assert pd.api.types.is_integer_dtype(cleaned_data["Year"])
    assert pd.api.types.is_numeric_dtype(cleaned_data["Age"])


def test_valid_medals(cleaned_data):
    valid_medals = {"Gold", "Silver", "Bronze"}

    actual_medals = set(
        cleaned_data["Medal"].dropna().unique()
    )

    assert actual_medals.issubset(valid_medals)


def test_historical_year_range(cleaned_data):
    assert cleaned_data["Year"].min() == 1896
    assert cleaned_data["Year"].max() == 2016


def test_unique_athlete_ids(cleaned_data):
    assert cleaned_data["ID"].nunique() == 116776


def test_missing_dataset_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_and_clean_data(data_dir=tmp_path)
