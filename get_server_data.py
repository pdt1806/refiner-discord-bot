import json
from discord import Guild

async def get_data(path : str, guild: Guild):
    data = json.load(open(path + '/servers_data/data.json', 'r'))
    print(data[guild.id])
    if data[guild.id] == None:
        member_data = {}
        for member in guild.members:
            member_data.update({member.id: {
                "name": member.name,
                "joined_at": member.joined_at,
                "status": member.status,
                "display_name": member.display_name,
                "anime_list": [],
                "unwatched_anime": [],
                "watched_anime": [],
            }})
        data.update({guild.id: {
            "name": guild.name,
            "members": member_data,
        }})
        json.dump(data, open(path + '/servers_data/data.json', 'a'))
    await print('Data loaded!')
    return data[{guild.id}]
    