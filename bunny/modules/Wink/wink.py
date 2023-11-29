import asyncio
import requests
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import *
from pyrogram.types import Message
from config import HANDLER as hl
from bunny.powers.basic import edit_or_reply, get_text
from bunny.core.clients import bunny as Client

@Client.on_message(filters.command("wink", hl) & filters.me)
async def wink(client: Client, message: Message):
    hmm_s = "https://some-random-api.ml/animu/wink"
    r = requests.get(url=hmm_s).json()
    image_s = r["link"]
    await client.send_video(message.chat.id, image_s)
    await message.delete()
