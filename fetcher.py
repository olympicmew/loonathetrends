import loonathetrends as ltt
import sqlite3
import argparse
import logging

argparser = argparse.ArgumentParser()
argparser.add_argument('db')
argparser.add_argument('--videostats', action='store_true')
args = argparser.parse_args()

logging.basicConfig(filename='fetcher.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

db = sqlite3.connect(args.db)
logging.info('Database connected')

if args.videostats:
    ltt.write_videostats(db)
    logging.info('Youtube stats: done')
else:
    ltt.write_youtube(db)
    logging.info('Youtube: done')
    ltt.write_spotify(db)
    logging.info('Spotify: done')
    ltt.write_twitter(db)
    logging.info('Twitter: done')
    ltt.write_melon(db)
    logging.info('Melon: done')
