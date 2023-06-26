import discord
from discord.ext import commands
from discord import app_commands
from waifuim import WaifuAioClient

wf = WaifuAioClient()

class waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='waifu', description='Send you a waifu pic.')
    async def waifu(self, interaction : discord.Interaction):
        image : str = await wf.search(included_tags=['waifu'])
        await interaction.response.send_message(image)

async def setup(bot):
    await bot.add_cog(waifu(bot))