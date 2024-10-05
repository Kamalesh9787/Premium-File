# (c) Mr. Vishal & @AbirHasan2005

from handlers.helpers import os
import datetime
from configs import Config
from handlers.database import Database

db = Database(Config.DATABASE_URL, Config.BOT_USERNAME)

yoyo = REMOVING_CREDITSS

async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id
    if not await db.is_user_exist(chat_id):
        await db.add_user(chat_id)
        await bot.send_message(
            Config.LOG_CHANNEL,
            f"#{yoyo}: \n\n😚 Nᴇᴡ Usᴇʀ[{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) 😙 Sᴛᴀʀᴛᴇᴅ @{Config.BOT_USERNAME} !!"
        )

    ban_status = await db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
                datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await db.remove_ban(chat_id)
        else:
            await cmd.reply_text("Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ Bʏᴇ Bʏᴇ Bʏᴇ ﹗﹗﹗﹗﹗﹗﹗﹗﹗🥺", quote=True)
            return
    await cmd.continue_propagation()
