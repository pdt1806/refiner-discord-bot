import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import uvicorn
from utils import extract_urls, get_activity_and_mood
import asyncio
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


load_dotenv()

TOKEN = os.environ['TOKEN']


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://disi.bennynguyen.dev"],
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

bot = commands.Bot(intents=discord.Intents.all(),
                   command_prefix='ref!', application_id='1121931862546329631')

# ------------------ #


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


# ------------------ #


bot = Bot()


@app.get("/")
def home():
    return {"message": "API of Refiner Discord Bot"}


@app.get("/user/{userid}")
@limiter.limit("60/minute")
async def get_user_info(request: Request, userid: str, full: str = "false"):
    if not userid:
        raise HTTPException(status_code=400, detail="ID parameter is missing.")
    fullRequired = full.lower() == "true"

    guild = bot.guilds[0]

    member_short = discord.utils.find(
        lambda m: str(m.id) == userid, guild.members)

    if not member_short:
        raise HTTPException(
            status_code=404, detail="User not found in the server.")

    activity, mood = get_activity_and_mood(member_short.activities)

    # The followings require full data (which means longer time, about 150-200ms):
    #     - accent_color
    #     - banner

    member = await bot.fetch_user(userid) if fullRequired else None

    # Full data => fetch_user => Discord API => 150-200ms

    try:
        user_info = {
            "id": str(member.id),
            "username": member.name,
            "display_name": member.display_name,
            "avatar": member.avatar.url.replace("size=1024", "size=512") if member.avatar else member.default_avatar.url if member.default_avatar else None,
            "status": str(member_short.status[0]),
            "banner": member.banner.url.replace("size=512", "size=1024") if member.banner else None,
            "accent_color": str(member.accent_color) if member.accent_color else None,
            "created_at": member.created_at.strftime("%m-%d-%Y"),
            "activity": activity,
            "mood": mood,
        } if fullRequired else {
            "id": str(member_short.id),
            "username": member_short.name,
            "display_name": member_short.display_name,
            "avatar": member_short.avatar.url.replace("size=1024", "size=512") if member_short.avatar else member_short.default_avatar.url if member_short.default_avatar else None,
            "status": str(member_short.status[0]),
            "created_at": member_short.created_at.strftime("%m-%d-%Y"),
            "activity": activity,
            "mood": mood,
        }

        urls = extract_urls(user_info)
        user_info["urls"] = urls

        return JSONResponse(content=user_info)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/username/{username}")
@limiter.limit("5/minute")
def get_id(request: Request, username: str):
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
