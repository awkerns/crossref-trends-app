import pandas as pd


def build_dataframe(rows):
    """
    Convert raw API results into a DataFrame.

    Parameters
    ----------
    rows : list of dict
        Each dict contains:
        {
            "Year": int,
            "Phrase": str,
            "Count": int
        }

    Returns
    -------
    pandas.DataFrame
    """
    return pd.DataFrame(rows)


def pivot_data(df):
    """
    Pivot long-format data into wide format.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain columns: Year, Phrase, Count

    Returns
    -------
    pandas.DataFrame
        Index = Year
        Columns = Phrase
        Values = Count
    """
    df_pivot = df.pivot(index="Year", columns="Phrase", values="Count")
    return df_pivot.fillna(0).astype(int)


def normalize_by_year(df_pivot):
    """
    Normalize counts within each year (row-wise).

    Useful to compare relative usage across phrases.

    Returns
    -------
    pandas.DataFrame
    """
    return df_pivot.div(df_pivot.sum(axis=1), axis=0).fillna(0)


def moving_average(df_pivot, window=3):
    """
    Apply a moving average smoothing over time.

    Parameters
    ----------
    df_pivot : pandas.DataFrame
    window : int

    Returns
    -------
    pandas.DataFrame
    """
    return df_pivot.rolling(window=window, min_periods=1).mean()


def compute_log_transform(df_pivot):
    """
    Apply log transform to stabilize variance.

    Adds 1 to avoid log(0).

    Returns
    -------
    pandas.DataFrame
    """
    import numpy as np
    return np.log1p(df_pivot)


def compute_summary_stats(df_pivot):
    """
    Compute basic summary statistics per phrase.

    Returns
    -------
    pandas.DataFrame
    """
    return pd.DataFrame({
        "mean": df_pivot.mean(),
        "std": df_pivot.std(),
        "min": df_pivot.min(),
        "max": df_pivot.max(),
        "total": df_pivot.sum()
    })
