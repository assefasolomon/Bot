import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

BOT_TOKEN = "7787305003:AAH2iR7nV9woqIZ7XsjHstdDv73LoH8UjR8"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await send_custom_welcome(update, user.first_name)
    await delete_message(update)

# New group members
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            continue
        try:
            await context.bot.send_message(chat_id=member.id, text=build_welcome_message(member.first_name))
        except Exception as e:
            logger.error(f"Couldn't send DM to {member.id}: {e}")

# /added command
async def track_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("እባክዎ የጨምራችሁትን ጓደኛ መለያ ይጻፉ (ለምሳሌ: /added @username)")
        await delete_message(update)
        return
    friend_username = context.args[0]
    user = update.effective_user
    await update.message.reply_text(
        f"አመሰግናለሁ {user.first_name}! @{friend_username} ተመዝግቧል።\n\n"
        "የጨመርከውን ብዛት ለማየት /status ይጠቀሙ።"
    )
    await delete_message(update)

# /status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"{user.first_name} ያስገቡት የጓደኞች ብዛት:\n\n"
        "100 Add - 5000 ብር\n"
        "200 Add - 10,000 ብር\n"
        "300 Add - 15,000 ብር\n"
        "400+ Add - 20,000 ብር\n\n"
        "ለተጨማሪ መረጃ /start ይጫኑ።"
    )
    await delete_message(update)

# General messages (non-commands)
async def handle_general_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await send_custom_welcome(update, user.first_name)
    await delete_message(update)

# Send custom welcome
async def send_custom_welcome(update: Update, name: str):
    await update.message.reply_text(build_welcome_message(name))

# Delete original message
async def delete_message(update: Update):
    try:
        await update.message.delete()
    except Exception as e:
        logger.warning(f"Couldn't delete message: {e}")

# Build message
def build_welcome_message(first_name):
    return (
        f"ውድ {first_name} እንኳን ደህና መጡ።\n\n"
        "ጓደኞችህን Add በማድረግ መሸለም ይችላሉ።\n\n"
        "100 Add - ሽልማት 5000 ብር\n"
        "200 Add - ሽልማት 10,000 ብር\n"
        "300 Add - ሽልማት 15,000 ብር\n"
        "400+ Add - ሽልማት 20,000 ብር\n\n"
        "እባኮትን በቂ ጓደኛ አስገብተው https://t.me/Safricom7 አካውንቱን ይላኩ።"
    )

# Run bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("added", track_referrals))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_general_message))

    logger.info("✅ Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
