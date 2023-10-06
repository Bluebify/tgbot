import log

from pyrogram import filters

from base import bot
from db import mongo_client

from utils.admin import is_admin

@bot.on_message(filters.command("mute"))
def mute(bot, message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    if not is_admin(bot, chat_id, user_id):
        message.reply_text("You have to be an admin to mute someone")
        return False
    
    if not is_admin(bot, chat_id, bot.id):
        message.reply_text("If I am not an admin, how can I mute someone else")
        return False

    if len(message.command) < 2:
        message.reply_text("Please provide a username to mute")
        return False

    username = message.command[1]
    entities = message.entities

    if username == str(bot.username).replace("@", ""):
        message.reply_text("I will NOT mute my self!")
        return False

    try:

        for entity in entities:
            if entity.type == "mention" or entity.type == "text_mention":
                mention_text = message.text[entity.offset : entity.offset + entity.length]
                if mention_text[1:] == username:
                    user = entity.user

                    permissions = {
                        "send_messages": False,
                        "send_media": False,
                        "send_stickers": False,
                    }

                    bot.restrict_chat_member(chat_id, user.id, permissions)

                    message.reply_text(f"@{username} has been muted!")
                    return
                
    except Exception as e:
        message.reply_text("For some reason, I just can't mute this user")
        log.log("ERROR", f"Error {e} occured while muting")

        return False

    message.reply_text(f"@{username} not found in the message")

@bot.on_message(filters.command("unmute"))
def unmute(bot, message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    if len(message.command) < 2:
        message.reply_text("Please provide a username to unmute")
        return False
    
    if not is_admin(bot, chat_id, user_id):
        message.reply_text("You have to be an admin to unmute someone")
        return False
    
    if not is_admin(bot, chat_id, bot.id):
        message.reply_text("If I am not an admin, how can I unmute someone else")
        return False

    if len(message.command) < 2:
        message.reply_text("Please provide a username to unmute")
        return False

    username = message.command[1]
    entities = message.entities

    try:
        for entity in entities:
            if entity.type == "mention" or entity.type == "text_mention":
                mention_text = message.text[entity.offset : entity.offset + entity.length]
                if mention_text[1:] == username:
                    user = entity.user

                    chat_member = bot.get_chat_member(chat_id, user.id)
                    if not chat_member.permissions.can_send_messages:

                        permissions = {
                        "send_messages": True,
                        "send_media": True,
                        "send_stickers": True,
                        }

                        bot.restrict_chat_member(chat_id, user.id, permissions)

                        message.reply_text(f"Ok, @{username} can speak now")
                        return
                
                    else:

                        message.reply_text(f"@{username} can already speak")

    except Exception as e:
        message.reply_text("For some reason, I just can't unmute this user")
        log.log("ERROR", f"Error {e} occured while unmuting")

        return False


    message.reply_text(f"@{username} not found in the message.")

__mod_name__ = "Bans"

__help__ = """
**Bans**

With this feature, you can keep annoying members in check, muting them, kicking them out, or even banning them(forever-if you wish)

**Commands**
- /mute `< username >` : mute member with their `< username >`
- /unmute`< username >`: unmutes member with their `< username >`
"""