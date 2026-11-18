"""How Origin Shapes Wine: Style, Price & Reputation.

Lab 2 vibe-coding dashboard: choropleth of average critic points by
country, a dual-mode bar (style mix vs underrated provinces), and a
log-price vs points density heatmap.

Engineering patterns (single cached load, pure filter function,
empty-state placeholder) adapted from the course-provided example
dashboard; design and charts are our own.
"""
from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

from src.data_loader import (
    CATEGORY_ORDER,
    get_country_options,
    get_price_bounds,
    load_wine_data,
)

# 酒主题配色:连续色阶 luminance 单调(奶油→琥珀→酒红→深 burgundy),
# 类别色板在白色卡片上保持区分度与对比(L02:sequential 表量级、categorical 表类别)
WINE_SCALE = ["#faf3e3", "#e9c46a", "#c1663e", "#8e3b52", "#4a1226"]
CATEGORY_COLORS = {
    "red": "#9b2226",
    "white": "#ddc173",
    "rose": "#f4acb7",
    "sparkling": "#81b29a",
    "dessert": "#ca6702",
    "other": "#adb5bd",
}
BAR_MODES = [
    {"label": "Style mix by country", "value": "mix"},
    {"label": "Underrated provinces", "value": "value"},
]
MIN_PROVINCE_BOTTLES = 200  # 性价比排名的小样本门槛(统计诚信)

FIG_FONT = dict(family="'Inter', 'PingFang SC', -apple-system, 'Segoe UI', sans-serif")


@lru_cache(maxsize=1)
def get_data() -> pd.DataFrame:
    return load_wine_data()


def base_layout(fig, title: str, height: int):
    fig.update_layout(
        template="plotly_white",
        font=FIG_FONT,
        title=dict(text=title, font=dict(size=16, color="#4a1226")),
        height=height,
        margin=dict(l=20, r=20, t=56, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        transition_duration=400,
    )
    return fig


def apply_filters(
    df: pd.DataFrame,
    countries: list[str] | None,
    category: str | None,
    price_range: list[float],
    include_countries: bool = True,
) -> pd.DataFrame:
    filtered = df
    if include_countries and countries:
        filtered = filtered.loc[filtered["country_display"].isin(countries)]
    if category and category != "__all__":
        filtered = filtered.loc[filtered["category"] == category]
    lo, hi = price_range
    # price 为 NaN 的行在全局视图保留;只有显式缩小区间时才过滤价格
    if lo > PRICE_MIN or hi < PRICE_MAX:
        filtered = filtered.loc[
            filtered["price"].between(lo, hi, inclusive="both")
        ]
    return filtered


def empty_figure(message: str):
    fig = px.scatter()
    base_layout(fig, "", 420)
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[
            dict(
                text=message, x=0.5, y=0.5, xref="paper", yref="paper",
                showarrow=False, font=dict(size=15, color="#adb5bd"),
            )
        ],
    )
    return fig


def make_map_figure(df: pd.DataFrame):
    summary = (
        df.loc[df["country_display"] != "Unknown"]
        .groupby("country_display", as_index=False)
        .agg(
            avg_points=("points", "mean"),
            bottles=("id", "count"),
            median_price=("price", "median"),
            top_variety=("variety", lambda s: s.value_counts().idxmax()),
        )
    )
    if summary.empty:
        return empty_figure("No country data for the current filters.")

    fig = px.choropleth(
        summary,
        locations="country_display",
        locationmode="country names",
        color="avg_points",
        hover_name="country_display",
        hover_data={
            "avg_points": ":.2f",
            "bottles": ":,",
            "median_price": ":.0f",
            "top_variety": True,
            "country_display": False,
        },
        color_continuous_scale=WINE_SCALE,
        labels={
            "avg_points": "Avg points",
            "median_price": "Median price ($)",
            "top_variety": "Top variety",
        },
    )
    base_layout(fig, "Which countries score highest on average?", 440)
    fig.update_layout(
        margin=dict(l=0, r=0, t=56, b=0),
        coloraxis_colorbar=dict(
            title="Avg points", tickfont=dict(size=11),
            outlinecolor="#e9ecef", outlinewidth=1,
        ),
    )
    fig.update_geos(
        showframe=False, showcoastlines=False, projection_type="natural earth",
        landcolor="#f1f3f5", oceancolor="#fdfbf7", showocean=True,
    )
    return fig


