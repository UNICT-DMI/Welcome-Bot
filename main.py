from os import getenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackContext, filters
from json import load
from random import randrange


def get_new_user_name(user: dict) -> str:
    #fallback does not work properly
    return f"@{user['username']}" if user['username'] != '' else user['first_name']

def generate_welcome(new_member) -> str:
    new_member_username = get_new_user_name(new_member)
    print(new_member['language_code'])

    match new_member["language_code"]:
        case "it":
            code = "it"
        case "en" | _ :
            code = "en"

    with open("welcome.json", "r") as f:
        list = load(f)[code]

    #collapse when removing debug prints
    wlc_txt = list[randrange(0,2)].replace("USER",new_member_username)
    print(wlc_txt)
    return wlc_txt


async def send_welcome(update: Update, ctx: CallbackContext) -> None:
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
    

if __name__ == '__main__':
    main()
