import discord, datetime
from discord import app_commands
from discord.ext import commands
from jikanpy import Jikan

jikan = Jikan()

class season(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @app_commands.command(name='season', description='Return the anime series of a season.')
    async def season(self, interaction: discord.Interaction, extension: str = None, season: str = None, year: int = None):
        list = ''
        if season != None: season = season.capitalize().replace(' ', '')
        if season != None and extension == None and year == None: year = datetime.datetime.now().year
        if season == None and year == None and extension == None: extension = 'now'
        if season != None or year != None: extension = None
        if extension != None:
             title = 'Now airing anime series' if extension.lower() == 'now' else 'Upcoming anime series'
        else: title = f'Anime series of {season} {year}'
        match season:
            case 'Winter':
                color = 0x24D4FF
            case 'Spring':
                color = 0xB6FF1B
            case 'Summer':
                color = 0xFF0000
            case 'Fall':
                color = 0xFFA500
            case _:
                color = 0xFFFE00
        for i in jikan.seasons(extension=extension, season = season, year = year)['data']:
            list += '- ' + i['title'] + '\n'
        embed = discord.Embed(title=title, description=list, color=color)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(season(bot))