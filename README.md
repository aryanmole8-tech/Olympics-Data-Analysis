# 🏅 Olympics Data Analysis & Visualization Dashboard

An interactive data analytics dashboard built with Python, Pandas, Streamlit, and Plotly to explore the history of the Summer Olympic Games from 1896 to 2016.

The project transforms historical Olympic athlete and medal records into interactive visualizations that help users explore medal performance, participation trends, country achievements, and athlete statistics.

## 📌 Project Overview

The Olympics Data Analysis Dashboard provides a user-friendly interface for exploring historical Summer Olympic data.

It includes data preprocessing, reusable analysis modules, interactive charts, filtering options, and automated tests.

### Project Objectives

* Analyze historical Olympic medal records.
* Explore participation trends across Olympic editions.
* Compare country-level Olympic performance.
* Identify athletes with the highest medal counts.
* Examine male and female participation trends.
* Present analytical results through an interactive dashboard.

## ✨ Features

### 1. 🥇 Medal Tally

* View Gold, Silver, Bronze, and Total medal counts.
* Filter medal statistics by Olympic year and country.
* Explore country medal rankings.
* Compare medal types across countries.
* View the leading countries by total medal records.

### 2. 📊 Overall Olympics Analysis

* Explore the number of Olympic editions, nations, sports, events, and athletes.
* Analyze participating nations over time.
* Examine athlete participation trends across historical editions.
* Filter summary statistics by Olympic year.

### 3. 🌍 Country Analysis

* Select an individual country or region.
* Explore its medal performance.
* Visualize medal trends across Olympic editions.
* Identify sports with the highest medal-record counts.

### 4. 🏃 Athlete Analysis

* Explore male and female athlete participation trends.
* View athletes ranked by medal records.
* Filter athlete rankings by country.
* Compare athlete medal records using interactive charts.

## 🛠️ Technologies Used

| Technology | Purpose                        |
| ---------- | ------------------------------ |
| Python     | Application logic and analysis |
| Pandas     | Data cleaning and manipulation |
| NumPy      | Numerical operations           |
| Streamlit  | Interactive web dashboard      |
| Plotly     | Interactive visualizations     |
| Matplotlib | Exploratory data visualization |
| Seaborn    | Statistical visualization      |
| Pytest     | Automated testing              |
| Jupyter    | Notebook-based analysis        |

## 📂 Project Structure

```text
Olympics-Data-Analysis/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── athlete_events.csv
│   └── noc_regions.csv
│
├── notebooks/
│
├── assets/
│
├── pages/
│   ├── 1_Medal_Tally.py
│   ├── 2_Overall_Analysis.py
│   ├── 3_Country_Analysis.py
│   └── 4_Athlete_Analysis.py
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── medal_analysis.py
│   ├── overall_analysis.py
│   ├── country_analysis.py
│   └── athlete_analysis.py
│
└── tests/
    ├── test_preprocessing.py
    ├── test_medal_analysis.py
    ├── test_overall_analysis.py
    ├── test_country_analysis.py
    └── test_athlete_analysis.py
```

## 📊 Dataset

The project uses historical Olympic athlete-event records and an NOC-to-region mapping file.

Expected local dataset files:

* `data/athlete_events.csv`
* `data/noc_regions.csv`

The dataset covers Summer Olympic Games from 1896 through 2016.

**Important:** The raw CSV files are excluded from Git by the project's `.gitignore`. Obtain the datasets separately and place them in the `data/` directory before running the application.

## ⚙️ Installation

### Prerequisites

* Python 3.12 recommended.
* Git.
* The project repository.
* The required CSV dataset files.

### 1. Clone the repository

```bash
git clone https://github.com/aryanmole8-tech/Olympics-Data-Analysis.git
cd Olympics-Data-Analysis
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -3.12 -m venv .venv
```

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run the following command in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again.

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Add the datasets

Place the required CSV files in the `data/` directory:

```text
data/
├── athlete_events.csv
└── noc_regions.csv
```

### 6. Start the dashboard

```powershell
python -m streamlit run app.py
```

Streamlit will display a local address in the terminal. Open that address in your browser to access the dashboard.

## 🧪 Testing

The project includes automated tests for data preprocessing and the analysis modules.

Run the complete test suite:

```powershell
python -m pytest tests/ -v
```

### Latest test result

The latest recorded test run completed successfully:

* **Tests passed:** 48
* **Tests failed:** 0
* **Execution time:** 1.88 seconds

These results reflect the test run performed during project development. Run the tests again after making changes to confirm the current state.

## 📈 Analytical Scope and Limitations

* The analysis covers Summer Olympic Games from 1896 to 2016.
* Medal counts are based on the project's implemented counting methodology.
* Team-event handling and historical NOC or region mappings can affect medal totals.
* Computed totals should not automatically be treated as official national Olympic medal-table figures.
* The dashboard's results depend on the source dataset and preprocessing rules.
* This is a historical analysis project, not a live Olympic results application.

## 🚀 Future Improvements

* Deploy the dashboard for public access.
* Add additional data validation and integration tests.
* Improve historical country and NOC mapping.
* Validate medal-counting methodology against authoritative Olympic records.
* Add downloadable reports and filtered data exports.
* Improve dashboard accessibility and responsive layout.
* Add automated deployment and continuous integration.

## 👨‍💻 Project Status

**Current stage:** Interactive dashboard implemented; automated unit tests passing.

The dashboard has four analysis pages and has been tested locally. Additional integration checks, medal methodology validation, and online deployment remain part of the finalization process.

## 📄 License

A license has not yet been specified. Add an appropriate license before distributing the project under explicit open-source terms.
