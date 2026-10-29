import streamlit as st
import plotly.express as px

from src.preprocessing import load_and_clean_data
from src.athlete_analysis import (
    get_gender_participation_trend,
    get_top_athletes,
)

st.set_page_config(
    page_title="Athlete Analysis",
    page_icon="🏃",
    layout="wide",
)

st.title("🏃 Olympics Athlete Analysis")

st.markdown(
    """
    Explore athlete participation and medal achievements
    in the Summer Olympic Games from 1896 to 2016.
    """
)


@st.cache_data
def load_data():
    return load_and_clean_data(data_dir="data", season="Summer")


try:
    df = load_data()

    if df.empty:
        st.warning("No Summer Olympics data is available.")
        st.stop()

    # --------------------------------------------------
    # 1. GENDER PARTICIPATION TRENDS
    # --------------------------------------------------

    st.subheader("👥 Gender Participation Trends")

    gender_trend = get_gender_participation_trend(df)

    if (
        gender_trend is not None
        and not gender_trend.empty
        and {"Year", "Male", "Female"}.issubset(
            gender_trend.columns
        )
    ):
        gender_long = gender_trend.melt(
            id_vars="Year",
            value_vars=["Male", "Female"],
            var_name="Gender",
            value_name="Athletes",
        )

        fig_gender = px.line(
            gender_long,
            x="Year",
            y="Athletes",
            color="Gender",
            markers=True,
            title="Male and Female Participation Over Time",
            color_discrete_map={
                "Male": "#2878B5",
                "Female": "#E75480",
            },
        )

        fig_gender.update_layout(
            xaxis_title="Olympic Year",
            yaxis_title="Number of Athletes",
            legend_title="Gender",
            hovermode="x unified",
        )

        st.plotly_chart(
            fig_gender,
            use_container_width=True,
        )
    else:
        st.info(
            "Gender participation trend data is unavailable "
            "or does not contain the expected columns."
        )

    # --------------------------------------------------
    # 2. TOP ATHLETES
    # --------------------------------------------------

    st.divider()
    st.subheader("🏆 Top Athletes")

    countries = sorted(
        df["region"].dropna().astype(str).unique().tolist()
    )

    country_options = ["All Countries"] + countries

    selected_country = st.selectbox(
        "Filter by country",
        country_options,
    )

    region_filter = (
        None
        if selected_country == "All Countries"
        else selected_country
    )

    athletes = get_top_athletes(
        df,
        top_n=10,
        region=region_filter,
    )

    if athletes is not None and not athletes.empty:
        expected_columns = {
            "Name",
            "region",
            "Gold",
            "Silver",
            "Bronze",
            "Total",
        }

        if expected_columns.issubset(athletes.columns):
            athletes = athletes.sort_values(
                "Total",
                ascending=False,
            )

            st.dataframe(
                athletes,
                use_container_width=True,
                hide_index=True,
            )

            chart_data = athletes.sort_values(
                "Total",
                ascending=True,
            )

            fig_athletes = px.bar(
                chart_data,
                x="Total",
                y="Name",
                orientation="h",
                color="Total",
                hover_data=[
                    "region",
                    "Gold",
                    "Silver",
                    "Bronze",
                ],
                title="Top 10 Athletes by Medal Records",
                labels={
                    "Name": "Athlete",
                    "Total": "Total Medal Records",
                    "region": "Country",
                },
                color_continuous_scale="Blues",
            )

            fig_athletes.update_layout(
                xaxis_title="Total Medal Records",
                yaxis_title="Athlete",
            )

            st.plotly_chart(
                fig_athletes,
                use_container_width=True,
            )
        else:
            st.warning(
                "The athlete analysis function returned "
                "unexpected columns."
            )
    else:
        st.info(
            "No athlete medal records were found for "
            "the selected country."
        )

    st.caption(
        "Olympics Data Analysis & Visualization Project"
    )

except Exception as e:
    st.error("Unable to load the Athlete Analysis dashboard.")
    st.exception(e)
