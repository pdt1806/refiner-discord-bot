import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import uvicorn
from discord import Spotify


load_dotenv()

TOKEN = os.environ['TOKEN']

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://disi.bennynguyen.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = commands.Bot(intents=discord.Intents.all(),
                   command_prefix='ref!', application_id='1121931862546329631')

# ------------------#


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='ref!', intents=discord.Intents.all())
        self.cogslist = ['waifu']

    async def on_ready(self):
        await self.start_fastapi_server()

    async def start_fastapi_server(self):
        config = uvicorn.Config(app, host="127.0.0.1", port=7000)
        server = uvicorn.Server(config)
        loop = asyncio.get_event_loop()
        loop.create_task(server.serve())

    async def load(self):
        for cog in self.cogslist:
            await bot.load_extension(f'cogs.{cog}')


# ------------------#

bot = Bot()


@app.get("/")
def home():
    return {"message": "API of Refiner Discord Bot"}


@app.get("/user/{userid}")
async def get_user_info(userid: int):
    if not userid:
        raise HTTPException(status_code=400, detail="ID parameter is missing.")

    try:
        member = await bot.fetch_user(userid)
    except discord.NotFound:
        raise HTTPException(status_code=404, detail="User not found.")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")

    guild = bot.guilds[0]

    member2 = discord.utils.find(lambda m: m.id == userid, guild.members)

    if not member or not member2:
        raise HTTPException(
            status_code=404, detail="User not found in the server.")

    activity = {}
    if member2.activity:
        activity["type"] = str(member2.activity.type).replace(
            "ActivityType.", "")
        match member2.activity.type:
            case discord.ActivityType.listening:
                if isinstance(member2.activity, Spotify):
                    activity.update({
                        "name": member2.activity.title,
                        "artists": member2.activity.artists,
                        "album": {
                            "name": member2.activity.album,
                            "cover": member2.activity.album_cover_url,
                        },
                        "timestamp": {
                            "duration": str(member2.activity.duration),
                            "start": str(member2.activity.start),
                            "end": str(member2.activity.end),
                        },
                    })
            case _:
                activity.update({
                    "name": member2.activity.name,
                    "details": member2.activity.details,
                    "state": member2.activity.state,
                    "timestamps": member2.activity.timestamps,
                    "assets": member2.activity.assets,
                })

    try:
        user_info = {
            "id": str(member.id),
            "username": member.name,
            "display_name": member.display_name,
            "avatar": member.avatar.url if member.avatar else member.default_avatar.url if member.default_avatar else None,
            "status": str(member2.status[0]),
            "banner": member.banner.url.replace("size=512", "size=1024") if member.banner else None,
            "accent_color": str(member.accent_color) if member.accent_color else None,
            "created_at": member.created_at.strftime("%m-%d-%Y"),
            "activity": activity if activity else None,
        }
        return JSONResponse(content=user_info)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/username/{username}")
def get_id(username: str):
    if not username:
        raise HTTPException(
            status_code=400, detail="Username parameter is missing.")

    guild = bot.guilds[0]

    member = discord.utils.find(lambda m: m.name == username, guild.members)

    if not member:
        raise HTTPException(
            status_code=404, detail="User not found in the server.")

    return {"id": str(member.id)}


async def run_bot():
    await bot.load()
    await bot.start(TOKEN)


if __name__ == '__main__':
    asyncio.run(run_bot())
