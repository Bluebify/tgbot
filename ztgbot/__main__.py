import log

import os
from importlib import import_module

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from base import bot
from utils.help import ALL_MODULES, gen_help_keyboard

MOD_HELP = {}
LOADED_MODULES = []

modules = ALL_MODULES
for module_name in modules:
    imported_module = import_module("plugins." + module_name)

    if hasattr(imported_module, "__help__"):
        if hasattr(imported_module, "__mod_name__"):
            MOD_HELP[imported_module.__mod_name__] = [imported_module.__help__, imported_module.__name__]
            LOADED_MODULES.append(imported_module.__mod_name__)

        else:
            MOD_HELP[imported_module.__name__] = [imported_module.__help__, imported_module.__name__]
            LOADED_MODULES.append(imported_module.__name__)

HELP_KEYBOARD = gen_help_keyboard(sorted(LOADED_MODULES), 1)

START_TEXT = """
Hi i'm **Zuli**, your **AI** powered group assistant.

I'm new on Telegram but I promise i'll try my best.
Use the /help command to learn how to use me - more effectively.

Don't forget, to pick up my latest updates on my News Channel.
"""

HELP_TEXT = """
In general, i'm a handy group manager, handling from small private groups to large spam-liable ones.

**Basic Commands** :
- /start - Sends the start message, or restart the bot
- /help  - Sends _this_ help message
- /help `feature` - Sends the help message about the specified `feature`
- /listfeatures   - Sends a list of valid features (for the /help `feature` command)

You can also use my answer generator, just send me the question you have and i'll try my best to answer you.

My [Support Group](t.me/zulitggroup) also exists so feel free to ask questions.

These are all the features that I support:
"""

@bot.on_callback_query()
def callback_query(bot, CallbackQuery: CallbackQuery):
    query = CallbackQuery

    help_query = []
    for i in LOADED_MODULES:
        help_query.append(f"help_{i}")

    menu_button = InlineKeyboardMarkup(InlineKeyboardButton("Back", "menu"))

    if query.data in help_query:
        query(MOD_HELP[query.data.split("help_")[1]][0])
        query.edit_message_reply_markup(menu_button)

    if query.data == "menu":
        query.edit_message_text(HELP_TEXT, reply_markup=HELP_MARKUP)

START_KEYBOARD = [[
    InlineKeyboardButton("Tutorial", "_tutorial")
], [InlineKeyboardButton("Group", url="t.me/zulitggroup"), InlineKeyboardButton("News Channel", url="t.me/zulinews")]]

START_MARKUP = InlineKeyboardMarkup(START_KEYBOARD)

HELP_MARKUP = InlineKeyboardMarkup(HELP_KEYBOARD)

@bot.on_message(filters.command("start") & filters.private)
def start_command(bot, message):
    message.reply_text(START_TEXT, reply_markup=START_MARKUP)

@bot.on_message(filters.command("help"))
def help_command(bot, message):

    if len(message.command) > 2:

        feature = message.command[1]
        try:
            if feature in LOADED_MODULES:
                f = MOD_HELP[feature]          

            else:
                message.reply_text(f"Cannot find features {feature}, use /listfeatures to list valid features")
                return 

            message.reply_text(f[0])

        except ModuleNotFoundError:
            message.reply_text(f"Cannot find features {feature}, use /listfeatures to list valid features")

        return
    
    message.reply_text(HELP_TEXT, reply_markup=HELP_MARKUP)

@bot.on_message(filters.command("listfeatures"))
def listfeatures(bot, message):
    features = []

    for module in LOADED_MODULES:
        feature = f"`{module}`"
        features.append(feature)

    featurelist = ", ".join(features)
    message.reply_text(featurelist)

log.log("Bot started", "INFO")
bot.run()