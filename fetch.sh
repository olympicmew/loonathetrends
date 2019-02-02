#!/bin/bash
export DBPATH=$HOME/loonathetrends/loonathetrends.db
cd $HOME/loonathetrends
source venv/bin/activate
python fetcher.py $@
