
# Olympics Dataset Documentation

## Dataset Information

**Dataset:** 120 Years of Olympic History: Athletes and Results

**Source:** Kaggle

**Dataset URL:**
https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results

**Historical coverage:** 1896–2016

The dataset contains historical Olympic athlete-event
records from the Summer and Winter Olympic Games.

This project's MVP analyzes Summer Olympics only.

## Required Files

Download and extract the Kaggle dataset.

Copy these files into the `data/` directory:

- `athlete_events.csv`
- `noc_regions.csv`

Expected structure:

```text
data/
├── README.md
├── athlete_events.csv
└── noc_regions.csv
```

The CSV files are excluded from Git to avoid
redistributing the raw dataset.

## Dataset Structure

### athlete_events.csv

Contains athlete-event records with 15 columns:

- ID
- Name
- Sex
- Age
- Height
- Weight
- Team
- NOC
- Games
- Year
- Season
- City
- Sport
- Event
- Medal

### noc_regions.csv

Contains NOC-to-region mappings:

- NOC
- region
- notes

## Dataset Validation

The downloaded dataset was checked using Pandas.

| Metric | Result |
|---|---:|
| Original athlete-event records | 271,116 |
| Summer athlete-event records | 222,552 |
| Winter athlete-event records | 48,564 |
| Original NOC lookup rows | 230 |
| Exact duplicate rows in full dataset | 1,385 |
| Cleaned Summer records | 221,167 |
| Unique Summer athlete IDs | 116,776 |
| Distinct Summer edition years | 29 |
| Historical year range | 1896–2016 |

The source includes records from the 1906
Intercalated Games. These are included in the
dataset's distinct edition-year count but are not
generally counted as an official numbered Olympiad.

## Preprocessing Rules

Implemented in `src/preprocessing.py`:

1. Load both CSV files.
2. Validate required column names.
3. Filter to Summer Olympics.
4. Convert numeric columns using Pandas.
5. Preserve missing athlete measurements.
6. Keep missing medals as null values.
7. Remove exact duplicate athlete-event records.
8. Merge NOC codes with region names.
9. Use the NOC code when a region label is missing.
10. Return a cleaned DataFrame for the analysis modules.

## Medal Counting Methodology

National medal awards and athlete medals are
different measures.

For national medal tables, the project uses an
event-based classification to reduce inflation
caused by multiple athletes receiving medals
in team competitions.

For individual athlete rankings, each athlete
receives credit for medals earned, including
medals in team events.

**Limitations:**

- Team-event classification is heuristic.
- Some historical competitions remain ambiguous.
- Historical country labels may combine different
  Olympic delegations.
- Medal revisions may not match the source CSV.
- Results should be labeled dataset-derived
  estimates rather than official medal totals
  until independently validated.

## Reproducing the Data Load

From the project root:

```python
from src.preprocessing import load_and_clean_data

df = load_and_clean_data(
    data_dir="data",
    season="Summer"
)

print(df.shape)
print(df.head())
```

## Dataset Usage

This project uses the historical dataset for
educational purposes, portfolio development,
data analysis, and visualization.

Raw CSV files are kept locally and are not
committed to the GitHub repository.
