#!/bin/bash
cd $HOME/loonathetrends
source venv/bin/activate
python fetcher.py $@
