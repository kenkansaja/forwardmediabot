from functools import wraps
from forwardscoverbot.config import config

from telegram.ext.dispatcher import run_async


def sep(num, none_is_zero=False):
    if num is None:
        return 0 if none_is_zero is True else None
    return "{:,}".format(num)



def invalid_command(update, context):
    text = "This command is invalid"
    update.message.reply_text(text=text, quote=True)


def only_admin(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        if update.message.from_user.id not in config.ADMINS:
            invalid_command(update, context, *args, **kwargs)
            return
        return func(update, context, *args, **kwargs)
    return wrapped

