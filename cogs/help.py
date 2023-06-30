import discord
from discord import app_commands
from discord.ext import commands
from jikanpy import Jikan

jikan = Jikan()

class helpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.page = 1
        self.pagesNum = 2
    @discord.ui.button(label='<', style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction):
        if self.page > 1: self.page -= 1
        help.update_embed(interaction, self.page, self.pagesNum)
    @discord.ui.button(label='>', style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction):
        if self.page < self.pagesNum: self.page += 1
        help.update_embed(interaction, self.page, self.pagesNum)

class help(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.season = """
Return the anime series of a season.

**Usage**: `/season [extension] [season] [year]`

**Parameters**:
- `extension`: Optional. Can be `now` or `upcoming`. Return the now airing anime series or the upcoming anime series.
- `season`: Optional. Can be `winter`, `spring`, `summer` or `fall`. 
- `year`: Optional. Can be any year. If not specified, the current year will be used.

**Default return value**: The now airing anime series of the current season.
"""

    async def create_embed(self, page: int = 1, pagesNum: int = 2):
        embed = discord.Embed(title=f'Omoka-chan\'s guide!', description="I'm going to lead you through *everything~*", color=0xFFF700)
        embed.set_thumbnail(url=self.bot.user.avatar)
        match page:
            case 1:
                embed.add_field(name='/season', value=self.season, inline=False)
            case 2:
                embed.add_field(name='/waifu', value='Send you a waifu pic.', inline=False)
        embed.set_footer(text=f'Page {page} of {pagesNum}')
        return embed

    @app_commands.command(name='help', description='The ultimate guide of Omoka-chan.')
    async def help(self, interaction: discord.Interaction):
        embed = await self.create_embed()
        await interaction.response.send_message(embed=embed, view=helpView())
    
    async def update_embed(self, interaction: discord.Interaction, page: int, pagesNum: int):
        print('hi')
        embed = await self.create_embed(page, pagesNum)
        await interaction.response.defer()
        await interaction.response.edit_message(embed=embed, view=helpView())

async def setup(bot):
    await bot.add_cog(help(bot))