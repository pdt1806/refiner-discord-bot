import discord, datetime
from discord import app_commands
from discord.ext import commands
from jikanpy import Jikan

jikan = Jikan()

class help(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @app_commands.command(name='help', description='The ultimate guide of Omoka-chan.')
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f'Omoka-chan\'s guide!', description="I'm going to lead you through *everything~*", color=0xFFF700)
        embed.set_thumbnail(url=self.bot.user.avatar)
        await interaction.response.send_message(embed=embed)

    def waifu(embed):
        embed.add_field(name='waifu', value='Send you a waifu pic.', inline=False)

async def setup(bot):
    await bot.add_cog(help(bot))