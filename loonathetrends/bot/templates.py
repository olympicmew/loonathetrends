def followers_update(**fillin):
    is_daily = fillin["freq"] == "daily"
    s = "\n".join(
        "{date} @loonatheworld SNS follower counts {freq} update 🤖",
        "",
        "YouTube: {tots[youtube]:,} ({difs[youtube]:+,})" if is_daily else None,
        "Twitter: {tots[twitter]:,} ({difs[twitter]:+,})",
        "Instagram: {tots[instagram]:,} ({difs[instagram]:+,})",
        "Fancafe: {tots[daumcafe]:,} ({difs[daumcafe]:+,})",
        "VLIVE: {tots[vlive]:,} ({difs[vlive]:+,})",
        "Spotify: {tots[spotify]:,} ({difs[spotify]:+,})",
        "Melon: {tots[melon]:,} ({difs[melon]:+,})",
    )
    return s.format(**fillin)


youtube_update = "\n".join(
    (
        "{date} YouTube stats update 🤖",
        "",
        "{kind}",
        "{title}",
        "▶️ http://youtu.be/{videoid}",
        "",
        "👁️ {tots[views]:,.0f} ({rates[views]:,.0f})",
        "❤️ {tots[likes]:,.0f} ({rates[likes]:,.0f})",
        # "💔 {tots[dislikes]:,.0f} ({rates[dislikes]:,.0f})",
        "💬 {tots[comments]:,.0f} ({rates[comments]:,.0f})",
    )
).format

youtube_milestone = """\
{date} It's #OrbitStreamingTime! 🤖

This @loonatheworld video needs some love:
{title}
▶️ http://youtu.be/{videoid}

It needs {diff:,.0f} views to reach {milestone}. It should get there {prediction}, but we can make it happen faster!
""".format

youtube_milestone = "\n".join(
    "{date} It's #OrbitStreamingTime! 🤖",
    "",
    "This @loonatheworld video needs some love:",
    "{title}",
    "▶️ http://youtu.be/{videoid}",
    "",
    "It needs {diff:,.0f} views to reach {milestone}. It should get there {prediction}, but we can make it happen faster!)",
).format


def youtube_milestone_reached(**fillin):
    celebration = fillin.pop("celebration")
    s = "\n".join(
        (
            "YouTube milestone bulletin 🤖",
            "",
            "This @loonatheworld video:",
            "{title}",
            "▶️ http://youtu.be/{videoid}",
            "",
            "",
        )
    )
    if not celebration:
        s += "has reached {views:,.0f} views!"
    else:
        s += "\n".join(
            (
                "has finally reached {views:,.0f} views! 🎊",
                "Congratulations Orbits! 🎉 Keep going~",
            )
        )
    return s.format(**fillin)


youtube_statsdelivery = "@{user} Bleep bloop! You're served 🤖".format
youtube_statsdelivery_nourl = "@{user} I think you forgot the YouTube link! 🤖".format
youtube_statsdelivery_noloona = (
    "@{user} I only have stats for LOONA videos, sorry! 🤖".format
)
youtube_statsdelivery_smtm = "@{user} 😏 https://youtu.be/or6EBU-gKww".format
youtube_statsdelivery_moebius = (
    "@{user} Bleep bloop! You're served 🤖 https://youtu.be/DeoZhYJEn7o".format
)
