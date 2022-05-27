from os import getenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackContext, filters
import json
import random


def get_new_user_name(user: dict) -> str:
    #fallback does not work properly
    return f"@{user['username']}" if user['username'] != '' else user['first_name']

def generate_welcome(new_member) -> str:

    new_member_username = get_new_user_name(new_member)

    print(new_member['language_code'])
    #print(type(new_member['language_code']))

    # TODO: refactor, more entries in welcome.json
    wlc_txt = ""
    with open("welcome.json", "r") as f:
        list = json.load(f)[new_member["language_code"] if type(new_member["language_code"]) == type("una stringa") else "en"]
        wlc_txt = list[random.randrange(0,2)].replace("USER",new_member_username)

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
