import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Olympics Data Analysis",
    page_icon="🏅",
    layout="wide"
)

# Dashboard title
st.title("🏅 Olympics Data Analysis & Visualization")

st.markdown(
    """
    Welcome to the Olympics Data Analysis Dashboard!

    Explore Summer Olympic Games data from **1896 to 2016**.

    ### 📊 Dashboard Features
    - 🥇 Medal Tally
    - 🌍 Overall Olympics Analysis
    - 🏳️ Country Analysis
    - 🏃 Athlete Analysis
    """
)

st.info(
    "Dashboard development is in progress. "
    "The analysis modules and dataset will be connected in upcoming steps."
)

st.caption("Project: Olympics Data Analysis & Visualization")