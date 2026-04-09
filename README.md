# Crossref Phrase Trend Explorer

An interactive Python web application for analyzing publication trends over time using the Crossref API. Users can input custom search phrases, organize them into thematic groups, and visualize how terminology evolves across years.

---

## Overview

This tool queries the Crossref database and aggregates publication counts for user-defined phrases across a selected time range. It then generates interactive visualizations to explore trends in scientific terminology, research topics, and field evolution.

Built with:

- Python
- Streamlit
- Plotly
- Pandas
- Requests

---

## Features

- Custom phrase input (up to three groups)
- Time range selection via slider
- Real-time querying of Crossref metadata
- Interactive Plotly visualizations
- Color-coded phrase groups:
  - Blue: Core concepts
  - Green: Interaction / intensity concepts
  - Red: PGF / PGFL-related terms
- Downloadable results as CSV
- Modular, research-ready codebase

---

## Project Structure

crossref-trends-app/
│
├── app.py # Streamlit application
├── api.py # Crossref API interface
├── data.py # Data processing and transformation
├── plotting.py # Visualization functions
├── requirements.txt # Dependencies
└── README.md


---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/crossref-trends-app.git
cd crossref-trends-app
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
streamlit run app.py
http://localhost:8501
```

## Usage
Enter comma-separated phrases in each group (Blue, Green, Red).
Select a year range using the slider.
Click Run Analysis.
Explore the interactive plot.
Download results as a CSV if needed.

### Example Use Cases
Tracking the evolution of statistical terminology (e.g., “Cox process”, “PGFL”)
Bibliometric analysis of research fields
Identifying emerging vs. declining concepts
Comparing methodological vs. applied terminology

## Data Source
All data is retrieved from the Crossref API.

## Limitations
Subject to Crossref API rate limits
Query results depend on exact phrase matching
Counts reflect metadata matches, not full-text occurrences
Large queries may take time due to API throttling

## Potential Extensions
Log-scale visualization
Moving average smoothing
Normalization by total publications per year
Trend estimation and statistical inference
Change-point detection
Parallelized API queries
Advanced modeling (e.g., time series, Bayesian approaches)
