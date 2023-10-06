import log

from pyrogram import filters

from base import bot
from db import mongo_client

from utils.admin import is_admin

try:
    welcome_db = mongo_client["welcome"]["welcome_table"]
    settings_db = mongo_client["settings"]["settings_table"]

except Exception as e:
    log.log("ERROR", "Couldn't import mongodb database")

@bot.on_message(filters.command("setwelcome"))
def setwelcome(bot, message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    if is_admin(chat_id, user_id):
        try:

            if message.text.split()[1] == " " or message.text.split()[1] == "" or message.text.split()[1] == None:
                message.reply_text("The welcome message has to have a value")
                return False

            ids = []
            all_cases = welcome_db.find()
            for i in all_cases:
                ids.append(i["chat_id"])

            if chat_id not in ids:
                words = message.text.split()[1:]
                msg = " ".join(words)

                welcome_db.insert_one({
                    "type": "welcome",
                    "chat_id": chat_id,
                    "message": msg
                })

                message.reply_text("Successfully set welcome message")

            elif chat_id in ids:

                welcome_db.delete_many({
                    "type": "goodbye",
                    "chat_id": chat_id
                })

                words = message.text.split()[1:]
                msg = " ".join(words)

                welcome_db.insert_one({
                    "type": "welcome",
                    "chat_id": chat_id,
                    "message": msg
                })

                message.reply_text("Successfully changed welcome message")

        except Exception as e:
            log.log(e, "ERROR")
            return False

    elif is_admin(chat_id, user_id) == False:
        
        message.reply_text("You have to be an admin to use this command")
        return False
    
@bot.on_message(filters.command("setgoodbye"))
def setgoodbye(bot, message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    if is_admin(chat_id, user_id):
        try:

            if message.text.split()[1] == " " or message.text.split()[1] == "" or message.text.split()[1] == None:
                message.reply_text("The goodbye message has to have a value")
                return False

            ids = []
            all_cases = welcome_db.find()
            for i in all_cases:
                ids.append(i["chat_id"])

            if chat_id not in ids:
                words = message.text.split()[1:]
                msg = " ".join(words)

                welcome_db.insert_one({
                    "type": "goodbye",
                    "chat_id": chat_id,
                    "message": msg
                })

                message.reply_text("Successfully set goodbye message")

            elif chat_id in ids:

                welcome_db.delete_many({
                    "type": "goodbye",
                    "chat_id": chat_id
                })

                words = message.text.split()[1:]
                msg = " ".join(words)

                welcome_db.insert_one({
                    "type": "goodbye",
                    "chat_id": chat_id,
                    "message": msg
                })

                message.reply_text("Successfully changed goodbye message")

        except Exception as e:
            log.log(e, "ERROR")
            return False

    else:
        message.reply_text("You have to be an admin to use this command")
        return False
    
@bot.on_message(filters.command("usewelcome"))
def usewelcome(bot, message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    params = ["off", "on"]

    if is_admin(chat_id, user_id):
        try:
            if message.text.split()[1] not in params:
                message.reply_text("Command usage: /usewelcome `<on|off>`")
                return False
            
            ids = []
            all_cases = settings_db.find()
            for i in all_cases:
                ids.append(i["chat_id"])

            if chat_id in ids:
                uses_goodbye = settings_db.find_one({"chat_id": chat_id})["uses_goodbye"]
                settings_db.delete_many({
                    "chat_id": chat_id
                })

                settings_db.insert_one({
                    "chat_id": chat_id,
                    "uses_welcome": str(message.text.split()[1]),
                    "uses_goodbye": uses_goodbye
                })

            else:
                settings_db.insert_one({
                    "chat_id": chat_id,
                    "uses_welcome": str(message.text.split()[1]),
                    "uses_goodbye": "on"
                })

        except Exception as e:
            log.log(e, "ERROR")         

    else:
        message.reply_text("You have to be an admin to use this command")

@bot.on_message(filters.command("usegoodbye"))
def usegoodbye(bot, message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    params = ["off", "on"]

    if is_admin(chat_id, user_id):
        try:
            if message.text.split()[1] not in params:
                message.reply_text("Command usage: /usegoodbye `<on|off>`")
                return False
            
            ids = []
            all_cases = settings_db.find()
            for i in all_cases:
                ids.append(i["chat_id"])

            if chat_id in ids:
                uses_welcome = settings_db.find_one({"chat_id": chat_id})["uses_welcome"]
                settings_db.delete_many({
                    "chat_id": chat_id
                })

                settings_db.insert_one({
                    "chat_id": chat_id,
                    "uses_goodbye": str(message.text.split()[1]),
                    "uses_welcome": uses_welcome
                })

            else:
                settings_db.insert_one({
                    "chat_id": chat_id,
                    "uses_goodbye": str(message.text.split()[1]),
                    "uses_welcome": "on"
                })

        except Exception as e:
            log.log(e, "ERROR")         

    else:
        message.reply_text("You have to be an admin to use this command")
    
@bot.on_message(filters.new_chat_members)
def welcome(bot, message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    try:

        uses_welcome = settings_db.find_one({"chat_id": chat_id})["uses_welcome"] or ""

        if uses_welcome == "off":
            return False

        welcome_msg = welcome_db.find_one({
            "type": "welcome",
            "chat_id": chat_id
        })["message"] or ""

        if welcome_msg == "":
            #TODO:find a way to get new_member's details to improve greeting
            message.reply_text("Hello")

        else:
            message.reply_text(welcome_msg)

    except Exception as e:
        log.log(e, "ERROR")

@bot.on_message(filters.left_chat_member)
def goodbye(bot, message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    try:
        goodbye_msg = welcome_db.find_one({
            "type": "goodbye",
            "chat_id": chat_id
        })["message"] or ""

        if goodbye_msg == "":
            #TODO:find a way to get new_member's details to improve greeting
            message.reply_text("Goodbye")

        else:
            message.reply_text(goodbye_msg)

    except Exception as e:
        log.log(e, "ERROR")

__mod_name__ = "Greetings"

__help__ = """
**Greetings**

With this feature, you can soothe new members with a nice (or custom) welcome message, or honor old ones with a deserving goodbye.

**Commands:**
- /setwelcome `< welcome_message >` : Sets the custom welcome message to `< welcome_message >`
- /setgoodbye `< goodbye_message >` : Sets the custom goodbye message to `< goodbye_message >`
- /usewelcome `< on|off >` : Choose whether or not to send a welcome message
- /usegoodbye `< on|off >` : Choose whether or not to send a goodbye message
"""