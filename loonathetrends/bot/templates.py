followers_daily = '''\
Social media daily update ({date}) 🤖

YouTube: {tots[youtube]:,} ({difs[youtube]:+,}) subscribers
Twitter: {tots[twitter]:,} ({difs[twitter]:+,}) followers
Spotify: {tots[spotify]:,} ({difs[spotify]:+,}) followers
'''
#Melon: {tots[melon]:,} ({difs[melon]:+,}) followers

followers_weekly = '''\
Social media weekly roundup ({date}) 🤖

Youtube: {tots[youtube]:,} ({difs[youtube]:+,}) subscribers
Twitter: {tots[twitter]:,} ({difs[twitter]:+,}) followers
Spotify: {tots[spotify]:,} ({difs[spotify]:+,}) followers
'''
#Melon: {tots[melon]:,} ({difs[melon]:+,}) followers'''

videostats = '''\
YouTube stats update ({date} KST) 🤖

{title}
▶️ http://youtu.be/{videoid}

Views: {tots[views]:,.0f} ({rates[views]:,.1f} views/hour)
Likes: {tots[likes]:,.0f} ({rates[likes]:,.1f} likes/hour)
Dislikes: {tots[dislikes]:,.0f} ({rates[dislikes]:,.1f} dislikes/hour)
Comments: {tots[comments]:,.0f} ({rates[comments]:,.1f} comments/hour)
'''

youtube_update = '''\
YouTube stats update ({date}) 🤖

{kind}
▶️ http://youtu.be/{videoid}

Views: {tots[views]:,.0f} ({rates[views]:,.1f} views/day)
Likes: {tots[likes]:,.0f} ({rates[likes]:,.1f} likes/day)
Dislikes: {tots[dislikes]:,.0f} ({rates[dislikes]:,.1f} dislikes/day)
Comments: {tots[comments]:,.0f} ({rates[comments]:,.1f} comments/day)
'''
