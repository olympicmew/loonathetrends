import os
import tweepy
import pandas as pd
import arrow
from . import templates
from loonathetrends.utils import get_video_title_lookup

auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMERKEY'],
                           os.environ['TWITTER_CONSUMERSECRET'])
auth.set_access_token(os.environ['TWITTER_ACCESSTOKEN'],
                      os.environ['TWITTER_ACCESSSECRET'])
twitter = tweepy.API(auth)

def followers_update(db, freq, dry_run=False):
	if freq == 'daily':
		query = "SELECT * FROM followers " \
                "WHERE tstamp = date('now','-1 days') " \
                "OR tstamp = date('now','-2 days') " \
                "ORDER BY tstamp"
		date = arrow.now().shift(days=-1).format('YYYY-MM-DD')
		template = templates.followers_daily
	elif freq == 'weekly':
		query = "SELECT * FROM followers " \
                "WHERE tstamp = date('now','-1 days') " \
                "OR tstamp = date('now','-8 days') " \
                "ORDER BY tstamp"
		date = '{:04}-W{:02}'.format(*arrow.now().shift(days=-1).isocalendar())
		template = templates.followers_weekly
	else:
		raise RuntimeException('Parameter freq provided not valid')
	df = pd.read_sql(query, db, index_col='site')
	grouped = df.groupby('site')
	tots = grouped.last()['count'].to_dict()
	difs = (grouped.last()['count'] - grouped.first()['count']).to_dict()
	status = template.format(date=date, tots=tots, difs=difs)
	if not dry_run:
		twitter.update_status(status)
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
    date = arrow.get(last).format('YYYY-MM-DD Ha')
    title = lookup[videoid]
    # make charts
    # TODO
    # fill template and post
    template = templates.videostats
    status = template.format(title=title, date=date, tots=tots, rates=rates)
    if not dry_run:
        twitter.update_status(status)
    return status
