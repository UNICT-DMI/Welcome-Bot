from os import getenv
from telegram import Update, User
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackContext, filters
from json import load
from random import randrange


def get_new_user_name(user: User) -> str:
    return f"@{user['username']}" if user['username'] is not None else user['first_name']

def generate_welcome(new_member: User) -> str:
    new_member_username = get_new_user_name(new_member)

    match new_member["language_code"]:
        case "en":
            lan_code = "en"
        case "it" | _ :
            lan_code = "it"

    with open("src/welcome.json", "r") as f:
        wlc_mess_list = load(f)[lan_code]

    return wlc_mess_list[randrange(0, len(wlc_mess_list))].replace("USER", new_member_username)


async def send_welcome(update: Update, _: CallbackContext) -> None:
    for new_member in update['message']['new_chat_members']:
        if not new_member['is_bot']:
            await update.message.reply_text(f'{generate_welcome(new_member)}')

def main() -> None:
    token = getenv("QDBotToken")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(
        filters.ChatType.GROUPS & filters.StatusUpdate.NEW_CHAT_MEMBERS, 
        send_welcome
    ))
    app.run_polling()
    

def init() -> None:
    if __name__ == '__main__':
        main()

init()
