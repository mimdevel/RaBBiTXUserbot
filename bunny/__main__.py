from bunny.core.clients import bunny, bot
import asyncio
import time
import importlib
from pyrogram import Client, idle
from config import LOG_GROUP_ID
from bunny.modules import ALL_MODULES
from config import HANDLER as hl

async def start_user():
    await bot.start()
    print("[•bunny•]: єνєяутнιиg ιѕ σк, ѕтαятιиg... уσυя υѕєявσт ρℓєαѕє ωαιт... ⚡")
    for all_module in ALL_MODULES:
        importlib.import_module("bunny.modules" + all_module)
        print(f"[•bunny•] ѕυ¢¢єѕѕfυℓℓу ιмρσятє∂ {all_module} ⚡")
    await bunny.start()
    x = await bunny.get_me()
    print(f"υѕєявσт ѕυ¢¢єѕѕfυℓℓყ ѕтαятє∂ αѕ {x.first_name} ⚡ ")
    try:
     await bunny.join_chat("RaBBiT_GuYs")
     await bunny.join_chat("userbot_developers")
    except:
      pass
    try:
     await bunny.send_message(-1001795756149, "__**ѕтαятє∂ !!**__")
    except:
      pass
    await idle()
  
loop = asyncio.get_event_loop()
loop.run_until_complete(start_user())
