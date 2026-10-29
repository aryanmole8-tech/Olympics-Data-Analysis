import streamlit as st
import pandas as pd

from src.preprocessing import load_and_clean_data

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Olympics Data Analysis",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------
st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.7rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1.1rem;
            color: #777777;
            margin-bottom: 1.5rem;
        }

        .section-title {
            font-size: 1.6rem;
            font-weight: 700;
            margin-top: 1rem;
        }

        .feature-card {
            padding: 1.1rem;
            border: 1px solid rgba(128, 128, 128, 0.35);
            border-radius: 12px;
            min-height: 155px;
        }

        .feature-card h3 {
            margin-top: 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------
@st.cache_data
def load_data():
    """Load and clean Summer Olympics data."""
    return load_and_clean_data(
        data_dir="data",
        season="Summer",
    )


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    '<div class="main-title">🏅 Olympics Data Analysis</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        Explore Olympic history through data, statistics, and interactive visualizations.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

st.write(
    """
    Welcome to the **Olympics Data Analysis & Visualization Dashboard**.

    This project analyzes historical Summer Olympic Games data to explore
    medal achievements, participation trends, country performance, and
    athlete statistics.
    """
)

# --------------------------------------------------
# LOAD DATA AND DISPLAY KEY METRICS
# --------------------------------------------------
try:
    df = load_data()

    if df.empty:
        st.error(
            "The dataset loaded successfully, but it contains no records. "
            "Please check your dataset and preprocessing configuration."
        )
        st.stop()

    years = sorted(
        pd.to_numeric(df["Year"], errors="coerce")
        .dropna()
        .astype(int)
        .unique()
    )

    countries = (
        df["region"].dropna().nunique()
        if "region" in df.columns
        else 0
    )

    sports = (
        df["Sport"].dropna().nunique()
        if "Sport" in df.columns
        else 0
    )

    athletes = (
        df["ID"].nunique()
        if "ID" in df.columns
        else 0
    )

    st.markdown(
        '<div class="section-title">📊 Dataset Overview</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Olympic Editions", len(years))

    with col2:
        st.metric(
            "Participating Countries / Regions",
            f"{countries:,}",
        )

    with col3:
        st.metric("Sports", f"{sports:,}")

    with col4:
        st.metric("Unique Athletes", f"{athletes:,}")

    if years:
        st.caption(
            f"Dataset coverage: {min(years)}–{max(years)}. "
            "These figures are calculated from the cleaned dataset."
        )

except FileNotFoundError:
    st.error(
        "Olympics dataset not found. Make sure the required CSV files "
        "are present inside the project's data/ directory."
    )
    st.stop()

except Exception as exc:
    st.error(
        "The dashboard could not load the dataset. "
        "Check the dataset files, Python environment, and preprocessing module."
    )
    st.exception(exc)
    st.stop()

# --------------------------------------------------
# DASHBOARD FEATURES
# --------------------------------------------------
st.markdown("---")

st.markdown(
    '<div class="section-title">🧭 Explore the Dashboard</div>',
    unsafe_allow_html=True,
)

st.write(
    "Select a page from the sidebar to explore a specific area of Olympic data."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🥇 Medal Tally</h3>
            Explore gold, silver, and bronze medals by Olympic year
            and country. Compare country medal performance.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="feature-card">
            <h3>🌍 Country Analysis</h3>
            Investigate a country's medal history, performance trends,
            and most successful sports.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <h3>📈 Overall Analysis</h3>
            Examine Olympic participation, countries, sports,
            events, and athlete trends over time.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="feature-card">
            <h3>🏃 Athlete Analysis</h3>
            Explore athlete participation by gender and identify
            top-performing athletes.
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# PROJECT OBJECTIVES
# --------------------------------------------------
st.markdown("---")

st.markdown(
    '<div class="section-title">🎯 Project Objectives</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    - Analyze historical Summer Olympics data.
    - Compare medal achievements across countries and Olympic editions.
    - Understand participation trends across athletes, countries, and sports.
    - Explore country-level performance and athlete achievements.
    - Present findings through interactive tables, charts, and statistics.
    """
)

# --------------------------------------------------
# TECHNOLOGIES
# --------------------------------------------------
st.markdown("---")

st.markdown(
    '<div class="section-title">🛠️ Technologies Used</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    **Python** · **Pandas** · **Streamlit** · **Plotly** · **Matplotlib**
    · **Seaborn** · **Pytest**
    """
)

st.info(
    "Note: The dataset covers the historical Summer Olympic Games "
    "through 2016. The dashboard describes the records available in "
    "the project dataset, not live Olympic results."
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")

st.caption(
    "Olympics Data Analysis & Visualization | "
    "Educational Data Analytics Project"
)
