from telegram import Update, User
from telegram.ext import CallbackContext
from module.shared import welcome
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

    wlc_mess_list = welcome[lan_code]

    return wlc_mess_list[randrange(0, len(wlc_mess_list))].replace("USER", new_member_username)


def send_welcome(update: Update, _: CallbackContext) -> None:
    if update.message.new_chat_members:
        for new_member in update.message.new_chat_members:
            if not new_member.is_bot:
                handle_welcome(update, new_member)


def handle_welcome(update: Update, new_member: User) -> None:
        welcome_msg = f'{generate_welcome(new_member)}\n' + \
                      f"- Dai un'occhiata al [README]({welcome['readme']})\n" + \
                      f"- {welcome['utils'][randrange(0, len(welcome['utils']))]}"
        update.message.reply_markdown(welcome_msg, disable_web_page_preview=True)
