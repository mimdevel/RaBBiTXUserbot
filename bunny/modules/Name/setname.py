from bunny.powers.basic import edit_or_reply
from bunny.core.misc import extract_user
from pyrogram import Client, filters
from config import HANDLER as hl
from bunny.core.clients import bunny as Client
from pyrogram.types import Message

@Client.on_message(filters.command(["setname"], hl) & filters.me)
async def name(client: Client, message: Message):
    bunny = await edit_or_reply(message, "`ρяσ¢єѕѕιиg...⚡`")
    if len(message.command) == 1:
        return await bunny.edit(
            "**__give me that name..!!__**"
        )
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await bunny.edit(f"**__๏ {name} successfully changed your account name..!!__**")
        except Exception as e:
            await bunny.edit(f"**__๏ ERROR »__** `{e}`")
    else:
        return await bunny.edit(
            "__**give me a that text..!!**__"
                  )
