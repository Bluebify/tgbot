import time
import pyrogram

from pyrogram import filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQuery

app = pyrogram.Client("Ini", api_id=16031336,
             api_hash="d63e0b5d3947a76e6f1726d820c52082", phone_number="+2348155553688")

app.start()

for i in range(700):
    app.send_message("HeXamonbot", "/hunt")
    time.sleep(2)

app.run()