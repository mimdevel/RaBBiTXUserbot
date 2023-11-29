import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from config import HANDLER as hl
from bunny.core.clients import bunny as Client

API_URL = "https://api.nekosapi.com/v2/images/random"

@Client.on_message(filters.command("randomanime", hl) & filters.me)
async def anime(client: Client, message: Message):
    await message.edit("`processing...`")
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()["data"]["attributes"]
        image_url = data["file"]
        title = data["title"]
    except (requests.exceptions.RequestException, KeyError):
        await message.edit("__Failed to send rendom anime pic..!!__.")
        return

    await client.send_photo(message.chat.id, image_url, caption=f"**Title:** {title}")
    await message.edit("__Random anime pic sent..!!__")
