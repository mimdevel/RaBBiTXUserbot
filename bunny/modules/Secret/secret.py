import os
from pyrogram import Client, filters
from bunny.core.clients import bunny as Client
from config import HANDLER as hl

@Client.on_message(filters.command("wow",  hl) & filters.private & filters.me)
async def self_media(client, message):
    replied = message.reply_to_message
    if not replied:
        return
    if not (replied.photo or replied.video):
        return
    geek = await client.download_media(replied)
    await client.send_document("me", geek)
    os.remove(geek)
