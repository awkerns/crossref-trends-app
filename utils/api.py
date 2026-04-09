import requests
import time


BASE_URL = "https://api.crossref.org/works"


def query_crossref(phrase, year):
    """
    Query Crossref for a single phrase and year.
    Returns the total number of matching publications.
    """

    params = {
        "query.bibliographic": f'"{phrase}"',
        "filter": f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31",
        "rows": 0
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data["message"].get("total-results", 0)

    except Exception:
        return 0


def get_crossref_counts(phrases, years, sleep=0.5, progress_callback=None):
    """
    Query Crossref for multiple phrases across multiple years.

    Parameters
    ----------
    phrases : list of str
    years : list of int
    sleep : float
        Delay between API calls (rate limiting)
    progress_callback : callable (optional)
        Function to report progress (for UI frameworks like Streamlit)

    Returns
    -------
    list of dict
        Each dict contains: Year, Phrase, Count
    """

    rows = []
    total_calls = len(phrases) * len(years)
    completed = 0

    for phrase in phrases:
        for year in years:
            count = query_crossref(phrase, year)

            rows.append({
                "Year": year,
                "Phrase": phrase,
                "Count": count
            })

            completed += 1

            if progress_callback is not None:
                progress_callback(completed / total_calls)

            time.sleep(sleep)

    return rows
