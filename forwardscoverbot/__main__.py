import logging

# files
from forwardscoverbot.config import config
from forwardscoverbot import commands
from forwardscoverbot import messages
from forwardscoverbot import utils
from forwardscoverbot import albums
from forwardscoverbot import custom_filters

from telegram.ext import (
        Updater,
        CommandHandler,
        MessageHandler,
        Filters)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# disable apscheduler logging
aps_logger = logging.getLogger('apscheduler')
aps_logger.setLevel(logging.WARNING)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    print("\nrunning...")
    # define the updater
    updater = Updater(token=config.BOT_TOKEN, use_context=True)
    
    # define the dispatcher
    dp = updater.dispatcher

    # define jobs
    j = updater.job_queue

    # messages
    dp.add_handler(MessageHandler(Filters.all, messages.before_processing), 0)
    # albums
    dp.add_handler(MessageHandler(custom_filters.album, albums.collect_album_items), 1)
    # messages
    dp.add_handler(MessageHandler(Filters.all, messages.process_message, run_async=True), 1)
    # commands
    dp.add_handler(CommandHandler(('start', 'help'), commands.help_command, run_async=True), 2)
    dp.add_handler(CommandHandler('stats', commands.stats), 2)
    dp.add_handler(CommandHandler('disablewebpagepreview', commands.disable_web_page_preview, run_async=True), 2)
    dp.add_handler(CommandHandler('removecaption', commands.remove_caption, run_async=True), 2)
    dp.add_handler(CommandHandler('removebuttons', commands.remove_buttons, run_async=True), 2)
    dp.add_handler(CommandHandler('addcaption', commands.add_caption, run_async=True), 2)
    dp.add_handler(CommandHandler('addbuttons', commands.add_buttons, run_async=True), 2)
    dp.add_handler(MessageHandler(Filters.command, utils.invalid_command, run_async=True), 2)


    # handle errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
