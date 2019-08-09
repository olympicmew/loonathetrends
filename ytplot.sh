#!/bin/bash
export DBPATH="***REMOVED***"
export IMGUR_CLIENTID="***REMOVED***"
cd $HOME/loonathetrends
source venv/bin/activate
python ytplot.py $@ | \
curl -L -XPOST "https://api.imgur.com/3/image" \
     -H "Authorization: Client-ID $IMGUR_CLIENTID" -F "image=@-" -s | \
python -c "import sys, json; print(json.load(sys.stdin).get('data').get('link'))"
