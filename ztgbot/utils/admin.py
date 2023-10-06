import log

from pyrogram import filters

def is_admin(bot, chat_id: int, user_id: int):
    
    try:
        member = bot.get_chat_member(chat_id, user_id)

        if member:
            if member.status in ['creator', 'administrator']:
                return True
        
            else:
                return False
            
    except Exception as e:

        log.log("ERROR", f"Couldn't determine admin status\nError:{e}")
        return False