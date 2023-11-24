import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os
from flask import Flask, jsonify
from flask_cors import CORS
import threading

load_dotenv()

TOKEN = os.environ['TOKEN']

app = Flask(__name__)
CORS(app, resources={
     r"/*": {"origins": "https://disi.bennynguyen.us"}}, supports_credentials=True)  # normal one

bot = commands.Bot(intents=discord.Intents.all(),
                   command_prefix='ref!', application_id='1121931862546329631')


# ------------------#

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='ref!', intents=discord.Intents.all())
        self.cogslist = ['waifu']

    async def on_ready(self):
        for guildname in self.guilds:
            print(f'Joined {guildname.id}')
        synced = await bot.tree.sync()
        print(f'{len(synced)} application commands synced!')

        thread = threading.Thread(target=self.start_flask_server)
        thread.start()

    def start_flask_server(self):
        app.run(port=7000)

    async def on_guild_join(guild: discord.Guild):
        print(f'Joined {guild.name}')

    async def load(self):
        for cog in self.cogslist:
            await bot.load_extension(f'cogs.{cog}')
            print(f'Loaded {cog} cog!')


# ------------------#

bot = Bot()

guild = bot.guilds[0]

@app.route('/')
def home():
    return jsonify({'message': 'API of Refiner Discord Bot'})


@app.route('/user/<userid>', methods=['GET'])
def get_user_info(userid):
    if not userid:
        return jsonify({'error': 'ID parameter is missing.'}), 400

    

    member = discord.utils.find(lambda m: m.id == int(userid), guild.members)

    if not member:
        return jsonify({'error': 'User not found in the server.'}), 404

    user_info = {
        'id': member.id,
        'username': member.name,
        'avatar': member.avatar.url,
        'status': member.status[0],
        # 'banner': member.banner.url if member.banner else None,
        'created_at': member.created_at.strftime('%m-%d-%Y %H:%M:%S'),
    }

    return jsonify(user_info)

@app.route('/username/<username>', methods=['GET'])
def get_user_info(username):
    if not username:
        return jsonify({'error': 'Username parameter is missing.'}), 400


    member = discord.utils.find(lambda m: m.name == int(username), guild.members)

    if not member:
        return jsonify({'error': 'User not found in the server.'}), 404

    user_info = {
        'id': member.id,
    }

    return jsonify(user_info)


async def run_bot():
    await bot.load()
    await bot.start(TOKEN)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

    loop.run_until_complete(bot.start(TOKEN))
