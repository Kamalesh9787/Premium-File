# Coded By @Tamilan_BotsZ 😍 Support 🔥

from handlers.helpers import os
import time
import random
from pyrogram import Client, filters
import os
import asyncio
import traceback
from binascii import (
    Error
)
from pyrogram import (
    Client,
    enums,
    filters
)
from pyrogram.errors import (
    UserNotParticipant,
    FloodWait,
    QueryIdInvalid
)
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message
)
from configs import Config
from handlers.database import db
from handlers.add_user_to_db import add_user_to_database
from handlers.send_file import send_media_and_reply
from handlers.helpers import b64_to_str, str_to_b64
from handlers.check_user_status import handle_user_status
from handlers.force_sub_handler import (
    handle_force_sub,
    get_invite_link
)
from handlers.broadcast_handlers import main_broadcast_handler
from handlers.save_media import (
    save_media_in_channel,
    save_batch_media_in_channel
)

MediaList = {}

Bot = Client(
    name=Config.BOT_USERNAME,
    in_memory=True,
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)


@Bot.on_message(filters.private)
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)


@Bot.on_message(filters.command("start") & filters.private)
async def start(bot: Client, cmd: Message):

    if cmd.from_user.id in Config.BANNED_USERS:
        await cmd.reply_text("Sᴏʀʀʏ Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ ﹗⋅⋅⋅⋅")
        return
    if Config.UPDATES_CHANNEL is not None:
        back = await handle_force_sub(bot, cmd)
        if back == 400:
            return
    
    usr_cmd = cmd.text.split("_", 1)[-1]
    if usr_cmd == "/start":
        await add_user_to_database(bot, cmd)
        await cmd.reply_text(
            Config.HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💖 Uᴩᴅᴀᴛᴇs 💖", url="https://t.me/Tamilan_BotsZ")
                    ],
                    [
                        InlineKeyboardButton("😗 Sᴜᴩᴩᴏʀᴛ 😗", url="https://t.me/TamilanBotsZ_Support")
                    ],
                    [
                        InlineKeyboardButton("💖 Aʙᴏᴜᴛ Aɴᴅ Iɴғᴏ 💖", callback_data="use") 
                    ],
                    ]
                        InlineKeyboardButton("😇 Rᴇᴩᴏ 😇", callback_data="code"),
                        InlineKeyboardButton("🐥 Dᴇᴠᴇʟᴏᴩᴇʀ 🐥", callback_data="aboutdevs")
                    ]
                ]
            )
        )
    else:
        try:
            try:
                file_id = int(b64_to_str(usr_cmd).split("_")[-1])
            except (Error, UnicodeDecodeError):
                file_id = int(usr_cmd.split("_")[-1])
            GetMessage = await bot.get_messages(chat_id=Config.DB_CHANNEL, message_ids=file_id)
            message_ids = []
            if GetMessage.text:
                message_ids = GetMessage.text.split(" ")
                _response_msg = await cmd.reply_text(
                    text=f"**👏 Tᴏᴛᴀʟ Fɪʟᴇs :** `{len(message_ids)}`",
                    quote=True,
                    disable_web_page_preview=True
                )
            else:
                message_ids.append(int(GetMessage.id))
            for i in range(len(message_ids)):
                await send_media_and_reply(bot, user_id=cmd.from_user.id, file_id=int(message_ids[i]))
        except Exception as err:
            await cmd.reply_text(f"😔 Sᴏᴍᴇᴛʜɪɴɢ Wᴇɴᴛ Wʀᴏɴɢ !\n\n**❌:** `{err}`")


