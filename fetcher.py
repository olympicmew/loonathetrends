import loonathetrends as ltt
import sqlite3
import argparse
import logging
import os

argparser = argparse.ArgumentParser()
argparser.add_argument('mode')
args = argparser.parse_args()

logging.basicConfig(filename='fetcher.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

db = sqlite3.connect(os.environ['DBPATH'])
logging.info('Database connected')

if args.mode == 'video-stats':
    ltt.write_videostats(db)
    logging.info('Youtube stats: done')
elif args.mode == 'followers':
    ltt.write_youtube(db)
    logging.info('Youtube: done')
    ltt.write_spotify(db)
    logging.info('Spotify: done')
    ltt.write_twitter(db)
    logging.info('Twitter: done')
    ltt.write_vlive(db):
    logging.info('VLIVE: done')
    ltt.write_daumcafe(db):
    logging.info('Fancafe: done')
    ltt.write_instagram(db):
    logging.info('Instagram: done')
    ltt.write_melon(db)
    logging.info('Melon: done')
