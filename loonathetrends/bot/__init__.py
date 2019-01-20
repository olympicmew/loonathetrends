import os
from twitter import OAuth, Twitter
import pandas as pd
import arrow
from . import templates, plots
from loonathetrends.utils import get_video_title_lookup

auth = OAuth(os.environ['TWITTER_ACCESSTOKEN'],
             os.environ['TWITTER_ACCESSSECRET'],
             os.environ['TWITTER_CONSUMERKEY'],
             os.environ['TWITTER_CONSUMERSECRET'])
t = Twitter(auth=auth)
t_upload = Twitter(domain='upload.twitter.com', auth=auth)

def followers_update(db, freq, dry_run=False, post_plots=False):
    if freq == 'daily':
        query = "SELECT * FROM followers " \
                "WHERE tstamp = date('now') " \
                "OR tstamp = date('now','-1 days') " \
                "ORDER BY tstamp"
        template = templates.followers_daily
    elif freq == 'weekly':
        query = "SELECT * FROM followers " \
                "WHERE tstamp = date('now') " \
                "OR tstamp = date('now','-7 days') " \
                "ORDER BY tstamp"
        template = templates.followers_weekly
    else:
        raise RuntimeException('Parameter freq provided not valid')
    df = pd.read_sql(query, db)
    date = df['tstamp'].iloc[-1]
    grouped = df.groupby('site')
    tots = grouped.last()['count'].to_dict()
    difs = (grouped.last()['count'] - grouped.first()['count']).to_dict()
    status = template.format(date=date, tots=tots, difs=difs)
    if post_plots:
        media = plots.new_followers(db, freq)
    else:
        media = []
    if not dry_run:
        media_ids = []
        for img in media:
            media_id = t_upload.media.upload(media=img)['media_id_string']
            media_ids.append(media_id)
        t.statuses.update(status=status, media_ids=','.join(media_ids))
    return status

def videostats_update(db, freq, dry_run=False):
    # build lookup table for video titles
    lookup = get_video_title_lookup(db)
    # find out what video to post about
    df = pd.read_sql('select * from video_stats', db, parse_dates=['tstamp'])
    df = df.set_index('tstamp')
    func = lambda x: x.diff().last(freq).sum()
    videoid = df.groupby('video_id').comments.agg(func).idxmax()
    # get stats for the video
    stats = df[df.video_id == videoid].drop('video_id', axis=1)
    last = stats.index[-1]
    trimmed_stats = stats.reindex(pd.date_range(last - pd.Timedelta(freq), last, freq='h'))
    tots = trimmed_stats.iloc[-1].to_dict()
    rates = trimmed_stats.diff().mean().to_dict()
    date = arrow.get(last).format('YYYY-MM-DD ha')
    title = lookup[videoid]
    # make charts
    # TODO
    # fill template and post
    template = templates.videostats
    status = template.format(title=title, date=date, tots=tots, rates=rates, videoid=videoid)
    if not dry_run:
        t.statuses.update(status=status)
    return status

def youtube_update(db, kind, dry_run=False):
    # create DataFrame for stats
    allstats = pd.read_sql('SELECT * FROM video_stats ORDER BY tstamp',
                           db, parse_dates=['tstamp']).set_index('tstamp')
    
    # find out what video to post about
    func = lambda x: x.diff().last('7d').sum()
    if kind == 'latest':
        videoid = pd.read_sql('SELECT published_at, video_id FROM videos ' \
                              'ORDER BY published_at', db)['video_id'].iloc[-1]
    elif kind == 'views':
        videoid = allstats.groupby('video_id')['views'].agg(func).idxmax()
    elif kind == 'comments':
        videoid = allstats.groupby('video_id')['comments'].agg(func).idxmax()
    
    # get and trim stats
    stats = allstats[allstats.video_id == videoid].drop('video_id', axis=1)
    last = stats.index[-1]
    trimmed = stats.reindex(pd.date_range(last - pd.Timedelta('7d'), last, freq='h'))
    
    # assign fill-ins for template
    tots = trimmed.iloc[-1].to_dict()
    rates = (trimmed.diff().mean() * 24).to_dict()
    date = arrow.get(last).format('YYYY-MM-DD')
    
    # make charts
    media = plots.youtube_update(db, videoid)
    
    # fill template
    kind_template = {'latest': 'Latest upload from @loonatheworld:',
                     'views': 'Most viewed video this week:',
                     'comments': 'Most commented video this week:',
                    }
    template = templates.youtube_update
    status = template.format(kind=kind_template[kind],
                             date=date, tots=tots,
                             rates=rates, videoid=videoid)
    
    # post on twitter
    if not dry_run:
        media_id = t_upload.media.upload(media=img)['media_id_string']
        t.statuses.update(status=status, media_ids=media_id)
    return status
