import os, random, time, sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Bot import TRIGGERS as trg, OWNER_ID

@Client.on_message(filters.user(OWNER_ID) & filters.command('restart', prefixes=trg))
async def restart_bot(client: Client, message: Message):  
    msg = await message.reply("Restarting", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Dev', url='https://t.me/sohailkhan_indianime')]]))
    os.execl(sys.executable, sys.executable, "-m", "Bot")  

@Client.on_message(filters.command("uptype"))
async def upload_type(client, message):
    user_id = message.from_user.id

    # Fetch user metadata from the database
    current = await db.get_metadata(user_id)
    # Display the current metadata
    text = f"""
㊋ __Your current upload type is__: `{current}`**

**__Available upload types!__**: `Video` & `Document`
    """

    # Inline buttons
    buttons = [
            [
                InlineKeyboardButton(f"Document 📁{' ✓' if current == 'document' else ''}", callback_data='set_document'),
                InlineKeyboardButton(f"Video 🎥{' ✓' if current == 'media' else ''}", callback_data='set_media')
            ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await message.reply_text(text=text, reply_markup=keyboard, disable_web_page_preview=True)


@Client.on_callback_query(filters.regex(r"set_document|set_media"))
async def uptype_callback(client, query: CallbackQuery):
    user_id = query.from_user.id
    data = query.data

    # Handle On/Off metadata toggle
    if data in ["on_metadata", "off_metadata"]:
        await db.set_metadata(user_id, "document" if data == "on_metadata" else "Off")
        # Refresh metadata display
        current = await db.(user_id)

        text = f"""
**㊋ __Your current upload type is__: `{current}`**

**__Available upload types!__**: `Video` & `Document`
        """
        buttons = [
            [
                InlineKeyboardButton(f"Document 📁{' ✓' if current == 'document' else ''}", callback_data='set_document'),
                InlineKeyboardButton(f"Video 🎥{' ✓' if current == 'media' else ''}", callback_data='set_media')
            ],
        ]
        await query.message.edit_text(text=text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
        return
