import discord
from discord.ext import commands
from discord import app_commands
from jikanpy import Jikan

jikan = Jikan()

class hi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='hi', description='hi')
    async def hi(self, interaction : discord.Interaction):
        await interaction.response.send_message(f"Hi {interaction.user.mention}!")

async def setup(bot):
    await bot.add_cog(hi(bot))