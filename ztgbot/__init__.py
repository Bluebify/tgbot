s = "u"

from .config import API_ID, API_HASH, BOT_TOKEN

from pyrogram import Client

bot = Client("ZuliTgBot",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN
)