def make_mix_figure(df: pd.DataFrame):
    counts = (
        df.loc[df["country_display"] != "Unknown"]
        .groupby(["country_display", "category"], observed=True)
        .size()
        .reset_index(name="n")
    )
    if counts.empty:
        return empty_figure("No data for the current filters.")

    top_countries = (
        counts.groupby("country_display")["n"].sum()
        .sort_values(ascending=False).head(10).index
    )
    counts = counts.loc[counts["country_display"].isin(top_countries)]
    totals = counts.groupby("country_display")["n"].transform("sum")
    counts["percent"] = counts["n"] / totals * 100
    order = (
        counts.groupby("country_display")["n"].sum()
        .sort_values(ascending=False).index.tolist()
    )

    fig = px.bar(
        counts, x="country_display", y="percent", color="category",
        custom_data=["n"],
        category_orders={"category": CATEGORY_ORDER, "country_display": order},
        color_discrete_map=CATEGORY_COLORS,
        labels={"percent": "Share of bottles (%)", "country_display": ""},
    )
    fig.update_traces(
        hovertemplate="%{customdata[0]:,} bottles · %{y:.1f}%<extra>%{fullData.name}</extra>",
        marker_line_color="#ffffff", marker_line_width=0.6,
    )
    base_layout(
        fig,
        "How does each origin's style mix differ? (top 10 countries by volume)",
        420,
    )
    # 图例放右侧竖排,与标题拉开;bargap 让柱子细一点
    fig.update_layout(
        bargap=0.38,
        legend_title_text="",
        legend=dict(font=dict(size=12), yanchor="top", y=0.98, xanchor="left", x=1.02),
        margin=dict(l=20, r=110, t=56, b=20),
    )
    return fig


def make_value_figure(df: pd.DataFrame):
    priced = df.dropna(subset=["price"])
    grouped = (
        priced.loc[priced["province"] != "Unknown"]
        .groupby("province", as_index=False)
        .agg(
            bottles=("id", "count"),
            avg_points=("points", "mean"),
            median_price=("price", "median"),
        )
    )
    grouped = grouped.loc[grouped["bottles"] >= MIN_PROVINCE_BOTTLES]
    if grouped.empty:
        return empty_figure("No province data for the current filters.")

    grouped["value_score"] = grouped["avg_points"] / grouped["median_price"]
    top = grouped.sort_values("value_score", ascending=False).head(15)

    fig = px.bar(
        top.sort_values("value_score"),
        x="value_score", y="province", orientation="h",
        color="avg_points", color_continuous_scale=WINE_SCALE,
        custom_data=["bottles", "avg_points", "median_price"],
        labels={
            "value_score": "Value score (avg points / median price)",
            "province": "",
        },
    )
    fig.update_traces(
        hovertemplate=(
            "%{customdata[1]:.1f} pts · $%{customdata[2]:.0f} median · "
            "%{customdata[0]:,} bottles<extra>%{y}</extra>"
        ),
        marker_line_color="#ffffff", marker_line_width=0.6,
    )
    base_layout(
        fig,
        "Which provinces are underrated? "
        f"(avg points per median $, min {MIN_PROVINCE_BOTTLES} bottles)",
        460,
    )
    fig.update_layout(
        bargap=0.38,
        coloraxis_colorbar=dict(title="Avg points", tickfont=dict(size=11)),
    )
    return fig


def make_heatmap_figure(df: pd.DataFrame):
    priced = df.dropna(subset=["price"]).copy()
    if priced.empty:
        return empty_figure("No price data for the current filters.")

    priced["log_price"] = np.log10(priced["price"])
    r = np.corrcoef(priced["log_price"], priced["points"])[0, 1]

    fig = px.density_heatmap(
        priced, x="log_price", y="points", nbinsx=40, nbinsy=21,
        color_continuous_scale=WINE_SCALE,
        labels={"log_price": "Price ($)", "points": "Critic points"},
    )
    # 把 log 轴刻度翻译回美元
    ticks = [4, 10, 25, 50, 100, 200, 500, 1000, 3300]
    fig.update_xaxes(
        tickmode="array",
        tickvals=[np.log10(t) for t in ticks],
        ticktext=[f"${t:,}" for t in ticks],
    )
    fig.update_traces(
        hovertemplate="%{z:,.0f} bottles in this bin · %{y} pts<extra></extra>"
    )
    # 空格子落回色阶底端(奶油色)——空即空,不与密区争注意力
    fig.update_coloraxes(cmin=1)

    # OLS 趋势线:只画在数据主体覆盖的价格区间(1–99 分位),
    # 不向稀疏的高价长尾外推;浅色细线,只作参考、不抢密度云的主角
    slope, intercept = np.polyfit(priced["log_price"], priced["points"], 1)
    x_lo, x_hi = priced["log_price"].quantile([0.01, 0.99])
    xs = np.array([x_lo, x_hi])
    fig.add_trace(
        go.Scatter(
            x=xs, y=slope * xs + intercept,
            mode="lines", name="OLS trend",
            line=dict(color="rgba(74,18,38,0.5)", width=2, dash="dash"),
            hovertemplate=(
                f"trend: points ≈ {slope:.1f}·log₁₀(price) + {intercept:.1f}"
                "<extra></extra>"
            ),
        )
    )
    base_layout(
        fig,
        f"Do expensive wines really score higher? (Pearson r = {r:.2f})",
        430,
    )
    fig.update_layout(
        coloraxis_colorbar=dict(title="Bottles", tickfont=dict(size=11)),
        showlegend=True,
        legend=dict(
            x=0.98, y=0.02, xanchor="right", yanchor="bottom",
            bgcolor="rgba(255,253,249,0.85)", font=dict(size=12),
        ),
    )
    return fig


