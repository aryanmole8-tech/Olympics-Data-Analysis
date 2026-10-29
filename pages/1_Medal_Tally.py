import streamlit as st
import plotly.express as px

from src.preprocessing import load_and_clean_data
from src.medal_analysis import get_medal_tally


st.set_page_config(
    page_title="Olympics Medal Tally",
    page_icon="🥇",
    layout="wide"
)

st.title("🥇 Olympics Medal Tally")
st.markdown(
    "Explore medal achievements across the Summer Olympic Games "
    "from 1896 to 2016."
)


@st.cache_data
def load_data():
    return load_and_clean_data()


try:
    df = load_data()

    # Sidebar filters
    st.sidebar.header("Medal Tally Filters")

    available_years = sorted(
        df["Year"].dropna().astype(int).unique().tolist()
    )

    selected_year = st.sidebar.selectbox(
        "Select Olympic year",
        ["All Years"] + available_years,
        index=0
    )

    available_countries = sorted(
        df["region"].dropna().astype(str).unique().tolist()
    )

    selected_country = st.sidebar.selectbox(
        "Select country",
        ["All Countries"] + available_countries,
        index=0
    )

    year_filter = (
        None if selected_year == "All Years"
        else int(selected_year)
    )

    country_filter = (
        None if selected_country == "All Countries"
        else selected_country
    )

    # Calculate medal tally using the existing analysis function
    medal_df = get_medal_tally(
        df,
        year=year_filter,
        region=country_filter
    )

    if medal_df.empty:
        st.warning("No medal data is available for these filters.")

    else:
        medal_df = medal_df.sort_values(
            "Total", ascending=False
        ).reset_index(drop=True)

        # Medal statistics for the selected filters
        st.subheader("🏆 Medal Statistics")

        total_gold = int(medal_df["Gold"].sum())
        total_silver = int(medal_df["Silver"].sum())
        total_bronze = int(medal_df["Bronze"].sum())
        total_medals = int(medal_df["Total"].sum())

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("🥇 Gold", f"{total_gold:,}")
        col2.metric("🥈 Silver", f"{total_silver:,}")
        col3.metric("🥉 Bronze", f"{total_bronze:,}")
        col4.metric("🏅 Total Medals", f"{total_medals:,}")

        st.divider()

        # Country medal rankings for the selected filters
        st.subheader("🌍 Country Medal Rankings")

        st.dataframe(
            medal_df,
            use_container_width=True,
            hide_index=True
        )

        # Top 10 countries chart
        # This ranking is independent of the selected country.
        st.subheader("📊 Top 10 Countries by Total Medals")

        ranking_df = get_medal_tally(
            df,
            year=year_filter,
            region=None
        )

        if ranking_df.empty:
            st.info("No country ranking data is available.")
        else:
            top_countries = (
                ranking_df.sort_values(
                    "Total", ascending=False
                )
                .head(10)
                .sort_values("Total", ascending=True)
            )

            fig = px.bar(
                top_countries,
                x="Total",
                y="region",
                orientation="h",
                color="Total",
                hover_data=["Gold", "Silver", "Bronze"],
                labels={
                    "region": "Country",
                    "Total": "Total Medals"
                },
                title="Top 10 Countries by Total Medals"
            )

            fig.update_layout(
                yaxis_title="Country",
                xaxis_title="Total Medals",
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # Gold, silver, and bronze comparison
        st.subheader("🥇🥈🥉 Medal Type Comparison")

        top_medal_countries = medal_df.head(10)

        fig_medals = px.bar(
            top_medal_countries,
            x="region",
            y=["Gold", "Silver", "Bronze"],
            barmode="group",
            labels={
                "region": "Country",
                "value": "Medals",
                "variable": "Medal Type"
            },
            title="Gold, Silver and Bronze Medals"
        )

        st.plotly_chart(
            fig_medals,
            use_container_width=True
        )

        st.caption(
            "Medal totals depend on the project's existing medal "
            "counting methodology. Team-event totals may be estimates."
        )

except Exception:
    st.error("Unable to load the Medal Tally dashboard.")
    st.exception(Exception)

st.divider()
st.caption("Olympics Data Analysis & Visualization Project")

