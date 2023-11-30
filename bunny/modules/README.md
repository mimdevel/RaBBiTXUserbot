# This is an example of a simple plugin for Rabbituserbot. 

```python3
from pyrogram import Client, filters
from bunny.core.clients import bunny
from config import HANDLER as hl

@bunny.on_message(filters.command("ping", hl ))
async def ping(_, message):
    await message.reply_text("Pong!")
```
