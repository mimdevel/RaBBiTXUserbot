from pyrogram import Client, __version__ as pyro
import asyncio

API_ID = input("\nEnter your api_id to continue\n» ")
API_HASH = input("\nEnter Your api_hash to continue\n» ")
bunny = Client("bunny", api_id=API_ID, api_hash=API_HASH, in_memory=True)
async def start():
    await bunny.start()
    pussy = await bunny.export_session_string()
    sexx = f"Your Pyrogram {pyro} String Session is here\n\n<code>{pussy}</code>\n\nif you want you can join support group  @RaBBiTXUserBot"
    segss = await bunny.send_message("me", txt)
    print(f"Pyrogram {pyro} SESSION successfully generated and sended in you save message on telegram THANK YOU FOR USING RABBITX ")
asyncio.run(start())
