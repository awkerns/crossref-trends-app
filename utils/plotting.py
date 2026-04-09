import plotly.graph_objects as go


def create_color_map():
    """
    Define consistent color mapping for groups.
    """
    return {
        "Blue": "#1f77b4",
        "Green": "#2ca02c",
        "Red": "#d62728"
    }


def plot_crossref_trends(df_pivot, groups):
    """
    Create an interactive Plotly figure for Crossref trends.

    Parameters
    ----------
    df_pivot : pandas.DataFrame
        Pivot table with Years as index and phrases as columns
    groups : dict
        Dictionary of the form:
        {
            "Blue": [...phrases...],
            "Green": [...phrases...],
            "Red": [...phrases...]
        }

    Returns
    -------
    plotly.graph_objects.Figure
    """

    fig = go.Figure()
    color_map = create_color_map()

    for group_name, phrases in groups.items():
        color = color_map.get(group_name, "#333333")

        for phrase in phrases:
            if phrase in df_pivot.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df_pivot.index,
                        y=df_pivot[phrase],
                        mode="lines+markers",
                        name=phrase,
                        line=dict(color=color, width=2),
                        marker=dict(size=5),
                        hovertemplate=(
                            f"<b>{phrase}</b><br>"
                            "Year=%{x}<br>"
                            "Count=%{y}<extra></extra>"
                        ),
                    )
                )

    fig.update_layout(
        title="Crossref Publication Trends by Phrase",
        xaxis_title="Year",
        yaxis_title="Number of Publications",
        template="plotly_white",
        hovermode="x unified",
        legend_title="Phrases",
        height=700
    )

    fig.update_xaxes(showgrid=True, gridcolor="lightgray")
    fig.update_yaxes(showgrid=True, gridcolor="lightgray")

    return fig


def plot_with_optional_log_scale(fig, log_y=False):
    """
    Optionally convert y-axis to log scale.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
    log_y : bool

    Returns
    -------
    plotly.graph_objects.Figure
    """

    if log_y:
        fig.update_yaxes(type="log")

    return fig
