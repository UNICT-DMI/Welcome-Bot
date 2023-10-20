from os import getenv
from telegram.ext import MessageHandler, Updater, Filters
from module.commands.welcome import send_welcome

def main() -> None:
    TOKEN = getenv("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, send_welcome))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
