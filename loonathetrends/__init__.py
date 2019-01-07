from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials as SCC
import tweepy
import requests
import sqlite3
import arrow
from .utils import get_moon_phase
import os
import os.path

DBSCHEMA_PATH = os.path.join(os.path.split(__file__)[0], 'schema.sql')


def get_current_time():
    return arrow.now().to('Asia/Seoul')


def get_proxies(crawlera_apikey):
    proxy_url = f'{crawlera_apikey}:@proxy.crawlera.com:8010/'
    proxies = {'http': 'http://'+proxy_url, 'https': 'https://'+proxy_url}
    return proxies


class YTRetriever(object):
    def __init__(self, api_key):
        self._service = build('youtube', 'v3', developerKey=api_key)
        self._channels = self._service.channels()
        self._playlist_items = self._service.playlistItems()
        self._videos = self._service.videos()

    def get_channel_stats(self, channel_id):
        response = self._channels.list(
            id=channel_id,
            part='statistics',
            fields='items/statistics').execute()
        return response['items'][0]['statistics']

    def get_video_ids(self, playlist_id):
        request = self._playlist_items.list(
            playlistId=playlist_id,
            maxResults=50,
            part='contentDetails',
            fields='nextPageToken,items/contentDetails/videoId')
        videoids = []
        while request is not None:
            response = request.execute()
            for i in response['items']:
                videoids.append(i['contentDetails']['videoId'])
            request = self._playlist_items.list_next(request, response)
        return videoids

    def get_videos_info(self, video_ids):
        split_ids = [video_ids[i:i+50] for i in range(0, len(video_ids), 50)]
        videos_info = []
        for el in split_ids:
            request = self._videos.list(
                id=','.join(el),
                part='snippet,statistics',
                fields='nextPageToken,items(id,' \
                       'snippet(publishedAt,title,description),statistics)')
            while request is not None:
                response = request.execute()
                for i in response['items']:
                    d = {'id': i['id'],
                         'title': i['snippet']['title'],
                         'published_at': i['snippet']['publishedAt'],
                         'description': i['snippet']['description']}
                    d.update(**i['statistics'])
                    moon_phase = get_moon_phase(arrow.get(d['published_at']))
                    d.update(moon_phase=moon_phase)
                    videos_info.append(d)
                request = self._videos.list_next(request,response)
        return videos_info


class SpotifyRetriever(object):
    def __init__(self, client_id, client_secret):
        self._ccm = SCC(client_id=client_id, client_secret=client_secret)
        self._spotify = spotipy.Spotify(client_credentials_manager=self._ccm)

    def get_artist_followers(self, artist):
        response = self._spotify.artist(artist)
        return response['followers']['total']


class TwitterRetriever(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        self._auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self._auth.set_access_token(access_token, access_secret)
        self._api = tweepy.API(self._auth)

    def get_followers_count(self, user):
        return self._api.get_user(user).followers_count

class MelonRetriever(object):
    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update({'accept': '*/*',
                                      'user-agent': 'curl/7.53.1'})

    def get_fan_count(self, artistid):
        url = 'https://www.melon.com/artist/getArtistFanNTemper.json'
        response = self._session.get(url, params={'artistId': artistid})
        return response.json()['fanInfo']['SUMMCNT']



def write_youtube(db):
    channelids = os.environ['YT_CHANNELIDS'].split(':')
    retriever = YTRetriever(os.environ['GOOGLEAPI_KEY'])
    for channelid in channelids:
        stats = retriever.get_channel_stats(channelid)
        date = get_current_time().format('YYYY-MM-DD')
        record = (date, 'youtube', channelid, stats['subscriberCount'])
        c = db.cursor()
        c.execute('INSERT INTO followers VALUES (?, ?, ?, ?)', record)
        db.commit()

def write_spotify(db):
    artistids = os.environ['SPOTIFY_ARTISTIDS'].split(':')
    retriever = SpotifyRetriever(os.environ['SPOTIFY_CLIENTID'],
                                 os.environ['SPOTIFY_CLIENTSECRET'])
    for artistid in artistids:
        count = retriever.get_artist_followers(artistid)
        date = get_current_time().format('YYYY-MM-DD')
        record = (date, 'spotify', artistid, count)
        c = db.cursor()
        c.execute('INSERT INTO followers VALUES (?, ?, ?, ?)', record)
        db.commit()

def write_twitter(db):
    users = os.environ['TWITTER_USERS'].split(':')
    retriever = TwitterRetriever(os.environ['TWITTER_CONSUMERKEY'],
                                 os.environ['TWITTER_CONSUMERSECRET'],
                                 os.environ['TWITTER_ACCESSTOKEN'],
                                 os.environ['TWITTER_ACCESSSECRET'])
    for user in users:
        count = retriever.get_followers_count(user)
        date = get_current_time().format('YYYY-MM-DD')
        record = (date, 'twitter', user, count)
        c = db.cursor()
        c.execute('INSERT INTO followers VALUES (?, ?, ?, ?)', record)
        db.commit()

def write_videostats(db):
    playlistids = os.environ['YT_PLAYLISTIDS'].split(':')
    retriever = YTRetriever(GOOGLEAPI_KEY)
    for playlistid in playlistids:
        videoids = retriever.get_video_ids(playlistid)
        videosinfo = retriever.get_videos_info(videoids)
        date = get_current_time().format('YYYY-MM-DD HH:MM')
        c = db.cursor()
        for v in videosinfo:
            c.execute('INSERT OR IGNORE INTO videos' \
                      '(video_id, title, published_at, description, moon_phase)' \
                      'VALUES (?, ?, ?, ?, ?)',
                      (v['id'], v['title'], v['published_at'],
                       v['description'], v['moon_phase']))
            c.execute('INSERT INTO video_stats VALUES (?, ?, ?, ?, ?, ?)',
                      (date, v['id'], v['viewCount'], v['likeCount'],
                       v['dislikeCount'], v['commentCount']))
        db.commit()

def write_melon(db):
    artistids = os.environ['MELON_ARTISTIDS'].split(':')
    retriever = MelonRetriever()
    for artistid in artistids:
        count = retriever.get_fan_count(artistid)
        date = get_current_time().format('YYYY-MM-DD')
        record = (date, 'melon', artistid, count)
        c = db.cursor()
        c.execute('INSERT INTO followers VALUES (?, ?, ?, ?)',
                  record)
        db.commit()

def create_db(fname):
    db = sqlite3.connect(fname)
    c = db.cursor()
    with open(DBSCHEMA_PATH) as f:
        c.executescript(f.read())
    db.commit()

