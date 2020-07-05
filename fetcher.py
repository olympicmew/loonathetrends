import loonathetrends as ltt
import psycopg2
import argparse
import logging
import os

argparser = argparse.ArgumentParser()
argparser.add_argument("mode")
args = argparser.parse_args()

logging.basicConfig(
    filename="fetcher.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

db = psycopg2.connect(os.environ["DBPATH"])
logging.info("Database connected")

if args.mode == "video-stats":
    ltt.write_videostats(db)
    logging.info("Youtube stats: done")
elif args.mode == "followers":
    ltt.write_youtube(db)
    logging.info("Youtube: done")
    ltt.write_spotify(db)
    logging.info("Spotify: done")
    ltt.write_twitter(db)
    logging.info("Twitter: done")
    try:
        ltt.write_daumcafe(db)
        logging.info("Fancafe: done")
    except:
        logging.info("Fancafe: failed")
    try:
        ltt.write_instagram(db)
        logging.info("Instagram: done")
    except:
        logging.info("Instagram: failed")
    try:
        ltt.write_melon(db)
        logging.info("Melon: done")
    except:
        logging.info("Melon: failed")
    try:
        ltt.write_vlive(db)
        logging.info("VLIVE: done")
    except:
        logging.info("VLIVE: failed")
elif args.mode == "popularity":
    ltt.write_spotify_popularity(db)
    logging.info("Spotify popularity: done")

db.close()

