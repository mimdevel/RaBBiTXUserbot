import asyncio
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from config import *
from bunny.powers.basic import edit_or_reply
from bunny.core.misc import extract_user, extract_user_and_reason, list_admins
from config import HANDLER as hl
from bunny.core.clients import bunny as Client
from bunny.core.clients import DEVS

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)

@Client.on_message(filters.command(["kick", "shutup"], hl) & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    bunny = await edit_or_reply(message, "`ρяσ¢єѕѕιиg...⚡`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await bunny.edit("**__I don't have rights to kick anyone__**")
    if not user_id:
        return await bunny.edit("__**you're going to need to specify a user...!**__.")
    if user_id == client.me.id:
        return await bunny.edit("__**Yeahhh, I'm not going to kick myself.**__")
    if user_id == DEVS:
        return await bunny.edit("**__I can't kick him coz he is king of telegram..!!__**.")
    if user_id in (await list_admins(client, message.chat.id)):
        return await bunny.edit("**__I'm not gonna kick an admin... Though I reckon it'd be pretty funny.__**")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
**__๏ Kicked User »__** {mention}
**__๏ Kicked By »__** {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n**__๏ Reason »__** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await bunny.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await bunny.edit("**__ I'm not admin here..!! __**")

@Client.on_message(filters.group & filters.command("ban", hl) & filters.me)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    bunny = await edit_or_reply(message, "`ρяσ¢єѕѕιиg...⚡`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await bunny.edit("**__I don't have enough rights to ban anyone..!!**__")
    if not user_id:
        return await bunny.edit("__**you're going to need to specify a user...!!**__")
    if user_id == client.me.id:
        return await bunny.edit("__**You know what I'm not going to do? Ban myself..!!__**")
    if user_id in DEVS:
        return await bunny.edit("**__I can't ban him coz he is king of telegram..!!__**")
    if user_id in (await list_admins(client, message.chat.id)):
        return await bunny.edit("__**Why would I ban an admin? That sounds like a pretty dumb idea..!!__**")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    msg = (
        f"**__๏ Banned User »__** {mention}\n"
        f"**__๏ Banned By »__** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"**__๏ Reason »__** {reason}"
    await message.chat.ban_member(user_id)
    await bunny.edit(msg)

@Client.on_message(filters.group & filters.command("unban", hl) & filters.me)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    bunny = await edit_or_reply(message, "`ρяσ¢єѕѕιиg...⚡`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await bunny.edit("__**I don't have enough rights to unban anyone..!!**__")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await bunny.edit("**__I can't unban a channel..!!__**")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await bunny.edit(
            "**__you're going to need to specify a user..!!__**"
        )
    await message.chat.unban_member(user)
    umention = (await client.get_users(user)).mention
    await bunny.edit(f"**__๏ Unbanned »__** {umention}")

@Client.on_message(filters.command(["pin", "unpin"], hl) & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await edit_or_reply(message, "__**You need to reply to a message to pin it..!!**__")
    bunny = await edit_or_reply(message, "`ρяσ¢єѕѕιиg...⚡`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_pin_messages:
        return await bunny.edit("**__I don't have enough rights to pin messages..!!__**")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await bunny.edit(
            f"**__๏ Unpinned [this]({r.link}) message.__**",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await bunny.edit(
        f"**__๏ Pinned [this]({r.link}) message.__**",
        disable_web_page_preview=True,
    )

@Client.on_message(filters.command("mute", hl) & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    bunny = await edit_or_reply(message, "`ρяσ¢єѕѕιиg...⚡`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await bunny.edit("__**I don't have enough rights to mute anyone..!!**__")
    if not user_id:
        return await bunny.edit("__**you're going to need to specify a user..!!**__")
    if user_id == client.me.id:
        return await bunny.edit("__**You know what I'm not going to do? Mute myself..!!**__")
    if user_id in DEVS:
        return await bunny.edit("__**I can't mute him coz he is king of telegram..!!**__")
    if user_id in (await list_admins(client, message.chat.id)):
        return await bunny.edit("__**Ehhh, I'd rather not get involved in muting an admin. I'll stick to muting normal users, thanks..!!**__")
    mention = (await client.get_users(user_id)).mention
    msg = (
        f"**__๏ Muted User »__** {mention}\n"
        f"**__๏ Muted By »__** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"**__๏ Reason  »__** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await bunny.edit(msg)


@Client.on_message(
    filters.group & filters.command(["setchatphoto", "setgpic"], hl) & filters.me
)
async def set_chat_photo(client: Client, message: Message):
    zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.edit_text("**__You don't have enough rights to change group pfp..!!__**")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await message.edit_text("**__Reply to a photo to set it as group pfp..!!__**")

@Client.on_message(filters.group & filters.command("unmute", hl) & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    bunny = await edit_or_reply(message, "`ρяσ¢єѕѕιиg...⚡`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await bunny.edit("**__I don't have enough rights to unmute anyone..!!__**")
    if not user_id:
        return await bunny.edit("**__you're going to need to specify a user..!!**__.")
    await message.chat.restrict_member(user_id, permissions=unmute_permissions)
    umention = (await client.get_users(user_id)).mention
    await bunny.edit(f"**__๏ Unmuted __** {umention}")



@Client.on_message(
    filters.group & filters.command(["promote", "fullpromote"], hl) & filters.me
)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    umention = (await client.get_users(user_id)).mention
    bunny = await edit_or_reply(message, "`ρяσ¢єѕѕιиg...⚡`")
    if not user_id:
        return await bunny.edit("**__you're going to need to specify a user..!!__**")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_promote_members:
        return await bunny.edit("**__I don't have enough rights to promote anyone..!!**__")
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True,
            ),
        )
        return await bunny.edit(f"**__๏ Fully Promoted »__** {umention}")

    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_promote_members=False,
        ),
    )
    await bunny.edit(f"**__๏ Promoted »__** {umention}")

@Client.on_message(filters.group & filters.command("demote", hl) & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    bunny = await edit_or_reply(message, "`ρяσ¢єѕѕιиg...⚡`")
    if not user_id:
        return await bunny.edit("**__you're going to need to specify a user..!!**__")
    if user_id == client.me.id:
        return await bunny.edit("**__I am not going to demote myself..!!__**")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    umention = (await client.get_users(user_id)).mention
    await bunny.edit(f"**__๏ Demoted »**__ {umention}")
