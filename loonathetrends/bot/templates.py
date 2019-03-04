followers_update = """\
{date} SNS follower counts {freq} update 🤖

YouTube: {tots[youtube]:,} ({difs[youtube]:+,})
Twitter: {tots[twitter]:,} ({difs[twitter]:+,})
Instagram: {tots[instagram]:,} ({difs[instagram]:+,})
Fancafe: {tots[daumcafe]:,} ({difs[daumcafe]:+,})
VLIVE: {tots[vlive]:,} ({difs[vlive]:+,})
Spotify: {tots[spotify]:,} ({difs[spotify]:+,})
Melon: {tots[melon]:,} ({difs[melon]:+,})
"""

youtube_update = """\
{date} YouTube stats update 🤖

{kind}
{title}
▶️ http://youtu.be/{videoid}

👁️: {tots[views]:,.0f} ({rates[views]:,.1f} views/day)
❤️: {tots[likes]:,.0f} ({rates[likes]:,.1f} likes/day)
💔: {tots[dislikes]:,.0f} ({rates[dislikes]:,.1f} dislikes/day)
💬: {tots[comments]:,.0f} ({rates[comments]:,.1f} comments/day)
"""

youtube_milestone = """\
{date} #OrbitStreamingWednesday 🤖

This video needs some love:
{title}
▶️ http://youtu.be/{videoid}

It needs {diff:,.0f} views to reach {milestone}. It should get there {prediction}, but we can make it happen faster!
"""
