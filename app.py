import streamlit as st
import numpy as np

st.title("Crossref Phrase Trend Explorer")

# --- User Inputs ---
st.sidebar.header("Input Parameters")

blue_terms = st.sidebar.text_area("Blue group (comma-separated)")
green_terms = st.sidebar.text_area("Green group (comma-separated)")
red_terms = st.sidebar.text_area("Red group (comma-separated)")

start_year, end_year = st.sidebar.slider(
    "Select year range",
    1950, 2025, (2000, 2020)
)

run_button = st.sidebar.button("Run Analysis")

# --- Process Inputs ---
def parse_terms(text):
    return [t.strip() for t in text.split(",") if t.strip()]

if run_button:
    phrases = (
        parse_terms(blue_terms)
        + parse_terms(green_terms)
        + parse_terms(red_terms)
    )

    years = list(range(start_year, end_year + 1))

    st.write(f"Running query for {len(phrases)} phrases...")

    rows = get_crossref_counts(phrases, years)
    df_pivot = build_pivot(rows)

    color_groups = {
        "Blue": (parse_terms(blue_terms), ["#1f77b4"] * 20),
        "Green": (parse_terms(green_terms), ["#2ca02c"] * 20),
        "Red": (parse_terms(red_terms), ["#d62728"] * 20),
    }

    fig = plot_results(df_pivot, color_groups)
    st.pyplot(fig)

    st.download_button(
        "Download CSV",
        df_pivot.to_csv().encode("utf-8"),
        "crossref_results.csv"
    )
