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
        image = await wf.search(included_tags=['waifu'])
        await interaction.response.send_message(f"Here's your pic {interaction.user.mention} :3", files=[discord.File(image)])

async def setup(bot):
    await bot.add_cog(waifu(bot))