@Bot.on_message((filters.document | filters.video | filters.audio) & ~filters.chat(Config.DB_CHANNEL))
async def main(bot: Client, message: Message):

    if message.chat.type == enums.ChatType.PRIVATE:

        await add_user_to_database(bot, message)

        if Config.UPDATES_CHANNEL is not None:
            back = await handle_force_sub(bot, message)
            if back == 400:
                return

        if message.from_user.id in Config.BANNED_USERS:
            await message.reply_text("😵 Sᴏʀʀʏ Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ !\n\nCᴏɴᴛᴀᴄᴛ [Sᴜᴩᴩᴏʀᴛ Gʀᴏᴜᴩ](https://t.me/TamilanBotsZ_Support)",
                                     disable_web_page_preview=True)
            return

        if Config.OTHER_USERS_CAN_SAVE_FILE is False:
            return

        await message.reply_text(
            text="**Choose an option from below:**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📦 Sᴀᴠᴇ Iɴ Bᴀᴛᴄʜ 📂", callback_data="addToBatchTrue")],
                [InlineKeyboardButton("📎 Gᴇᴛ Lɪɴᴋ 💭", callback_data="addToBatchFalse")]
            ]),
            quote=True,
            disable_web_page_preview=True
        )
    elif message.chat.type == enums.ChatType.CHANNEL:
        if (message.chat.id == int(Config.LOG_CHANNEL)) or (message.chat.id == int(Config.UPDATES_CHANNEL)) or message.forward_from_chat or message.forward_from:
            return
        elif int(message.chat.id) in Config.BANNED_CHAT_IDS:
            await bot.leave_chat(message.chat.id)
            return
        else:
            pass

        try:
            forwarded_msg = await message.forward(Config.DB_CHANNEL)
            file_er_id = str(forwarded_msg.id)
            share_link = f"https://telegram.me/{Config.BOT_USERNAME}?start=AbirHasan2005_{str_to_b64(file_er_id)}"
            CH_edit = await bot.edit_message_reply_markup(message.chat.id, message.id,
                                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                                                              "Get Sharable Link", url=share_link)]]))
            if message.chat.username:
                await forwarded_msg.reply_text(
                    f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/{message.chat.username}/{CH_edit.id}) Channel's Broadcasted File's Button Added!")
            else:
                private_ch = str(message.chat.id)[4:]
                await forwarded_msg.reply_text(
                    f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/c/{private_ch}/{CH_edit.id}) Channel's Broadcasted File's Button Added!")
        except FloodWait as sl:
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=f"#FloodWait:\nGot FloodWait of `{str(sl.value)}s` from `{str(message.chat.id)}` !!",
                disable_web_page_preview=True
            )
        except Exception as err:
            await bot.leave_chat(message.chat.id)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=f"#ERROR_TRACEBACK:\nGot Error from `{str(message.chat.id)}` !!\n\n**Traceback:** `{err}`",
                disable_web_page_preview=True
            )


@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(Config.BOT_OWNER) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db)


@Bot.on_message(filters.private & filters.command("status") & filters.user(Config.BOT_OWNER))
async def sts(_, m: Message):
    total_users = await db.total_users_count()
    await m.reply_text(
        text=f"**Total Users in DB:** `{total_users}`",
        quote=True
    )


@Bot.on_message(filters.private & filters.command("ban_user") & filters.user(Config.BOT_OWNER))
async def ban(c: Client, m: Message):
    
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban any user from the bot.\n\n"
            f"Usage:\n\n"
            f"`/ban_user user_id ban_duration ban_reason`\n\n"
            f"Eg: `/ban_user 1234567 28 Yᴏᴜ Mɪsᴜssᴇᴅ Mᴇ`\n"
            f"This will ban user with id `1234567` for `28` Dᴀʏs Fᴏʀ Rᴇᴀsᴏɴ `Yᴏᴜ Mɪssᴜsᴇᴅ Mᴇ`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."
        try:
            await c.send_message(
                user_id,
                f"You are banned to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n"
                f"**Message from the admin**"
            )
            ban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"

        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ ! Tʀᴀᴄᴇ Bᴀᴄᴋ Gɪᴠᴇɴ Bᴇʟᴏᴡ 💬\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Bot.on_message(filters.private & filters.command("unban_user") & filters.user(Config.BOT_OWNER))
