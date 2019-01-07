import os
import tweepy
import pandas as pd
import arrow
from . import templates

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
		template = template = templates.followers_weekly
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
