followers_update = (
    "{date} SNS follower counts {freq} update 🤖\n"
    "\n"
    "YouTube: {tots[youtube]:,} ({difs[youtube]:+,})\n"
    "Twitter: {tots[twitter]:,} ({difs[twitter]:+,})\n"
    "Instagram: {tots[instagram]:,} ({difs[instagram]:+,})\n"
    "Fancafe: {tots[daumcafe]:,} ({difs[daumcafe]:+,})\n"
    "VLIVE: {tots[vlive]:,} ({difs[vlive]:+,})\n"
    "Spotify: {tots[spotify]:,} ({difs[spotify]:+,})\n"
    "Melon: {tots[melon]:,} ({difs[melon]:+,})\n"
)

youtube_update = """\
{date} YouTube stats update 🤖

{kind}
{title}
▶️ http://youtu.be/{videoid}

👁️ {tots[views]:,.0f} ({rates[views]:,.0f})
❤️ {tots[likes]:,.0f} ({rates[likes]:,.0f})
💔 {tots[dislikes]:,.0f} ({rates[dislikes]:,.0f})
💬 {tots[comments]:,.0f} ({rates[comments]:,.0f})
"""

youtube_milestone = """\
{date} #OrbitStreamingWednesday 🤖

This video needs some love:
{title}
▶️ http://youtu.be/{videoid}

It needs {diff:,.0f} views to reach {milestone}. It should get there {prediction}, but we can make it happen faster!
"""
