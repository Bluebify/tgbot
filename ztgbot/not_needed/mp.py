
import time
import pyrogram

from pyrogram import filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQuery

# Create a Pyrogram client object
app = pyrogram.Client("Yoprozee", api_id=21445386,
             api_hash="be6e17cb425d85b05a62eae722bc06ce")

app.start()

@app.on_message(filters.text)
def handle_message(client, message):

    if message.text.lower() == ".shoot":
        time.sleep(1)
        message.edit_text("▮▶")
        time.sleep(1)
        message.edit_text("▮▬->")
        time.sleep(1)
        message.edit_text("▮▬--->")
        time.sleep(1)
        message.edit_text("▮▬----->")
        time.sleep(1)
        message.edit_text("▮▬------💥")

    elif message.text.lower() == ".hunt":
        for i in range(200):
            app.send_message("HeXamonbot", "/hunt")
            time.sleep(2)


for i in range(1000):
    app.send_message("mydumpcode", "Alive")
    time.sleep(100)

# Run the bot
print("STARTED")

app.run()