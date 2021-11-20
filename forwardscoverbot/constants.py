from forwardscoverbot.config import config

from telegram import Bot

GET_ME = Bot(config.BOT_TOKEN).getMe()
