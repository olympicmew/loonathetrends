import argparse
import os
import psycopg2
import sys
import loonathetrends.bot.plots as lttplots

DBPATH = os.getenv("DBPATH")

argparser = argparse.ArgumentParser()
argparser.add_argument("videoid")
argparser.add_argument("--metric", "-m", default="views")
argparser.add_argument("--timeframe", "-t", default="short")
args = argparser.parse_args()

db = psycopg2.connect(DBPATH)

plot = lttplots.youtube(db, args.videoid, metric=args.metric, timeframe=args.timeframe)
sys.stdout.buffer.write(plot)

