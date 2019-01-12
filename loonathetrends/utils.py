import ephem
import pandas as pd

def get_moon_phase(date):
    date = ephem.Date(date.datetime)
    nnm = ephem.next_new_moon(date)
    pnm = ephem.previous_new_moon(date)
    return (date-pnm) / (nnm-pnm)

def get_moon_emoji(phase):
    emojis = '🌑🌒🌓🌔🌕🌖🌗🌘'
    idx = round(phase*8) % 8
    return emojis[idx]

def get_video_title_lookup(db):
    df = pd.read_sql('select video_id, title from videos',
                     db, index_col='video_id')
    return df.title.to_dict()
