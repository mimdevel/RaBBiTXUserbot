import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatType, UserStatus
from pyrogram.types import Message
from config import HANDLER as hl
from config import LOG_GROUP_ID
from bunny.core.clients import bunny as Client
from bunny.powers.basic import edit_or_reply


@Client.on_message(filters.me & filters.command("invite", hl))
async def invite(client: Client, message: Message):
    mg = await edit_or_reply(message, "`adding Users.. please wait...`")
    user_s_to_add = message.text.split(" ", 1)[1]
    if not user_s_to_add:
        await mg.edit("__Give Me Username To Add that members here..!!__")
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except BaseException as e:
        await mg.edit(f"__๏ Unable To Add Users..!!__ \n\n**ERROR:** `{e}`")
        return
    await mg.edit(f"__๏ Sucessfully Added {len(user_list)} To This Group..!!__")


@Client.on_message(filters.command(["inviteall"], hl) & filters.me)
async def invteall(client: Client, message: Message):
    bunny = await edit_or_reply(message, "`Processing...⚡`")
    text = message.text.split(" ", 1)
    queryy = text[1]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    await bunny.edit_text(f"__๏ inviting users from {chat.username}...!!__")
    async for member in client.get_chat_members(chat.id):
        user = member.user
        sex = [
            UserStatus.ONLINE,
            UserStatus.OFFLINE,
            UserStatus.RECENTLY,
            UserStatus.LAST_WEEK,
        ]
        if user.status in sex:
            try:
                await client.add_chat_members(tgchat.id, user.id)
            except Exception as e:
                mg = await client.send_message(LOG_GROUP_ID, f"**ERROR:** `{e}`")
                await asyncio.sleep(0.3)
                await mg.delete()


@Client.on_message(filters.command("invitelink", hl) & filters.me)
async def invitelink(client: Client, message: Message):
    bunny = await edit_or_reply(message, "`Processing...⚡`")
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        message.chat.title
        try:
            link = await client.export_chat_invite_link(message.chat.id)
            await bunny.edit(f"**__๏ Link Invite:__** {link}")
        except Exception:
            await bunny.edit("__๏ Denied permission__")
