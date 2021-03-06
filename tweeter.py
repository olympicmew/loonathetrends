import os
import re
import argparse
import logging
import psycopg2
import loonathetrends.bot as lttbot

DBPATH = os.environ["DBPATH"]

argparser = argparse.ArgumentParser()
argparser.add_argument("type")
argparser.add_argument("--dry-run", action="store_true")
argparser.add_argument("-p", "--plot", action="store_true")
args = argparser.parse_args()

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

db = psycopg2.connect(DBPATH)
logging.info("Database connected")

if args.type == "followers-daily":
    status = lttbot.followers_update(db, "daily", args.dry_run, post_plots=args.plot)
    if args.dry_run:
        print(status)
    else:
        logging.info(status)
elif args.type == "followers-weekly":
    status = lttbot.followers_update(db, "weekly", args.dry_run, post_plots=True)
    if args.dry_run:
        print(status)
    else:
        logging.info(status)
elif args.type == "videostats-8h":
    status = lttbot.videostats_update(db, "8h", args.dry_run)
    if args.dry_run:
        print(status)
    else:
        logging.info(status)
elif args.type == "youtube-milestone":
    status = lttbot.youtube_milestone(db, args.dry_run)
    if args.dry_run:
        print(status)
    else:
        logging.info(status)
elif args.type == "youtube-milestone-reached":
    status = lttbot.youtube_milestone_reached(db, args.dry_run)
    if args.dry_run:
        print(status)
    else:
        logging.info(status)
elif args.type == "youtube-statsdelivery":
    for status in lttbot.youtube_statsdelivery(db, args.dry_run):
        if args.dry_run:
            print(status)
        else:
            logging.info(status)
elif re.match(r"youtube-(?P<kind>\S+)", args.type):
    kind = re.match(r"youtube-(?P<kind>\S+)", args.type).group("kind")
    status = lttbot.youtube_update(db, kind, args.dry_run)
    if args.dry_run:
        print(status)
    else:
        logging.info(status)

db.close()
