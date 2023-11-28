import os
import re
import aiofiles
from pyrogram import Client, filters
from pyrogram.types import Message
from config import *
from bunny.powers.basic import edit_or_reply
from bunny.core.pastebin import paste
from config import HANDLER as hl
from bunny.core.clients import bunny as Client

pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


@Client.on_message(filters.command("paste", hl) & filters.me)
async def paste_func(client: Client, message: Message):
    if not message.reply_to_message:
        return await edit_or_reply(message, f"__**Reply To A Message With {hl}paste...**__")
    r = message.reply_to_message
    if not r.text and not r.document:
        return await edit_or_reply(message, "__**Only text and documents are supported...__**")
    bunny = await edit_or_reply(message, "`ραѕтιиg...`")
    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await bunny.edit("__**You can only paste files smaller than 40KB.__**")
        if not pattern.search(r.document.mime_type):
            return await bunny.edit("__**Only text files can be pasted.__**")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()
        os.remove(doc)
    link = await paste(content)
    try:
        if bunny.from_user.is_bot:
            await message.reply_photo(
                photo=link,
                quote=False,
                reply_markup=kb,
            )
        else:
            await message.reply_photo(
                photo=link,
                quote=False,
                caption=f"**Paste Link:** [Here]({link})",
            )
        await bunny.delete()
    except Exception:
        await bunny.edit(f"[Here]({link}) your paste")
