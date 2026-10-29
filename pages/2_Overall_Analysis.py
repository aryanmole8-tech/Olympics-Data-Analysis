import streamlit as st
import plotly.express as px

from src.preprocessing import load_and_clean_data
from src.overall_analysis import (
    get_overall_stats,
    get_participation_trend,
)

st.set_page_config(
    page_title="Overall Olympics Analysis",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Overall Olympics Analysis")

st.markdown(
    "Explore the history and participation trends of the "
    "Summer Olympic Games from 1896 to 2016."
)


@st.cache_data
def load_data():
    return load_and_clean_data(data_dir="data", season="Summer")


try:
    df = load_data()

    if df.empty:
        st.warning("No Summer Olympics data was found.")
        st.stop()

    # Sidebar filter
    st.sidebar.header("Analysis Filters")

    years = sorted(df["Year"].dropna().astype(int).unique().tolist())

    selected_year = st.sidebar.selectbox(
        "Select Olympic year",
        ["All Years"] + years,
    )

    filtered_df = df.copy()

    if selected_year != "All Years":
        filtered_df = filtered_df[
            filtered_df["Year"] == selected_year
        ]

    # Olympics at a Glance
    stats = get_overall_stats(filtered_df)

    st.subheader("🏅 Olympics at a Glance")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Editions", stats["editions"])
    col2.metric("Nations", stats["nations"])
    col3.metric("Sports", stats["sports"])
    col4.metric("Events", stats["events"])
    col5.metric("Athletes", f'{stats["athletes"]:,}')

    if selected_year == "All Years":
        st.caption("Statistics cover all available Summer Olympic editions.")
    else:
        st.caption(f"Statistics for the {selected_year} Summer Olympics.")

    st.divider()

    # Participation Trends
    st.subheader("📈 Participation Trends")

    trend = get_participation_trend(df)

    if not trend.empty:
        fig_nations = px.line(
            trend,
            x="Year",
            y="Nations",
            markers=True,
            title="Participating Nations Over Time",
            labels={
                "Year": "Olympic Year",
                "Nations": "Number of Nations",
            },
        )

        fig_nations.update_layout(
            xaxis=dict(dtick=8),
            hovermode="x unified",
        )

        st.plotly_chart(fig_nations, width="stretch")

        fig_athletes = px.line(
            trend,
            x="Year",
            y="Athletes",
            markers=True,
            title="Athlete Participation Over Time",
            labels={
                "Year": "Olympic Year",
                "Athletes": "Number of Athletes",
            },
        )

        fig_athletes.update_layout(
            xaxis=dict(dtick=8),
            hovermode="x unified",
        )

        st.plotly_chart(fig_athletes, width="stretch")

    else:
        st.info("No participation trend data is available.")

except Exception as e:
    st.error("Unable to load the Overall Olympics Analysis dashboard.")
    st.exception(e)

st.divider()
st.caption("Olympics Data Analysis & Visualization Project")
