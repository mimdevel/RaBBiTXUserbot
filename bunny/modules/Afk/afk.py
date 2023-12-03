import os
import re
import sys
import asyncio
import traceback
import importlib
import subprocess
from io import BytesIO
from types import ModuleType
from typing import Dict
import asyncio
from datetime import datetime
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import HANDLER as prefix
from bunny.core.clients import bunny as Client

requirements_list = []

def import_library(library_name: str, package_name: str = None):
    """
    Loads a library, or installs it in ImportError case
    :param library_name: library name (import example...)
    :param package_name: package name in PyPi (pip install example)
    :return: loaded module
    """
    if package_name is None:
        package_name = library_name
    requirements_list.append(package_name)

    try:
        return importlib.import_module(library_name)
    except ImportError:
        completed = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name]
        )
        if completed.returncode != 0:
            raise AssertionError(
                f"Failed to install library {package_name} (pip exited with code {completed.returncode})",
                parse_mode=enums.ParseMode.HTML
            )
        return importlib.import_module(library_name)

humanize = import_library("humanize")

import humanize

AFK = False
AFK_REASON = ""
AFK_TIME = ""
USERS = {}
GROUPS = {}

# Helpers


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.id

    elif not message.from_user.is_self:
        reply_id = message.id

    return reply_id


def GetChatID(message: Message):
    """Get the group id of the incoming message"""
    return message.chat.id


def subtract_time(start, end):
    """Get humanized time"""
    subtracted = humanize.naturaltime(start - end)
    return str(subtracted)


# Main


@Client.on_message(
    ((filters.group & filters.mentioned) | filters.private)
    & ~filters.me
    & ~filters.service,
    group=3,
)
async def collect_afk_messages(bot: Client, message: Message):
    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME)
        is_group = True if message.chat.type in ["supergroup", "group"] else False
        CHAT_TYPE = GROUPS if is_group else USERS

        if GetChatID(message) not in CHAT_TYPE:
            text = (
                f"`Beep boop. This is an automated message.\n"
                f"I am not available right now.\n"
                f"Last seen: {last_seen}\n"
                f"Reason: ```{AFK_REASON.upper()}```\n"
                f"See you after I'm done doing whatever I'm doing.`"
            )
            await bot.send_message(
                chat_id=GetChatID(message),
                text=text,
                reply_to_message_id=ReplyCheck(message),
                parse_mode=enums.ParseMode.HTML,
            )
            CHAT_TYPE[GetChatID(message)] = 1
            return
        elif GetChatID(message) in CHAT_TYPE:
            if CHAT_TYPE[GetChatID(message)] == 50:
                text = (
                    f"`This is an automated message\n"
                    f"Last seen: {last_seen}\n"
                    f"This is the 10th time I've told you I'm AFK right now..\n"
                    f"I'll get to you when I get to you.\n"
                    f"No more auto messages for you`"
                )
                await bot.send_message(
                    chat_id=GetChatID(message),
                    text=text,
                    reply_to_message_id=ReplyCheck(message),
                    parse_mode=enums.ParseMode.HTML,
                )
            elif CHAT_TYPE[GetChatID(message)] > 50:
                return
            elif CHAT_TYPE[GetChatID(message)] % 5 == 0:
                text = (
                    f"`Hey I'm still not back yet.\n"
                    f"Last seen: {last_seen}\n"
                    f"Still busy: ```{AFK_REASON.upper()}```\n"
                    f"Try pinging a bit later.`"
                )
                await bot.send_message(
                    chat_id=GetChatID(message),
                    text=text,
                    reply_to_message_id=ReplyCheck(message),
                    parse_mode=enums.ParseMode.HTML,
                )

        CHAT_TYPE[GetChatID(message)] += 1


@Client.on_message(filters.command("afk", prefix) & filters.me, group=3)
async def afk_set(bot: Client, message: Message):
    global AFK_REASON, AFK, AFK_TIME

    cmd = message.command
    afk_text = ""

    if len(cmd) > 1:
        afk_text = " ".join(cmd[1:])

    if isinstance(afk_text, str):
        AFK_REASON = afk_text

    AFK = True
    AFK_TIME = datetime.now()

    await message.delete()


@Client.on_message(filters.command("afk", "!") & filters.me, group=3)
async def afk_unset(bot: Client, message: Message):
    global AFK, AFK_TIME, AFK_REASON, USERS, GROUPS

    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME).replace("ago", "").strip()
        await message.edit(
            f"`While you were away (for {last_seen}), you received {sum(USERS.values()) + sum(GROUPS.values())} "
            f"messages from {len(USERS) + len(GROUPS)} chats`",
            parse_mode=enums.ParseMode.HTML
        )
        AFK = False
        AFK_TIME = ""
        AFK_REASON = ""
        USERS = {}
        GROUPS = {}
        await asyncio.sleep(5)

    await message.delete()


@Client.on_message(filters.me, group=3)
async def auto_afk_unset(bot: Client, message: Message):
    global AFK, AFK_TIME, AFK_REASON, USERS, GROUPS

    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME).replace("ago", "").strip()
        reply = await message.reply(
            f"`While you were away (for {last_seen}), you received {sum(USERS.values()) + sum(GROUPS.values())} "
            f"messages from {len(USERS) + len(GROUPS)} chats`",
            parse_mode=enums.ParseMode.HTML,
        )
        AFK = False
        AFK_TIME = ""
        AFK_REASON = ""
        USERS = {}
        GROUPS = {}
        await asyncio.sleep(5)
        await reply.delete()