async def unban(c: Client, m: Message):

    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban any user.\n\n"
            f"Usage:\n\n`/unban_user user_id`\n\n"
            f"Eg: `/unban_user 1234567`\n"
            f"This will unban user with id `1234567`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Uɴʙᴀɴɴɪɴɢ Usᴇʀ {user_id}"
        try:
            await c.send_message(
                user_id,
                f"Yᴏᴜʀ Bᴀɴ Wᴀs Lɪғғᴛᴇᴅ!"
            )
            unban_log_text += '\n\nUsᴇʀ Nᴏᴛɪғɪᴇᴅ Sᴜᴄᴄᴇsғᴜʟʟʏ 😁!'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\nUsᴇʀ Nᴏᴛɪғɪᴄᴀᴛɪᴏɴ Fᴀɪʟᴇᴅ 😞! \n\n`{traceback.format_exc()}`"
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(
            unban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ ! Tʀᴀᴄᴇʙᴀᴄᴋ Gɪᴠᴇɴ Bᴇʟᴏᴡ 💬\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Bot.on_message(filters.private & filters.command("banned_users") & filters.user(Config.BOT_OWNER))
async def _banned_users(_, m: Message):
    
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ''

    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"> **user_id**: `{user_id}`, **Bᴀɴ Dᴜʀᴀᴛɪᴏɴ**: `{ban_duration}`, " \
                f"**Bᴀɴɴᴇᴅ Oɴ**: `{banned_on}`, **Rᴇᴀsᴏɴ**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s): `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)


@Bot.on_message(filters.private & filters.command("clear_batch"))
async def clear_user_batch(bot: Client, m: Message):
    MediaList[f"{str(m.from_user.id)}"] = []
    await m.reply_text("Cleared your batch files successfully!")

@Bot.on_callback_query()
async def button(bot: Client, cmd: CallbackQuery):

    cb_data = cmd.data
    if "use" in cb_data:
        await cmd.message.edit(
            Config.USE_BOT_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💖 Uᴩᴅᴀᴛᴇs 💖", url="https://t.me/Tamilan_BotsZ")
                    ],
                    [
                        InlineKeyboardButton("😗 Sᴜᴩᴩᴏʀᴛ 😗", url="https://t.me/TamilanBotsZ_Support")
                    ],
                    [
                        InlineKeyboardButton("👓 Rᴇᴩᴏ 👓", url="https://Github.com/TamilanBotsZ/Premium-File-Store-Bot")                                            
                    ],
                    [
                        InlineKeyboardButton("💫 Mʏ Fᴇᴀᴛᴜʀᴇs 💫", callback_data="featuress")
                    ],
                    [
                       
                        InlineKeyboardButton("⇄ Bᴀᴄᴋ ⇄", callback_data="gotohome"),
                        InlineKeyboardButton("🐤 Dᴇᴠᴇʟᴏᴩᴇʀ 🐤", callback_data="aboutdevs")
                    ]
                ]
            )
        )
        
@Bot.on_callback_query()
async def button(bot: Client, cmd: CallbackQuery):

    cb_data = cmd.data
    if "code" in cb_data:
        await cmd.message.edit(
            Config.REPO_BOT_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💖 Uᴩᴅᴀᴛᴇs 💖", url="https://t.me/Tamilan_BotsZ")
                    ],
                    [
                        InlineKeyboardButton("😗 Sᴜᴩᴩᴏʀᴛ 😗", url="https://t.me/TamilanBotsZ_Support")
                    ],
                    [
                        InlineKeyboardButton("👓 Rᴇᴩᴏ ﹝ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ﹞ 👓",
                                             url="https://Github.com/TamilanBotsZ/Premium-File-Store-Bot")
                    ],
                    [
                        InlineKeyboardButton("⇄ Bᴀᴄᴋ ⇄", callback_data="gotohome"),
                        InlineKeyboardButton("🐤 Dᴇᴠᴇʟᴏᴩᴇʀ 🐤", callback_data="aboutdevs")
                    ]
                ]
            )
        )

