import streamlit as st
import plotly.express as px

from src.preprocessing import load_and_clean_data
from src.country_analysis import (
    get_country_medal_trend,
    get_top_sports,
)

st.set_page_config(
    page_title="Country Analysis",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 Country-wise Olympics Analysis")

st.markdown(
    """
    Explore the Olympic performance of individual countries.

    Select a country to explore its medal history and
    most successful sports from 1896 to 2016.
    """
)


# --------------------------------------------------
# 1. LOAD AND PREPARE DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return load_and_clean_data(data_dir="data", season="Summer")


try:
    df = load_data()

    if df.empty:
        st.warning("No Summer Olympics data is available.")
        st.stop()

    countries = sorted(
        df["region"].dropna().unique().tolist()
    )

    if not countries:
        st.warning("No countries were found in the dataset.")
        st.stop()

    # --------------------------------------------------
    # 2. COUNTRY SELECTION
    # --------------------------------------------------

    preferred_countries = [
        "India",
        "USA",
        "UK",
        "China",
        "Australia",
    ]

    default_country = next(
        (
            name
            for name in preferred_countries
            if name in countries
        ),
        countries[0],
    )

    country = st.selectbox(
        "Select a country",
        countries,
        index=countries.index(default_country),
    )

    # --------------------------------------------------
    # 3. MEDAL PERFORMANCE
    # --------------------------------------------------

    st.subheader(f"🏅 Medal Performance: {country}")

    country_df = df[df["region"] == country]

    medal_df = country_df[
        country_df["Medal"].notna()
    ]

    gold = int((medal_df["Medal"] == "Gold").sum())
    silver = int((medal_df["Medal"] == "Silver").sum())
    bronze = int((medal_df["Medal"] == "Bronze").sum())
    total = gold + silver + bronze

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🥇 Gold Medals", f"{gold:,}")
    col2.metric("🥈 Silver Medals", f"{silver:,}")
    col3.metric("🥉 Bronze Medals", f"{bronze:,}")
    col4.metric("🏅 Total Medals", f"{total:,}")

    st.caption(
        "Medal totals are calculated from the dataset's "
        "medal records. Team-event counting may differ "
        "from official national medal-table totals."
    )

    # --------------------------------------------------
    # 4. MEDAL TRENDS OVER TIME
    # --------------------------------------------------

    st.divider()
    st.subheader("📈 Medal Trends Over Time")

    trend = get_country_medal_trend(
        df,
        region=country,
    )

    if trend is not None and not trend.empty:
        required = {"Year", "Gold", "Silver", "Bronze"}
        
        if required.issubset(trend.columns):
            trend_long = trend.melt(
                id_vars="Year",
                value_vars=["Gold", "Silver", "Bronze"],
                var_name="Medal Type",
                value_name="Medals",
            )

            fig_trend = px.line(
                trend_long,
                x="Year",
                y="Medals",
                color="Medal Type",
                markers=True,
                title=f"Medal History of {country}",
                color_discrete_map={
                    "Gold": "#D4AF37",
                    "Silver": "#A7A9AC",
                    "Bronze": "#CD7F32",
                },
            )

            fig_trend.update_layout(
                xaxis_title="Olympic Year",
                yaxis_title="Number of Medals",
                legend_title="Medal Type",
                hovermode="x unified",
            )

            st.plotly_chart(
                fig_trend,
                use_container_width=True,
            )
        else:
            st.warning(
                "The medal trend data does not contain "
                "the expected columns."
            )
    else:
        st.info(
            f"No medal trend data is available for {country}."
        )

    # --------------------------------------------------
    # 5. TOP SPORTS
    # --------------------------------------------------

    st.divider()
    st.subheader("🏆 Top Sports")

    top_sports = get_top_sports(
        df,
        region=country,
        top_n=10,
    )

    if top_sports is not None and not top_sports.empty:
        if {"Sport", "Total"}.issubset(top_sports.columns):
            fig_sports = px.bar(
                top_sports.sort_values("Total"),
                x="Total",
                y="Sport",
                orientation="h",
                title=f"Top Sports for {country}",
                labels={
                    "Total": "Medal Records",
                    "Sport": "Sport",
                },
                color="Total",
                color_continuous_scale="Blues",
            )

            st.plotly_chart(
                fig_sports,
                use_container_width=True,
            )

            st.dataframe(
                top_sports,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.warning(
                "The top sports data does not contain "
                "the expected Sport and Total columns."
            )
    else:
        st.info(
            f"No top sports data is available for {country}."
        )

    st.caption(
        "Olympics Data Analysis & Visualization Project"
    )

except Exception as e:
    st.error("Unable to load the Country Analysis dashboard.")
    st.exception(e)

