from os import getenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackContext, filters

def main() -> None:
    token = getenv("QDBotToken")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(
        filters.ChatType.GROUPS & filters.StatusUpdate.NEW_CHAT_MEMBERS, 
        None
    ))
    app.run_polling()
    

if __name__ == '__main__':
    main()