@Bot.on_callback_query()
async def button(bot: Client, cmd: CallbackQuery):


    elif "aboutdevs" in cb_data:
        await cmd.message.edit(
            Config.ABOUT_DEV_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("👓 Rᴇᴩᴏ ﹝ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ﹞ 👓",
                                             url="https://Github.com/TamilanBotsZ/Premium-File-Store-Bot")
                    ],
                    [
                        InlineKeyboardButton("😶 Aʙᴏᴜᴛ Mᴇ 😶", callback_data="aboutbot"),
                        InlineKeyboardButton("⇄ Bᴀᴄᴋ ⇄", callback_data="gotohome")
                    ]
                ]
            )
        )
        
    elif "featuress" in cb_data:
        await cmd.message.edit(
            Config.FEATURESS_BOT_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("👓 Rᴇᴩᴏ ﹝ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ﹞ 👓",
                                             url="https://Github.com/TamilanBotsZ/Premium-File-Store-Bot")
                    ],
                    ]
                        InlineKeyboardButton("💖 Aʙᴏᴜᴛ Aɴᴅ Iɴғᴏ 💖", callback_data="use") 
                    ],
                    ]                        
                        InlineKeyboardButton("😶 Aʙᴏᴜᴛ Mᴇ 😶", callback_data="aboutbot"),
                        InlineKeyboardButton("⇄ Bᴀᴄᴋ ⇄", callback_data="gotohome")
                    ]
                ]
            )
        )

    elif "gotohome" in cb_data:
        await cmd.message.edit(
            Config.HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💖 Uᴩᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ 💖", url="https://t.me/Tamilan_BotsZ"),
                        InlineKeyboardButton("😗 Sᴜᴩᴩᴏʀᴛ Gʀᴏᴜᴩ 😗", url="https://t.me/TamilanBotsZ_Support")
                    ],
                    [
                        InlineKeyboardButton("💖 Aʙᴏᴜᴛ Aɴᴅ Iɴғᴏ 💖", callback_data="use")
                    ],
                    [                   
                        InlineKeyboardButton("😇 Rᴇᴩᴏ 😇", callback_data="code"),
                        InlineKeyboardButton("🐥 Dᴇᴠᴇʟᴏᴩᴇʀ 🐥", callback_data="aboutdevs")
                    ]
                ]
            )
        ﹚
        
    elif "refreshForceSub" in cb_data:
        if Config.UPDATES_CHANNEL:
            if Config.UPDATES_CHANNEL.startswith("-100"):
                channel_chat_id = int(Config.UPDATES_CHANNEL)
            else:
                channel_chat_id = Config.UPDATES_CHANNEL
            try:
                user = await bot.get_chat_member(channel_chat_id, cmd.message.chat.id)
                if user.status == "kicked":
                    await cmd.message.edit(
                        text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/TamilanBotsZ_Support).",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                invite_link = await get_invite_link(channel_chat_id)
                await cmd.message.edit(
                    text="**Fɪʀsᴛ Jᴏɪɴ Mʏ Uᴩᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ☹️, Cʟɪᴄᴋ Jᴏɪɴ Uᴏᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ Bᴜᴛᴛᴏɴ**\n\n"
                         "Aɴᴅ Cʟɪᴄᴋ Rᴇғʀᴇsʜ 😙",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Jᴏɪɴ Uᴩᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ 🤖", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton("🔄 Rᴇғʀᴇsʜ 🔄", callback_data="refreshmeh")
                            ]
                        ]
                    )
                )
                return
            except Exception:
                await cmd.message.edit(
                    text="Sᴏᴍᴇᴛʜɪɴɢ Wᴇɴᴛ Wʀᴏɴɢ 😳. Cᴏɴᴛᴀᴄᴛ Mʏ [Sᴜᴩᴩᴏʀᴛ Gʀᴏᴜᴩ](https://t.me/TamilanBotsZ_Support).",
                    disable_web_page_preview=True
                )
                return
        await cmd.message.edit(
            text=Config.HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("✌ Sᴜᴩᴩᴏʀᴛ Gʀᴏᴜᴩ ✌", url="https://t.me/TamilanBotsZ_Support"),
                        InlineKeyboardButton("💕 Uᴩᴅᴀᴛᴇs 💕", url="https://t.me/Tamilan_BotsZ")
                    ],
                    [
                        InlineKeyboardButton("😉 Aʙᴏᴜᴛ Mᴇ 😉", callback_data="aboutbot"),
                        InlineKeyboardButton("🐥 Dᴇᴠᴇʟᴏᴩᴇʀ 🐥", callback_data="aboutdevs")
                    ]
                ]
            )
        )

    elif cb_data.startswith("ban_user_"):
        user_id = cb_data.split("_", 2)[-1]
        if Config.UPDATES_CHANNEL is None:
            await cmd.answer("Sᴏᴏʀʏ 😙 !", show_alert=True)
            return
        if not int(cmd.from_user.id) == Config.BOT_OWNER:
            await cmd.answer("Yᴏᴜ Nᴏᴛ Aʟʟᴏᴡᴇᴅ Tᴏ Dᴏ Tʜᴀᴛ!", show_alert=True)
            return
        try:
            await bot.kick_chat_member(chat_id=int(Config.UPDATES_CHANNEL), user_id=int(user_id))
            await cmd.answer("Usᴇʀ Bᴀɴɴᴇᴅ Fʀᴏᴍ Uᴩᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ !", show_alert=True)
        except Exception as e:
            await cmd.answer(f"😗 Cᴀɴ-ᴛ Bᴀɴ Hɪᴍ!\n\nEʀʀᴏʀ 😔: {e}", show_alert=True)

    elif "addToBatchTrue" in cb_data:
        if MediaList.get(f"{str(cmd.from_user.id)}", None) is None:
            MediaList[f"{str(cmd.from_user.id)}"] = []
        file_id = cmd.message.reply_to_message.id
        MediaList[f"{str(cmd.from_user.id)}"].append(file_id)
        await cmd.message.edit("File Saved in Batch!\n\n"
                               "Press below button to get batch link.",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("📂 Gᴇᴛ Bᴀᴛᴄʜ Lɪɴᴋ 📂", callback_data="getBatchLink")],
                                   [InlineKeyboardButton("😞 Cʟᴏsᴇ Mᴇssᴀɢᴇ 😞", callback_data="closeMessage")]
                               ]))

    elif "addToBatchFalse" in cb_data:
        await save_media_in_channel(bot, editable=cmd.message, message=cmd.message.reply_to_message)

    elif "getBatchLink" in cb_data:
        message_ids = MediaList.get(f"{str(cmd.from_user.id)}", None)
        if message_ids is None:
            await cmd.answer("Batch List Empty!", show_alert=True)
            return
        await cmd.message.edit("Pʟᴇᴀsᴇ Wᴀɪᴛ Aɴᴅ Sᴜᴩᴩᴏʀᴛ @Tamilan_BotsZ ﹝ Yᴏᴜʀ Bᴀᴛᴄʜ Lɪɴᴋ Is Gᴇɴᴇʀᴀᴛɪɴɢ ﹞ ...")
        await save_batch_media_in_channel(bot=bot, editable=cmd.message, message_ids=message_ids)
        MediaList[f"{str(cmd.from_user.id)}"] = []

    elif "closeMessage" in cb_data:
        await cmd.message.delete(True)

    try:
        await cmd.answer()
    except QueryIdInvalid: pass


