import asyncio
from pyrogram import *
from pyrogram import filters
from pyrogram.errors import YouBlockedUser
from pyrogram.types import *
from config import HANDLER as hl
from bunny.powers.basic import edit_or_reply
from bunny.core import extract_user
from bunny.core.clients import bunny as Client

@Client.on_message(filters.command(["sg", "sa", "sangmata"], hl) & filters.me)
async def sg(client: Client, message: Message):
    args = await extract_user(message)
    lol = await edit_or_reply(message, "`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            return await lol.edit(f"`Please specify a valid user!`")
    bot = "@SangMata_beta_bot"
    try:
        await client.send_message(bot, f"{user.id}")
    except YouBlockedUser:
        await client.unblock_user(bot)
        await client.send_message(bot, f"{user.id}")
    await asyncio.sleep(1)

    async for stalk in client.search_messages(bot, query="Name", limit=1):
        if not stalk:
            await message.edit_text("**Orang Ini Belum Pernah Mengganti Namanya**")
            return
        elif stalk:
            await message.edit(stalk.text)
            await stalk.delete()

    async for stalk in client.search_messages(bot, query="Username", limit=1):
        if not stalk:
            return
        elif stalk:
            await message.reply(stalk.text)
            await stalk.delete()
