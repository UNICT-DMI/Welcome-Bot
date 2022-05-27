from os import getenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackContext, filters


def get_new_user_name(user: dict) -> str:
    return f"@{user['username']}" if "username" in user else user['first_name']


async def send_welcome(update: Update, ctx: CallbackContext) -> None:
    for new_member in update['message']['new_chat_members']:
        if not new_member['is_bot']:
            new_member_username = get_new_user_name(new_member)
            print(new_member['language_code'])
            # TODO: Implement array for random welcome messages

            await update.message.reply_text(f'Ciao {new_member_username} ^-^')

def main() -> None:
    token = getenv("QDBotToken")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(
        filters.ChatType.GROUPS & filters.StatusUpdate.NEW_CHAT_MEMBERS, 
        send_welcome
    ))
    app.run_polling()
    

if __name__ == '__main__':
    main()