CMD = ["/", "."]

@Client.on_message(filters.command("info", CMD))
async def info(bot, message):
    text =f"""
😗 Fɪʀsᴛ Nᴀᴍᴇ : {message.from_user.first_name} 
😙 Lᴀsᴛ Nᴀᴍᴇ : {message.from_user.last_name} 
😁 Usᴇʀ Nᴀᴍᴇ : {message.from_user.username}
😵 Usᴇʀ Iᴅ : {message.from_user.id}
😆 Usᴇʀ Mᴇɴᴛɪᴏɴ : {message.from_user.mention}
😃 Cʀᴇᴅɪᴛs : {repo_credits}"""
    
    await message.reply_text(text=text)
    
@Client.on_message(filters.command("credits", CMD))
async def credits(bot, message):
    text = f"""
🌻 Fᴜʟʟ Cʀᴇᴅɪᴛs Tᴏ : {repo_credits}
🐥 Dᴇᴠᴇʟᴏᴩᴇʀ : @SharathItsIsme
😙 Tʜᴀɴᴋs Tᴏ Oᴜʀ Sᴜᴩᴩᴏʀᴛᴇʀ"""

    await message.reply_text(text=text)
    
    
@Client.on_message(filters.group & filters.command("id", CMD))
async def id(bot, message):
    text =f"""
    
    """
    
    await message.reply_text(text=text)
    
    
