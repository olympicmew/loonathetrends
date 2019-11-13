# Yuxi
Stats fetcher and bot powering Twitter account @loonathetrends.

## Requirements
- Python >= 3.7
- PostgreSQL >= 10
- check `requirements.txt` for more (it's made with `pip freeze` so all secondary dependencies are baked in, sorry)

## Quick overview of how this works
1. `fetcher.py` takes care of getting the stats and storing them on the Postgres database
2. `tweeter.py` takes care of tweeting stuff
3. `loonathetrends` contains the fetching logic
4. `loonathetrends.bot` contains most Twitter related things
5. `loonathetrends.bot.plots` has the plot drawing logic
6. `loonathetrends.bot.templates` has the tweet templates


## More questions?
[DM me on Twitter](https://twitter.com/messages/compose?recipient_id=1076917999968374786). A day may come when I tidy the codebase, but it is not today. ~~[TODAY! WE! FIGHT!](https://youtu.be/M8pR1rZZHEs?t=15)~~ ATM I'm too busy with music school stuff to code much 😅
