import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
from io import BytesIO

sns.set('talk', 'ticks', font='Source Han Sans KR')

def _add_watermark(fig):
    fig.text(0.5, 0.5, 'cr: @loonathetrends',
             fontsize=36, color='black',
             ha='center', va='center', alpha=0.1)

def _add_thousand_sep(ax):
    formatter = FuncFormatter(lambda y,  p: format(int(y), ','))
    ax.yaxis.set_major_formatter(formatter)

def new_followers(db, freq):
    if freq == 'daily':
        extent = 7
    elif freq == 'weekly':
        extent = 30
    else:
        extent = 30
    titles = {'youtube': 'LOONA YouTube new subscribers',
              'spotify': 'LOONA Spotify new followers',
              'twitter': 'LOONA Twitter new followers',
              'melon': 'LOONA Melon new followers'}
    df = (pd.read_sql('select tstamp, site, count from followers '
                     'order by tstamp', db, parse_dates=['tstamp'])
                     .set_index('tstamp'))
    grouped = df.groupby('site')
    media = []
    for site, stats in grouped['count']:
        stats = stats.asfreq('d') # make sure to have days with no measurements
        stats = stats.last('{}d'.format(extent))
        stats = stats.diff() # get gain instead of cumulative followers
        # create plot
        fig, ax = plt.subplots()
        stats.plot(ax = ax, title = titles[site],
                   style = '.-', markersize = 14,
                   figsize = (max(7, len(stats)/(extent/10)), 5))
        ax.set_xlabel('')
        _add_thousand_sep(ax)
        _add_watermark(fig)
        image = BytesIO()
        fig.savefig(image, format='png', dpi=160, bbox_inches='tight')
        media.append(image.getvalue())
    return media