def make_slice_stats(df: pd.DataFrame) -> list:
    """动态切片摘要条:随过滤器实时更新的一行数字芯片。"""
    if df.empty:
        chips = ["0 bottles"]
    else:
        n = len(df)
        avg = df["points"].mean()
        med_price = df["price"].median()
        n_countries = df.loc[df["country_display"] != "Unknown",
                             "country_display"].nunique()
        top_cat = df["category"].value_counts().idxmax()
        chips = [
            f"{n:,} bottles",
            f"avg {avg:.1f} pts",
            f"median ${med_price:,.0f}" if pd.notna(med_price) else "no price data",
            f"{n_countries} countries",
            f"top category: {top_cat}",
        ]
    return [html.Span(chip, className="stat-chip") for chip in chips]


data = get_data()
PRICE_MIN, PRICE_MAX = get_price_bounds(data)
# 线性轴上低价区挤在一起:刻度只留两档,并用内联样式上色(版本无关,不吃 CSS class 变化)
PRICE_MARKS = {
    t: {"label": f"${t:,}", "style": {"color": "#d9c3ae", "fontSize": 11}}
    for t in [500, 3300]
}

app = Dash(__name__, title="Wine Origin Dashboard")
server = app.server

app.layout = html.Div(
    className="page",
    children=[
        html.Header(
            className="page-header",
            children=[
                html.P("COMP7507 · Wine review explorer", className="eyebrow"),
                html.H1("How Origin Shapes Wine"),
                html.P(
                    "Style, price and critic reputation across 43 countries — "
                    "and whether expensive wines really score higher.",
                    className="subtitle",
                ),
                html.Div(id="slice-stats", className="stat-row"),
            ],
        ),
        html.Div(
            className="body",
            children=[
                html.Aside(
                    className="sidebar",
                    children=[
                        html.H2("Filters"),
                        html.Label("Countries"),
                        dcc.Dropdown(
                            id="country-filter",
                            options=get_country_options(data),
                            value=[],
                            multi=True,
                            placeholder="All countries (default)",
                        ),
                        html.Label("Category"),
                        dcc.Dropdown(
                            id="category-filter",
                            options=[{"label": "All categories", "value": "__all__"}]
                            + [
                                {"label": c.capitalize(), "value": c}
                                for c in CATEGORY_ORDER
                            ],
                            value="__all__",
                            clearable=False,
                        ),
                        html.Label("Price range"),
                        dcc.RangeSlider(
                            id="price-slider",
                            className="price-slider",
                            min=PRICE_MIN, max=PRICE_MAX,
                            value=[PRICE_MIN, PRICE_MAX],
                            marks=PRICE_MARKS,
                            tooltip={"placement": "bottom", "always_visible": False},
                            updatemode="mouseup",
                            allowCross=False,
                        ),
                        html.P(
                            "The map always keeps the global overview; "
                            "country selection drives the two charts below.",
                            className="hint",
                        ),
                    ],
                ),
                html.Main(
                    className="content",
                    children=[
                        dcc.Graph(id="map", config={"displayModeBar": False}),
                        html.Div(
                            className="mode-row",
                            children=[
                                html.Span("Bar view:", className="mode-label"),
                                dcc.RadioItems(
                                    id="bar-mode",
                                    options=BAR_MODES,
                                    value="mix",
                                    className="mode-radio",
                                    inline=True,
                                ),
                            ],
                        ),
                        dcc.Graph(id="dual-bar", config={"displayModeBar": False}),
                        dcc.Graph(id="heatmap", config={"displayModeBar": False}),
                    ],
                ),
            ],
        ),
        html.Footer(
            className="page-footer",
            children="Data: Wine Reviews (Kaggle) · 129,971 bottles · "
            "critic points 80–100 · prices in USD",
        ),
    ],
)


@app.callback(
    Output("map", "figure"),
    Output("dual-bar", "figure"),
    Output("heatmap", "figure"),
    Output("slice-stats", "children"),
    Input("country-filter", "value"),
    Input("category-filter", "value"),
    Input("price-slider", "value"),
    Input("bar-mode", "value"),
)
def update_dashboard(countries, category, price_range, bar_mode):
    map_slice = apply_filters(
        data, None, category, price_range, include_countries=False
    )
    filtered = apply_filters(data, countries, category, price_range)

    bar_fig = (
        make_mix_figure(filtered)
        if bar_mode == "mix"
        else make_value_figure(filtered)
    )
    return (
        make_map_figure(map_slice),
        bar_fig,
        make_heatmap_figure(filtered),
        make_slice_stats(filtered),
    )


if __name__ == "__main__":
    import os

    app.run(debug=False, use_reloader=False, port=int(os.environ.get("PORT", "8050")))