@Client.on_message(filters.command("ping", CMD))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("..😍.😝..😙..😚..😛..")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pɪɴɢ 🔥 !\n{time_taken_s:.3f} ᴍs\nSᴜᴩᴩᴏʀᴛ : {repo_credits}")
    
    
@Client.on_message(filters.command(["id", "info"]))
async def media_info(bot, m): 
    message = m
    ff = m.from_user
    md = m.reply_to_message
    if md:
       try:
          if md.photo:
              await m.reply_text(text=f"**your photo id is **\n\n`{md.photo.file_id}`") 
          if md.sticker:
              await m.reply_text(text=f"**your sticker id is **\n\n`{md.sticker.file_id}`")
          if md.video:
              await m.reply_text(text=f"**your video id is **\n\n`{md.video.file_id}`")
          if md.document:
              await m.reply_text(text=f"**your document id is **\n\n`{md.document.file_id}`")
          if md.audio:
              await m.reply_text(text=f"**your audio id is **\n\n`{md.audio.file_id}`")
          if md.text:
              await m.reply_text("**hey man please reply with ( photo, video, sticker, documents, etc...) Only media **")  
          else:
              await m.reply_text("[404] Error..🤖")                                                                                      
       except Exception as e:
          print(e)
          await m.reply_text(f"[404] Error {e}")
                                        
    if not md:
        buttons = [[
            InlineKeyboardButton("✨️ Support", url="https://t.me/BETA_SUPPORT"),
            InlineKeyboardButton("📢 Updates", url="https://t.me/Beta_BoTZ")
        ]]       
        mkn = await m.reply("please wait....")
        if ff.photo:
           user_dp = await bot.download_media(message=ff.photo.big_file_id)
           await m.reply_photo(
               photo=user_dp,
               caption=txt.INFO_TXT.format(id=ff.id, dc=ff.dc_id, n=ff.first_name, u=ff.username),
               reply_markup=InlineKeyboardMarkup(buttons),
               quote=True,
               parse_mode=enums.ParseMode.HTML,
               disable_notification=True
           )          
           os.remove(user_dp)
           await mkn.delete()
        else:  
           await m.reply_text(
               text=txt.INFO_TXT.format(id=ff.id, dc=ff.dc_id, n=ff.first_name, u=ff.username),
               reply_markup=InlineKeyboardMarkup(buttons),
               quote=True,
               parse_mode=enums.ParseMode.HTML,
               disable_notification=True
           )


Bot.run()
