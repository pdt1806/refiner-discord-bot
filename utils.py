from typing import Tuple, Union
import discord
from discord import Activity, Game, CustomActivity, Streaming, Spotify

ActivityTypes = Union[Activity, Game, CustomActivity, Streaming, Spotify]

# ------------------ #

valid_types = [
    discord.ActivityType.playing,
    discord.ActivityType.streaming,
    discord.ActivityType.listening,
    discord.ActivityType.watching,
    discord.ActivityType.competing,
    discord.ActivityType.custom,
]


def get_activity_and_mood(member_activities: Tuple[ActivityTypes, ...]):
    try:
        activity, mood, rawActivity = {}, None, None

        activities = [
            activity for activity in member_activities if activity.type in valid_types]

        if activities[0].type == discord.ActivityType.custom:
            mood = activities[0].to_dict()
            if mood["emoji"]["id"]:
                mood["emoji"]["id"] = str(mood["emoji"]["id"])
            activities.pop(0)

        if activities:
            activities.sort(key=lambda activity: activity.type)
            rawActivity = activities[0]

        if rawActivity:
            activity["type"] = str(rawActivity.type).replace(
                "ActivityType.", "")
            match rawActivity.type:
                case discord.ActivityType.listening:
                    if isinstance(rawActivity, discord.Spotify):
                        activity.update({
                            "platform": "Spotify",
                            "name": rawActivity.title,
                            "artists": rawActivity.artists,
                            "album": {
                                "name": rawActivity.album,
                                "cover": rawActivity.album_cover_url,
                            },
                            "timestamps": {
                                "start": str(rawActivity.start),
                                "end": str(rawActivity.end),
                            },
                        })
                case discord.ActivityType.streaming:
                    activity.update({
                        "platform": rawActivity.platform,
                        "details": rawActivity.details,
                        "game": rawActivity.game,
                        "twitch_name": rawActivity.twitch_name,
                        "timestamps": {
                            "start": str(rawActivity.created_at),
                        },
                        "url": rawActivity.url,
                        "assets": rawActivity.assets
                    })
                case _:
                    activity.update({
                        "name": rawActivity.name,
                        "application_id": str(rawActivity.application_id),
                        "details": rawActivity.details,
                        "state": rawActivity.state,
                        "timestamps": rawActivity.timestamps,
                        "assets": rawActivity.assets,
                    })
        return activity if activity else None, mood
    except Exception as e:
        return None, None
