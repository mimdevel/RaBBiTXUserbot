from pyrogram.types import Message
from config import HANDLER as hl
from bunny.powers.basic import get_text
import requests
from pyrogram import Client, filters
from bunny.core.clients import bunny as Client

@Client.on_message(filters.command("trump", hl) & filters.me)
async def tweet(client: Client, message: Message):
    text = get_text(message)
    if not text:
        await message.edit(f"`give me somthing to tweet...`")
        return
    url = f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}"
    r = requests.get(url=url).json()
    tweet = r["message"]
    await message.edit(f"`Trump is tweeting...`")
    await client.send_photo(message.chat.id, tweet)
    await message.delete()
