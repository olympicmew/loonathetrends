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


youtube_milestone_reached = """\
YouTube milestone bulletin 🤖

This @loonatheworld video:
{title}
▶️ http://youtu.be/{videoid}

has finally reached {views:,.0f} views! 🎊
Congratulations Orbits! 🎉 Keep going~
"""

youtube_statsdelivery = "@{user} Bleep bloop! You're served 🤖"
youtube_statsdelivery_nourl = "@{user} I think you forgot the YouTube link! 🤖"
youtube_statsdelivery_noloona = "@{user} I only have stats for LOONA videos, sorry! 🤖"
youtube_statsdelivery_smtm = "@{user} 😏 https://youtu.be/or6EBU-gKww"
youtube_statsdelivery_moebius = "@{user} Bleep bloop! You're served 🤖 https://youtu.be/DeoZhYJEn7o"
