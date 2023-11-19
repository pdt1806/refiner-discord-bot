import discord
import asyncio
from discord import Guild
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ['TOKEN']


bot = commands.Bot(intents=discord.Intents.all(),
                   command_prefix='ar!', application_id='1121931862546329631')


# ------------------#

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='ar!', intents=discord.Intents.all())
        self.cogslist = ['waifu']

    async def on_ready(self):
        for guildname in self.guilds:
            print(f'Joined {guildname.id}')
        synced = await bot.tree.sync()
        print(f'{len(synced)} application commands synced!')

    async def on_guild_join(guild: Guild):
        print(f'Joined {guild.name}')

    async def load(self):
        for cog in self.cogslist:
            await bot.load_extension(f'cogs.{cog}')
            print(f'Loaded {cog} cog!')

# ------------------#


bot = Bot()


async def main():
    async with bot:
        await bot.load()
        await bot.start(TOKEN)

asyncio.run(main())
