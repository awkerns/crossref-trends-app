import streamlit as st
import requests
import pandas as pd
import time
import plotly.graph_objects as go

# =========================
# Crossref Query Function
# =========================
@st.cache_data(show_spinner=False)
def get_crossref_counts(phrases, years, sleep=0.5):
    rows = []

    progress = st.progress(0)
    total = len(phrases) * len(years)
    counter = 0

    for phrase in phrases:
        for y in years:
            url = "https://api.crossref.org/works"
            params = {
                "query.bibliographic": f'"{phrase}"',
                "filter": f"from-pub-date:{y}-01-01,until-pub-date:{y}-12-31",
                "rows": 0
            }

            try:
                r = requests.get(url, params=params, timeout=15)
                r.raise_for_status()
                count = r.json()["message"].get("total-results", 0)
            except Exception:
                count = 0

            rows.append({"Year": y, "Phrase": phrase, "Count": count})

            counter += 1
            progress.progress(counter / total)

            time.sleep(sleep)

    return rows


# =========================
# Data Processing
# =========================
def build_pivot(rows):
    df = pd.DataFrame(rows)
    df_pivot = df.pivot(index="Year", columns="Phrase", values="Count")
    return df_pivot.fillna(0).astype(int)


# =========================
# Plotly Plot Function
# =========================
def plot_results(df_pivot, groups):
    fig = go.Figure()

    color_map = {
        "Blue": "#1f77b4",
        "Green": "#2ca02c",
        "Red": "#d62728"
    }

    for group_name, phrases in groups.items():
        color = color_map[group_name]

        for phrase in phrases:
            if phrase in df_pivot.columns:
                fig.add_trace(go.Scatter(
                    x=df_pivot.index,
                    y=df_pivot[phrase],
                    mode="lines+markers",
                    name=phrase,
                    line=dict(color=color, width=2),
                    marker=dict(size=5),
                    hovertemplate=f"{phrase}<br>Year=%{{x}}<br>Count=%{{y}}<extra></extra>"
                ))

    fig.update_layout(
        title="Crossref Publication Trends by Phrase",
        xaxis_title="Year",
        yaxis_title="Number of Publications",
        template="plotly_white",
        hovermode="x unified",
        legend_title="Phrases",
        height=700
    )

    return fig


# =========================
# Streamlit UI
# =========================
st.title("Crossref Phrase Trend Explorer")

st.sidebar.header("Inputs")

blue_terms = st.sidebar.text_area("Blue group (comma-separated)")
green_terms = st.sidebar.text_area("Green group (comma-separated)")
red_terms = st.sidebar.text_area("Red group (comma-separated)")

start_year, end_year = st.sidebar.slider(
    "Select year range",
    1950, 2025, (2000, 2020)
)

run_button = st.sidebar.button("Run Analysis")


def parse_terms(text):
    return [t.strip() for t in text.split(",") if t.strip()]


if run_button:
    blue_list = parse_terms(blue_terms)
    green_list = parse_terms(green_terms)
    red_list = parse_terms(red_terms)

    phrases = blue_list + green_list + red_list

    if len(phrases) == 0:
        st.warning("Please enter at least one phrase.")
        st.stop()

    years = list(range(start_year, end_year + 1))

    st.write(f"Querying Crossref for {len(phrases)} phrases...")

    rows = get_crossref_counts(phrases, years)
    df_pivot = build_pivot(rows)

    groups = {
        "Blue": blue_list,
        "Green": green_list,
        "Red": red_list
    }

    fig = plot_results(df_pivot, groups)

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Data Table")
    st.dataframe(df_pivot)

    st.download_button(
        "Download CSV",
        df_pivot.to_csv().encode("utf-8"),
        "crossref_phrase_counts.csv",
        "text/csv"
    )
