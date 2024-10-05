# (c) @AbirHasan2005

import os
from handlers.helpers import os

ok = "@Tamilan_BotsZ"

class Config(object):
	API_ID = int(os.environ.get("API_ID", "0"))
	API_HASH = os.environ.get("API_HASH")
	BOT_TOKEN = os.environ.get("BOT_TOKEN")
	BOT_USERNAME = os.environ.get("BOT_USERNAME")
	DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-100"))
	BOT_OWNER = int(os.environ.get("BOT_OWNER", "1445283714"))
	DATABASE_URL = os.environ.get("DATABASE_URL")
	UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "")
	LOG_CHANNEL = os.environ.get("LOG_CHANNEL", None)
	BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "1234567890").split())
	FORWARD_AS_COPY = bool(os.environ.get("FORWARD_AS_COPY", True))
	BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", False))
	BANNED_CHAT_IDS = list(set(int(x) for x in os.environ.get("BANNED_CHAT_IDS", "-1001362659779 -1001255795497").split()))
	OTHER_USERS_CAN_SAVE_FILE = bool(os.environ.get("OTHER_USERS_CAN_SAVE_FILE", True))
	ABOUT_BOT_TEXT = f"""Iᴀᴍ Pᴇʀᴍᴀɴᴇɴᴛ Fɪʟᴇ Sᴛᴏʀᴇ Bᴏᴛ ﹗ Wɪᴛʜ Mᴀɴʏ Fᴇᴀᴛᴜʀᴇs ﹗ Mᴀᴅᴇᴅ Bʏ TᴀᴍɪʟᴀɴBᴏᴛsZ ﹗
	
🤖 **Mʏ Nᴀᴍᴇ Is :** [Files Store Bot](https://t.me/{BOT_USERNAME})

📝 **Lᴀɴɢᴜᴀɢᴇ :** [Python3](https://www.python.org)

📚 **Lɪʙʀᴀʀʏ :** [Pyrogram](https://docs.pyrogram.org)

📡 **Hᴏsᴛᴇᴅ Oɴ :** [Heroku](https://heroku.com)

🧑🏻‍💻 **Dᴇᴠᴇʟᴏᴩᴇʀ :** @AbirHasan2005

👥 **Sᴜᴩᴩᴏʀᴛ Gʀᴏᴜᴩ :** [Tᴀᴍɪʟᴀɴ BᴏᴛsZ Sᴜᴩᴩᴏʀᴛ](https://t.me/DevsZone)

📢 **Uᴩᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ :** [Tᴀᴍɪʟᴀɴ BᴏᴛsZ](https://t.me/Discovery_Updates)
"""
repo_credits = REMOVING_CREDITS
repo = REPO

	ABOUT_DEV_TEXT = f"""
🧑🏻‍💻 **Dᴇᴠᴇʟᴏᴩᴇʀ :** @Sharathitsisme 🐣

Dᴇᴠᴇʟᴏᴩᴇʀ : G . Sʜᴀʀᴀᴛʜ 🐥

Uᴩᴅᴀᴛᴇs : {repo_credits} 😃.

I Aᴍ Lᴀɴᴄʜ Mᴀɴʏ Oᴩᴇɴ-Sᴏᴜʀᴄᴇ Pʀᴏᴊᴇᴄᴛs Fᴏʀ Mʏ Lᴏᴠᴇʟʏ Fᴀᴍɪʟɪᴇs 😘.

Sᴜᴩᴩᴏʀᴛ Tᴀᴍɪʟᴀɴ BᴏᴛsZ 😚
"""
	HOME_TEXT = f"""
😁 Hi, [{}](tg://user?id={})\n\nTʜɪs Is **Fɪʟᴇ Sᴛᴏʀᴇ Bᴏᴛ**.

😙 Iᴀᴍ Bᴇsᴛ Fɪʟᴇ Sᴛᴏʀᴇ Bᴏᴛ Fʀᴏᴍ @Tamilan_BotsZ Tᴇᴀᴍ.!.
"""

	CODE_TEXT = f"""
Tʜɪs Rᴇᴩᴏ Is Rᴇᴀʟsᴇᴅ Bʏ : {repo_credits}
Rᴇᴩᴏ :- {repo}
"""

	FEATURESS_TEXT = f"""
Iᴀᴍ Bᴇsᴛ Fɪʟᴇ Sᴛᴏʀᴇ Bᴏᴛ Fʀᴏᴍ : {repo_credits}
Fᴇᴀᴛᴜʀᴇs :
😁 I Gɪᴠᴇ Pᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋ Oғ Yᴏᴜʀ Fɪʟᴇ
😁 Aᴜᴛᴏ Dᴇʟᴇᴛᴇ Fɪʟᴇs Dᴜᴇ Tᴏ Cᴏᴩʏʀɪɢʜᴛ 
😁 U Cᴀɴ Gᴇɴᴇʀᴀᴛᴇ Pʀᴇᴍᴀɴᴇɴᴛ Lɪɴᴋ Oғ 4ɢʙ Fɪʟᴇs 
😁 Bᴇsᴛ Uɪ 
😁 Aᴛᴛʀᴀᴄʀᴛɪᴠᴇ Eᴍᴏᴊɪs
😁 Aɴᴅ Mᴏʀᴇ Cʜᴇᴄᴋ Iɴ Rᴇᴩᴏ"""

    USE_TEXT = f"""
I Gɪᴠᴇ Yᴏᴜ Fɪʟᴇs 
Mᴀᴅᴇᴅ Bʏ {ok}"""
