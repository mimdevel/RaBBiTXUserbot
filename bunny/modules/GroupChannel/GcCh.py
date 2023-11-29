from pyrogram import Client, filters
from pyrogram.types import Message
from config import HANDLER as hl
from bunny.powers.basic import edit_or_reply
from bunny.core.clients import bunny as Client

@Client.on_message(filters.command("create", hl) & filters.me)
async def gcch(client: Client, message: Message):
    if len(message.command) < 3:
        return await edit_or_reply(
            message, f"__if you need help__\n\n `{hl}help create`"
        )
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    bunny = await edit_or_reply(message, "`Processing...`")
    fuk = "ʀᴀʙʙɪᴛx ᴜsᴇʀs" 
    if group_type == "gc": 
        _id = await client.create_supergroup(group_name, fuk)
        link = await client.get_chat(_id["id"])
        await bunny.edit(
            f"__successfully created your Group as: [{group_name}]({link['invite_link']})__",
            disable_web_page_preview=True,
        )
    elif group_type == "ch":  
        _id = await client.create_channel(group_name, fuk)
        link = await client.get_chat(_id["id"])
        await bunny.edit(
            f"__successfully created your channel as: [{group_name}]({link['invite_link']})__",
            disable_web_page_preview=True,
        )
