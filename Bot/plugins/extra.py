import os, random, time, sys
from Bot import TRIGGERS as trg, OWNER_ID
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from Bot.plugins.database.mongo_db import get_uptype, set_uptype  # Import from database.py

# Configure logging (avoid reinitializing to prevent duplicate handlers)
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )

@Client.on_message(filters.user(OWNER_ID) & filters.command('restart', prefixes=trg))
async def restart_bot(client: Client, message: Message):  
    msg = await message.reply("Restarting", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Dev', url='https://t.me/The_TGguy')]]))
    os.execl(sys.executable, sys.executable, "-m", "Bot")  

@Client.on_message(filters.command("uptype"))
async def upload_type(client, message):
    user_id = message.from_user.id
    logger.info(f"User {user_id} invoked /uptype command")

    try:
        # Fetch user upload type from the database
        current = get_uptype(user_id)
        if current not in ["video", "document"]:
            logger.warning(f"Invalid uptype {current} for user {user_id}, resetting to document")
            set_uptype(user_id, "document")
            current = "document"

        # Display the current upload type
        text = f"""
㊋ __Your current upload type is__: `{current.capitalize()}`

**__Available upload types__**: `Video` & `Document`
        """
        buttons = [
            [
                InlineKeyboardButton(
                    f"Document 📁{' ✓' if current == 'document' else ''}",
                    callback_data="set_document"
                ),
                InlineKeyboardButton(
                    f"Video 🎥{' ✓' if current == 'video' else ''}",
                    callback_data="set_media"
                ),
            ],
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        await message.reply_text(text=text, reply_markup=keyboard, disable_web_page_preview=True)
        logger.info(f"Displayed upload type {current} for user {user_id}")
    except Exception as e:
        logger.error(f"Error in upload_type for user {user_id}: {e}")
        await message.reply_text("⚠️ Error fetching upload type. Please try again later.")

@Client.on_callback_query(filters.regex(r"set_document|set_media"))
async def uptype_callback(client, query: CallbackQuery):
    user_id = query.from_user.id
    data = query.data
    logger.info(f"User {user_id} triggered callback {data}")

    try:
        # Map callback data to uptype
        uptype = "video" if data == "set_media" else "document"
        set_uptype(user_id, uptype)
        logger.info(f"Set uptype to {uptype} for user {user_id}")

        # Refresh metadata display (keeping redundant call)
        current = get_uptype(user_id)

        text = f"""
㊋ __Your current upload type is__: `{current.capitalize()}`

**__Available upload types__**: `Video` & `Document`
        """
        buttons = [
            [
                InlineKeyboardButton(
                    f"Document 📁{' ✓' if current == 'document' else ''}",
                    callback_data="set_document" 
                ),
                InlineKeyboardButton(
                    f"Video 🎥{' ✓' if current == 'video' else ''}",
                    callback_data="set_media"
                ),
            ],
        ]
        await query.message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
        logger.info(f"Updated UI with uptype {current} for user {user_id}")
    except Exception as e:
        logger.error(f"Error in uptype_callback for user {user_id}: {e}")
        await query.answer(f"⚠️ Error updating upload type: {e}", show_alert=True)
