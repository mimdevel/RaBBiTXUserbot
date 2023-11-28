from os import getenv
import os

# API_IDS ~ my.telegram.org
API_ID = int(getenv("API_ID", None)) # API_ID get it from my.telegram.org
API_HASH = getenv("API_HASH", None) # API_HASH get ut from my.telegram.org

# SESSIONS ~ python3 RaBBiTgram.py
STRING_SESSION = getenv("STRING_SESSION", None) # SESSION get it by run cmd "python3 RaBBiTgram.py" in heroku consol or locally 
BOT_TOKEN = getenv("BOT_TOKEN",None) # BOT_TOKEN get it from @BotFather Bot on telegram

# DATABASES ~ mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", None) # MONGO_DB_URL get it from mongodb.com

# LOGGGERS ~ telegram private group
LOG_GROUP_ID = getenv("LOG_GROUP_ID", None) # LOG_GROUP_ID get it by creating private group on telegram and fill here that's group id

# HANDLER ~ use ( .,-,!,+,-) any symbol like this...
HANDLER = getenv("HANDLER", None) # HANDLER choose your bot command handler

# IMAGES ~ telegram link of pic
ALIVE_PIC = getenv("ALIVE_PIC", None) # ALIVE_PIC a pic link for alive command in bot
if not ALIVE_PIC:
    ALIVE_PIC = "https://telegra.ph//file/342f127c890603ea346b5.jpg"
    
HELP_PIC = getenv("HELP_PIC", None) # HELP_PIC a pic link for help commad in bot

# SUDO_USERS ~ ( not necessary )
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
if not SUDO_USERS:
    SUDO_USERS = [6647321265]
    
# BLACKLISTED CHATS ~ ( not necessary )
BLACKLIST_CHAT = getenv("BLACKLIST_CHAT", None) # BLACKLISTED CHATS your telegram group id ( not necessary )
if not BLACKLIST_CHAT:
    BLACKLIST_CHAT = [-1001901276605]

# BIO ~ any message in any font for bio ( not necessary )
BIO = os.environ.get("BIO", "〆 яαввιтχ υѕєявσт υѕєя 〆") # BIO for clone and revert commands
