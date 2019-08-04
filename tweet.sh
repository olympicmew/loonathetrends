#!/bin/bash
export DBPATH="***REMOVED***"
cd $HOME/loonathetrends
source venv/bin/activate
python tweeter.py $@
