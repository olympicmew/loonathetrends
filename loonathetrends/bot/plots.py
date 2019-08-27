from math import log10
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
from io import BytesIO
from loonathetrends.utils import get_video_title_lookup

sns.set(
    "talk",
    "ticks",
    font="Source Han Sans KR",
    rc={
        "axes.facecolor": "15202b",
        "axes.edgecolor": "white",
        "savefig.facecolor": "15202b",
        "savefig.edgecolor": "none",
        "axes.labelcolor": "white",
        "axes.grid": True,
        "figure.facecolor": "15202b",
        "grid.color": "3d5466",
        "text.color": "white",
        "xtick.color": "white",
        "ytick.color": "white",
    },
)
sns.set_palette("pastel")


def _add_watermark(fig):
    fig.text(
        0.5,
        0.5,
        "cr: @loonathetrends",
        fontsize=36,
        color="black",
        ha="center",
        va="center",
        alpha=0.1,
    )


def _add_thousand_sep(ax):
    formatter = FuncFormatter(lambda y, p: format(int(y), ","))
    ax.yaxis.set_major_formatter(formatter)


def new_followers(db):
    titles = {
        "youtube": "LOONA YouTube new subscribers",
        "spotify": "LOONA Spotify new followers",
        "twitter": "LOONA Twitter new followers",
        "vlive": "LOONA VLIVE new followers",
        "instagram": "LOONA Instagram new followers",
        "daumcafe": "LOONA fancafe new members",
        "melon": "LOONA Melon new followers",
    }
    df = pd.read_sql(
        "select tstamp, site, count from followers " "order by tstamp",
        db,
        parse_dates=["tstamp"],
    ).set_index("tstamp")
    grouped = df.groupby("site")
    media = {}
    for site, stats in grouped["count"]:
        stats = stats.asfreq("d")  # make sure to have days with no measurements
        stats = stats.last("148d")
        stats = stats.diff()  # get gain instead of cumulative followers
        # special case for Instagram data
        if site == "instagram":
            stats["2019-02-13":"2019-02-14"] = None
        # create plot
        fig, ax = plt.subplots()
        stats.plot(ax=ax, title=titles[site], markersize=14, figsize=(10, 5))
        ax.set_xlabel("")
        _add_thousand_sep(ax)
        _add_watermark(fig)
        image = BytesIO()
        fig.savefig(image, format="png", dpi=160, bbox_inches="tight")
        media[site] = image.getvalue()
    return (
        media["youtube"],
        media["twitter"],
        media["instagram"],
        media["daumcafe"],
        media["vlive"],
        media["spotify"],
        media["melon"],
    )


def youtube(db, videoid, metric="views", timeframe="short"):
    # get stats and clean up
    stats = pd.read_sql(
        "select * from video_stats where video_id=%s order by tstamp",
        db,
        params=[videoid],
        parse_dates=["tstamp"],
    )
    stats = (
        stats.set_index("tstamp")
        .drop("video_id", axis=1)
        .tz_convert("Asia/Seoul")
        .tz_localize(None)
    )
    title = get_video_title_lookup(db)[videoid]
    stats = stats.asfreq("h")
    # stats = stats.tshift(-1)

    # calculate moving averages
    df = pd.DataFrame(stats[metric])
    if timeframe == "medium":
        df = df.asfreq("d", normalize=True).diff().dropna().asfreq("d").tshift(-1)
        df = df.assign(
            avg_w=df.rolling("7d", min_periods=5).mean(),
            avg_m=df.rolling("28d", min_periods=26).mean(),
        )
    else:
        df = df.diff().dropna().asfreq("h") * 24
        df = df.assign(
            avg_d=df.rolling("1d", min_periods=18).mean(),
            avg_w=df.rolling("7d", min_periods=162).mean(),
        )
        hourly_data = df.pop(metric).tshift(-1)
        df = pd.concat([hourly_data, df], axis=1)
    # trim depending on timeframe
    if timeframe == "medium":
        df = df.last("168d")
    else:
        df = df.last("28d")
    # decide what to plot
    if len(stats) <= 24 * 3 or (len(stats) <= 24 * 21 and timeframe == "medium"):
        y = [metric]
        style = ["-"]
        has_legend = False
    elif len(stats) <= 24 * 21:
        y = [metric, "avg_d"]
        style = [".", "-"]
        has_legend = True
        labels = ["Hourly measurements", "Daily average"]
    elif len(stats) <= 24 * 84:
        if timeframe == "medium":
            y = [metric, "avg_w"]
            style = ["-", "-"]
            has_legend = True
            labels = ["Daily average", "Weekly average"]
        else:
            y = [metric, "avg_d", "avg_w"]
            style = [".", "-", "-"]
            has_legend = True
            labels = ["Hourly measurements", "Daily average", "Weekly average"]
    else:
        has_legend = True
        if timeframe == "medium":
            y = [metric, "avg_w", "avg_m"]
            style = ["-", "-", "-"]
            labels = ["Daily average", "Weekly average", "Monthly average"]
        else:
            y = [metric, "avg_d", "avg_w"]
            style = [".", "-", "-"]
            labels = ["Hourly measurements", "Daily average", "Weekly average"]
    # check whether to draw log plot
    islog = log10(df[metric].max() / df[metric].median()) > 1

    # draw plot
    ax = df.plot(
        y=y,
        legend=has_legend,
        title=title,
        markersize=3,
        figsize=(10, 5),
        style=style,
        logy=islog,
    )
    # edit labels and add watermark
    ax.set_xlabel(None)
    ax.set_ylabel("{}/day".format(metric))
    if has_legend:
        legend = ax.get_legend().get_texts()
        for label, text in zip(legend, labels):
            label.set_text(text)
    _add_thousand_sep(ax)
    _add_watermark(ax.get_figure())

    # save image of plot
    image = BytesIO()
    ax.get_figure().savefig(image, format="png", dpi=160, bbox_inches="tight")

    return image.getvalue()
