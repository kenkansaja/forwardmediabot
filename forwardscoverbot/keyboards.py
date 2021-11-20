from forwardscoverbot.config import config
from forwardscoverbot import constants

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def github_link_kb():
    button0 = InlineKeyboardButton(
            text="GROUP SUPPORT", 
            url=config.GROUP)
    button1 = InlineKeyboardButton(text="CHANNEL", url=config.CHANNEL)
    buttons_list = [[button0], [button1]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def private_chat_kb():
    bot_link = "https://t.me/{}".format(constants.GET_ME.username)
    button0 = InlineKeyboardButton(text="Private chat", url=bot_link)
    buttons_list = [[button0]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard
