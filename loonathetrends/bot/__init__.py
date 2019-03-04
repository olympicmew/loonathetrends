import os
import unicodedata
from twitter import OAuth, Twitter
import numpy as np
import pandas as pd
import arrow
from . import templates, plots
from loonathetrends.utils import get_video_title_lookup, get_video_ismv_lookup

auth = OAuth(
    os.environ["TWITTER_ACCESSTOKEN"],
    os.environ["TWITTER_ACCESSSECRET"],
    os.environ["TWITTER_CONSUMERKEY"],
    os.environ["TWITTER_CONSUMERSECRET"],
)
t = Twitter(auth=auth)
t_upload = Twitter(domain="upload.twitter.com", auth=auth)

MILESTONES = {
    100_000: "100k",
    200_000: "200k",
    500_000: "500k",
    1_000_000: "1M",
    2_000_000: "2M",
    5_000_000: "5M",
    10_000_000: "10M",
    20_000_000: "20M",
    50_000_000: "50M",
    100_000_000: "100M",
}


def followers_update(db, freq, dry_run=False, post_plots=False):
    if freq == "daily":
        ndays = 1
    elif freq == "weekly":
        ndays = 7
    else:
        raise RuntimeError("Parameter freq provided not valid")
    query = (
        "SELECT * FROM followers "
        "WHERE tstamp = date('now') "
        "OR tstamp = date('now','-{} days') "
        "ORDER BY tstamp".format(ndays)
    )
    template = templates.followers_update
    df = pd.read_sql(query, db)
    date = arrow.get(df["tstamp"].iloc[-1]).format("YYMMDD")
    grouped = df.groupby("site")
    tots = grouped.last()["count"].to_dict()
    difs = (grouped.last()["count"] - grouped.first()["count"]).to_dict()
    status = template.format(freq=freq, date=date, tots=tots, difs=difs)
    status_len = len(unicodedata.normalize("NFC", status))
    if status_len > 280:
        raise RuntimeError(f"The status update is {status_len} characters long.")
    if post_plots:
        media = plots.new_followers(db)
    else:
        media = []
    if not dry_run:
        media_ids = []
        for img in media:
            media_id = t_upload.media.upload(media=img)["media_id_string"]
            media_ids.append(media_id)
        if media_ids:

            def chunk_four(l):
                for i in range(0, len(l), 4):
                    yield l[i : i + 4]

            last_tweet = None
            for chunk in chunk_four(media_ids):
                if last_tweet == None:
                    last_tweet = t.statuses.update(
                        status=status, media_ids=",".join(chunk)
                    )
                else:
                    last_tweetid = last_tweet["id_str"]
                    last_tweet = t.statuses.update(
                        status="@loonathetrends",
                        media_ids=",".join(chunk),
                        in_reply_to_status_id=last_tweetid,
                    )
        else:
            t.statuses.update(status=status)
    else:
        for n, img in enumerate(media, 1):
            with open("test{}.png".format(n), "wb") as f:
                f.write(img)
    return status


def youtube_update(db, kind, dry_run=False):
    # create DataFrame for stats
    allstats = pd.read_sql(
        "SELECT * FROM video_stats ORDER BY tstamp", db, parse_dates=["tstamp"]
    ).set_index("tstamp")
    lookup = get_video_title_lookup(db)
    mvlookup = pd.Series(get_video_ismv_lookup(db))

    # find out what video to post about
    func = lambda x: x.diff().last("7d").sum()
    if kind == "latest":
        videoid = pd.read_sql(
            "SELECT published_at, video_id FROM videos ORDER BY published_at", db
        ).set_index("video_id").loc[mvlookup].index[-1]
    elif kind == "views":
        videoid = allstats.groupby("video_id")["views"].agg(func).idxmax()
    elif kind == "likes":
        videoid = allstats.groupby("video_id")["likes"].agg(func).idxmax()
    elif kind == "comments":
        videoid = allstats.groupby("video_id")["comments"].agg(func).idxmax()

    # get and trim stats
    stats = allstats[allstats.video_id == videoid].drop("video_id", axis=1)
    last = stats.index[-1]
    length = pd.Timedelta("1d")
    trimmed = stats.reindex(pd.date_range(last - length, last, freq="h"))

    # assign fill-ins for template
    title = lookup[videoid]
    tots = trimmed.iloc[-1].to_dict()
    rates = (trimmed.diff().mean() * 24).to_dict()
    date = arrow.get(last).format("YYMMDD")

    # make charts
    media = plots.youtube_update(db, videoid)

    # fill template
    kind_template = {
        "latest": "Latest MV from @loonatheworld:",
        "views": "Most viewed video this week:",
        "likes": "Most liked video this week:",
        "comments": "Most commented video this week:",
    }
    template = templates.youtube_update
    status = template.format(
        kind=kind_template[kind],
        title=title,
        date=date,
        tots=tots,
        rates=rates,
        videoid=videoid,
    )
    status_len = len(unicodedata.normalize("NFC", status))
    if status_len > 280:
        raise RuntimeError(f"The status update is {status_len} characters long.")

    # post on twitter
    if not dry_run:
        media_id = t_upload.media.upload(media=media)["media_id_string"]
        t.statuses.update(status=status, media_ids=media_id)
    return status


def youtube_milestone(db, dry_run=False):
    # get the stats
    stats = pd.read_sql(
        "select * from video_stats order by tstamp", db, parse_dates=["tstamp"]
    )
    mvlookup = pd.Series(get_video_ismv_lookup(db))
    lookup = get_video_title_lookup(db)
    # get the current view counts for all videos
    views = stats.groupby("video_id")["views"].last()
    # calculate how many views are left for each milestone for all videos
    marray = np.array(list(MILESTONES)).reshape((1, len(MILESTONES)))
    varray = np.array(views).reshape((len(views), 1))
    viewsleft = pd.DataFrame(
        columns=MILESTONES, data=marray - varray, index=views.index
    )
    viewsleft = viewsleft[viewsleft > 0]  # discard reached milestones
    # calculate the current view rate for all videos
    pivot = stats.pivot(index="tstamp", columns="video_id", values="views")
    rates = pivot.last("7d1h").asfreq("h").diff().mean() * 24
    # calculate how many days are left to reach the milestones
    daysleft = viewsleft.apply(lambda x: x / rates).min(axis=1)
    # find out the featured video for today
    daysleft_mv = daysleft[(daysleft <= 7) & mvlookup]
    videoid = daysleft.idxmin() if daysleft_mv.empty else daysleft_mv.idxmin()
    milestone = viewsleft.loc[videoid].idxmin()
    # create the mapping for the tweet template
    fillin = {
        "date": arrow.now().format("YYMMDD"),
        "videoid": videoid,
        "title": lookup[videoid],
        "diff": viewsleft.loc[videoid].min(),
        "milestone": MILESTONES[milestone],
        "prediction": (arrow.now().shift(days=daysleft.loc[videoid]).humanize()),
    }
    # fill in the template and post on Twitter
    template = templates.youtube_milestone
    status = template.format(**fillin)
    status_len = len(unicodedata.normalize("NFC", status))
    if status_len > 280:
        raise RuntimeError(f"The status update is {status_len} characters long.")
    if not dry_run:
        t.statuses.update(status=status)
    return status
