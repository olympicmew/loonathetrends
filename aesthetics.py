import loonathetrends.utils as utils
from twitter import OAuth, Twitter
import arrow
import os
import math

auth = OAuth(os.environ['TWITTER_ACCESSTOKEN'],
             os.environ['TWITTER_ACCESSSECRET'],
             os.environ['TWITTER_CONSUMERKEY'],
             os.environ['TWITTER_CONSUMERSECRET'])
t = Twitter(auth=auth)

def update_handle():
    me = t.account.verify_credentials()
    phase = utils.get_moon_phase(arrow.utcnow())
    emoji = utils.get_moon_emoji(phase)
    handle = emoji + me['name'][1:]
    t.account.update_profile(name=handle)

def update_color():
    birth = arrow.get('2018-08-20 18:00+0900')
    days = (arrow.now() - birth).total_seconds() / 86400
    r, g, b = (math.sin(2*math.pi*days/i) for i in (28,23,33))
    
    if r >= 0:
        emo = (r, 0, 0)
    else:
        emo = (0, -r ,-r)
    if g >= 0:
        phy = (0, g, 0)
    else:
        phy = (-g, 0, -g)
    if b >= 0:
        ine = (0, 0, b)
    else:
        ine = (-b, -b, 0)
    
    fR = round((emo[0]+phy[0]+ine[0])/3*255)
    fG = round((emo[1]+phy[1]+ine[1])/3*255)
    fB = round((emo[2]+phy[2]+ine[2])/3*255)
    
    color = (hex(fR)[2:] + hex(fG)[2:] + hex(fB)[2:]).upper()
    t.account.update_profile(profile_link_color=color)

if __name__ == '__main__':
    update_handle()
    #update_color()
    