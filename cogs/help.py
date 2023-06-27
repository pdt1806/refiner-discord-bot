import discord, datetime
from discord import app_commands
from discord.ext import commands
from jikanpy import Jikan

jikan = Jikan()

class help(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.pagesNum: int = 3
        self.page: int = 1
    
    @app_commands.command(name='help', description='The ultimate guide of Omoka-chan.')
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f'Omoka-chan\'s guide!', description="I'm going to lead you through *everything~*", color=0xFFF700)
        embed.set_thumbnail(url=self.bot.user.avatar)
        match self.page:
            case 1:
                embed.add_field(name='season', value='Return the anime series of a season.', inline=False)
            case _:
                embed.add_field(name='waifu', value='Send you a waifu pic.', inline=False)
        embed.set_footer(text=f'Page {self.page} of {self.pagesNum}')
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(help(bot))