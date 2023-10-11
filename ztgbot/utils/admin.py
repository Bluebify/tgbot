import log
from config import SUDO

from pyrogram import filters, Client

def is_admin(bot: Client, chat_id: int, user_id: int):

    if user_id in SUDO:
        return True
    
    try:
        chat_member = bot.get_chat_member(chat_id, user_id)
        
        if chat_member.status == "administrator" or chat_member.status == "creator":
            bot.send_message(chat_id, response_message)
            response_message = "You are an admin!"
            return True
        else:
            response_message = "You are not an admin."
            bot.send_message(chat_id, response_message)
            return False

    except Exception as e:
        response_message = f"Error: {str(e)}"
        bot.send_message(chat_id, response_message)
        return False