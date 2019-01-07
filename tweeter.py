import os
import argparse
import logging
import sqlite3
import loonathetrends.bot as lttbot

DBPATH = os.environ['DBPATH']

argparser = argparse.ArgumentParser()
argparser.add_argument('type')
argparser.add_argument('--dry-run', action='store_true')
args = argparser.parse_args()

logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

db = sqlite3.connect(DBPATH)
logging.info('Database connected')

if args.type == 'followers-daily':
	status = lttbot.followers_update(db, 'daily', args.dry_run)
	if args.dry_run:
		print(status)
	else:
		logging.info(status)
elif args.type == 'followers-weekly':
	status = lttbot.follwers_update(db, 'weekly', args.dry_run)
	if args.dry_run:
		print(status)
	else:
		logging.info(status)
