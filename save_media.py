# (c) @AbirHasan2005

from handlers.helper import os
import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.errors import FloodWait
from handlers.helpers import str_to_b64

removing_credits = REMOVING_CREDITS


async def forward_to_channel(bot: Client, message: Message, editable: Message):
    try:
        __SENT = await message.forward(Config.DB_CHANNEL)
        return __SENT
    except FloodWait as sl:
        if sl.value > 45:
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=f"#FloodWait:\n😳 Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ Oғ `{str(sl.value)}s` Fʀᴏᴍ `{str(editable.chat.id)}` !!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("😳 Bᴀɴ Usᴇʀ 😳", callback_data=f"ban_user_{str(editable.chat.id)}")]
                    ]
                )
            )
        return await forward_to_channel(bot, message, editable)


async def save_batch_media_in_channel(bot: Client, editable: Message, message_ids: list):
    try:
        message_ids_str = ""
        for message in (await bot.get_messages(chat_id=editable.chat.id, message_ids=message_ids)):
            sent_message = await forward_to_channel(bot, message, editable)
            if sent_message is None:
                continue
            message_ids_str += f"{str(sent_message.id)} "
            await asyncio.sleep(2)
        SaveMessage = await bot.send_message(
            chat_id=Config.DB_CHANNEL,
            text=message_ids_str,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("❌ Dᴇʟᴇᴛᴇ Bᴀᴛᴄʜ ❌", callback_data="closeMessage")
            ]])
        )
        share_link = f"https://telegram.me/{Config.BOT_USERNAME}?start=AbirHasan2005_{str_to_b64(str(SaveMessage.id))}"
        await editable.edit(
            f"**💖 Bᴀᴛᴄʜ Fɪʟᴇs Sᴛᴏʀᴇᴅ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ 💖!**\n\n😁 Hᴇʀᴇ Is Tʜᴇ Pᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋ Oғ Yᴏᴜʀ Fɪʟᴇ : {share_link} 😁\n\n"
            f"😊 Jᴜsᴛ Cʟɪᴄᴋ Tʜᴇ Lɪɴᴋ Tᴏ GᴇᴛFɪʟᴇ 😊!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🌚 Gᴇᴛ Mʏ Fɪʟᴇs 🌚", url=share_link)],
                 [InlineKeyboardButton("💭 Uᴩᴅᴀᴛᴇs 💭", url=f"{REMOVING_CREDITS}"),
                  InlineKeyboardButton("😵 Sᴜᴩᴩᴏʀᴛ Gʀᴏᴜᴩ 😵", url=f"{REMOVING_CREDITS_GROUP}")]]
            ),
            disable_web_page_preview=True
        )
        await bot.send_message(
            chat_id=int(Config.LOG_CHANNEL),
            text=f"#BATCH_SAVE:\n\n[{editable.reply_to_message.from_user.first_name}](tg://user?id={editable.reply_to_message.from_user.id}) GᴏᴛBᴀᴛᴄʜ Lɪɴᴋ 😌!",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Link", url=share_link)]])
        )
    except Exception as err:
        await editable.edit(f"Sᴏᴍᴇᴛʜɪɴɢ Wᴇɴᴛ Wʀᴏɴɢ 😙!\n\n**Eʀʀᴏʀ :** `{err}`")
        await bot.send_message(
            chat_id=int(Config.LOG_CHANNEL),
            text=f"#ERROR_TRACEBACK:\n😳 Gᴏᴛ Eʀʀᴏʀ Fʀᴏᴍ `{str(editable.chat.id)}` !!\n\n**TʀᴀᴄᴇBᴀᴄᴋ:** `{err}`",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("😒 Bᴀɴ Usᴇʀ 😙", callback_data=f"ban_user_{str(editable.chat.id)}")]
                ]
            )
        )


async def save_media_in_channel(bot: Client, editable: Message, message: Message):
    try:
        forwarded_msg = await message.forward(Config.DB_CHANNEL)
        file_er_id = str(forwarded_msg.id)
        await forwarded_msg.reply_text(
            f"#PRIVATE_FILE:\n\n[{message.from_user.first_name}](tg://user?id={message.from_user.id}) Gᴏᴛ Fɪʟᴇ Lɪɴᴋ 😗!",
            disable_web_page_preview=True)
        share_link = f"https://telegram.me/{Config.BOT_USERNAME}?start=AbirHasan2005_{str_to_b64(file_er_id)}"
        await editable.edit(
            "**Yᴏᴜ Fɪʟᴇ Sᴀᴠᴇᴅ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ 😻!**\n\n"
            f"Hᴇʀᴇ Is Yᴏᴜʀ Pᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋ Oғ Yᴏᴜʀ Fɪʟᴇ 😗: {share_link} \n\n"
            "Cʟɪᴄᴋ Tʜᴇ Lɪɴᴋ Aɴᴅ Gᴇᴛ Yᴏᴜʀ Fɪʟᴇs! {removing_credits}"
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🌚 Gᴇᴛ Mʏ Fɪʟᴇs 🌚", url=share_link)],
                 [InlineKeyboardButton("💭 Uᴩᴅᴀᴛᴇs 💭", url=f"{REMOVING_CREDITS}")],
                  InlineKeyboardButton("😵 Sᴜᴩᴩᴏʀᴛ Gʀᴏᴜᴩ 😵", url=f"{REMOVING_CREDITS_GROUP}"),
                  InlineKeyboardButton("﹝﹛﹙﹤` ʀᴇᴩᴏ ´﹥﹚﹜﹞", url=f"{REPO}")]]
            ),
            disable_web_page_preview=True
        )
    except FloodWait as sl:
        if sl.value > 45:
            print(f"😢 Sʟᴇᴇᴩ Oғ {sl.value}s Cᴀᴜsᴇᴅ Bʏ FʟᴏᴏᴅWᴀɪᴛ ...")
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text="#FloodWait:\n"
                     f"😳 Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ Oғ  `{str(sl.value)}s` from `{str(editable.chat.id)}` !!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("😉 Bᴀɴ Usᴇʀ 😙", callback_data=f"ban_user_{str(editable.chat.id)}")]
                    ]
                )
            )
        await save_media_in_channel(bot, editable, message)
    except Exception as err:
        await editable.edit(f"😔 SᴏᴍᴇTʜɪɴɢ Wᴇɴᴛ Wʀᴏɴɢ !\n\n**Eʀʀᴏʀ :** `{err}`")
        await bot.send_message(
            chat_id=int(Config.LOG_CHANNEL),
            text="#ERROR_TRACEBACK:\n"
                 f"😳 Gᴏᴛ Eʀʀᴏʀ Fʀᴏᴍ `{str(editable.chat.id)}` !!\n\n"
                 f"**Traceback:** `{err}`",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("😢 Bᴀɴ Usᴇʀ 😙", callback_data=f"ban_user_{str(editable.chat.id)}")]
                ]
            )
        )
