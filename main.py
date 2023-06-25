# https://discord.com/api/oauth2/authorize?client_id=1121931862546329631&permissions=53320143531056&scope=bot

import discord, os, json, asyncio, sys
from discord import Guild
from discord.ext import commands

#------------------#

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='ar!', application_id='1121931862546329631')

path : str = os.path.dirname(sys.argv[0])

# servers_data = {}

#------------------#

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='ar!', intents=discord.Intents.all())
        self.cogslist = ['hi', 'season', 'waifu']

    async def on_ready(self):
        for guildname in self.guilds:
            print(f'Joined {guildname.name}')
            # await get_data(path, guildname)
        synced = await bot.tree.sync()
        print(f'{len(synced)} application commands synced!')
        
    async def on_guild_join(guild: Guild):
        print(f'Joined {guild.name}')

    async def load(self):
        for cog in self.cogslist:
            await bot.load_extension(f'cogs.{cog}')
            print(f'Loaded {cog} cog!')
    

# async def get_data(path : str, guild: Guild):
#     data : dict = json.load(open(path + '/servers_data/data.json'))
#     print(data)
#     if not data[{guild.id}]:
#         member_data = {}
#         for member in guild.members:
#             member_data.update({member.id: {
#                 "name": member.name,
#                 "joined_at": member.joined_at,
#                 "status": member.status,
#                 "display_name": member.display_name,
#                 "anime_list": [],
#                 "unwatched_anime": [],
#                 "watched_anime": [],
#             }})
#         await data.update({guild.id: {
#             "name": guild.name,
#             "members": member_data,
#         }})
#         await json.dump(data, path + '/servers_data/data.json', 'a')
#     await print('Data loaded!')
#     return data[{guild.id}]

#------------------#

bot = Bot()

async def main():
    async with bot:
        config = json.load(open(path + '/config.json', 'r'))
        await bot.load()
        await bot.start(config["token"])

asyncio.run(main())