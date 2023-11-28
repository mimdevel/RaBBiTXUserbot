from pyrogram import Client, filters
from pyrogram.types import Message
from bunny.powers.tools import get_arg
from asyncio import sleep
from config import HANDLER as hl
from bunny.core.clients import bunny as Client

spam_chats = []

@Client.on_message(filters.command("tagall", hl) & filters.me)
async def mentions(client: Client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    direp = message.reply_to_message
    args = get_arg(message)
    if not direp and not args:
        return await message.reply(f"**__» give  a message or reply to any message..!!**__\n\n**๏ Example** » `{hl}tagall hlww everyone` !!**")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}), "
        if usrnum == 5:
            if args:
                txt = f"{args}\n{usrtxt}"
                await client.send_message(chat_id, txt)
            elif direp:
                await direp.reply(usrtxt)
            await sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@Client.on_message(filters.command("cancel", hl) & filters.me)
async def canceltagall(client: Client, message: Message):
    if not message.chat.id in spam_chats:
        return await message.edit("**__» I'm not tagging anyone here so I can't cancel either..!!__**")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.edit("**__๏ Successfully Cancel taging members..!!⚡__**")
