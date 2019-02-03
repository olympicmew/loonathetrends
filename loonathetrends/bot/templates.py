followers_update = '''\
Social media {freq} update ({date}) 🤖

YouTube: {tots[youtube]:,} ({difs[youtube]:+,}) subscribers
Twitter: {tots[twitter]:,} ({difs[twitter]:+,}) followers
Instagram: {tots[instagram]:,} ({difs[instagram]:+,}) followers
Fancafe: {tots[daumcafe]:,} ({difs[daumcafe]:+,}) members
VLIVE: {tots[vlive]:,} ({difs[vlive]:+,}) followers
Spotify: {tots[spotify]:,} ({difs[spotify]:+,}) followers
Melon: {tots[melon]:,} ({difs[melon]:+,}) followers
'''

youtube_update = '''\
YouTube stats update ({date}) 🤖

{kind}
{title}
▶️ http://youtu.be/{videoid}

👁️: {tots[views]:,.0f} ({rates[views]:,.1f} views/day)
❤️: {tots[likes]:,.0f} ({rates[likes]:,.1f} likes/day)
💔: {tots[dislikes]:,.0f} ({rates[dislikes]:,.1f} dislikes/day)
💬: {tots[comments]:,.0f} ({rates[comments]:,.1f} comments/day)
'''

youtube_milestone = '''\
#OrbitStreamingWednesday ({date}) 🤖

This video needs some love:
{title}
▶️ http://youtu.be/{videoid}

It needs {diff:,.0f} views to reach {milestone}. It should get there {prediction}, but we can make it happen faster!
'''
