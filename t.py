import os
import logging
from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from BitTorrent.Client import Client

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update):
    update.message.reply_text("Hi! Use /magnet to start downloading a magnet link.")

def download_torrent(link, bot, chat_id):
    client = Client(link)
    title = client.torrent_info.name()
    save_path = os.path.join('/path/to/save/downloaded/files', title)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    client.start_download(save_path)
    bot.send_message(chat_id=chat_id, text=f"Downloading {title}...")
    while (not client.is_seed()):
        pass
    bot.send_message(chat_id=chat_id, text=f"Download of {title} complete!")

def magnet(bot, update, args):
    if not args:
        update.message.reply_text("Please provide a magnet link.")
        return

    link = args[0]
    chat_id = update.message.chat_id
    download_torrent(link, bot, chat_id)
    update.message.reply_text(f"Download of {link} complete!")

def error(bot, update, error):
    logger.warning(f"Update {update} caused error {error}")

def main():
    token = "6022869666:AAGBLpgMLUnVrZgurGc00qZDjK6IJBgGDT4"
    bot = Bot(token)
    updater = Updater(token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("magnet", magnet, pass_args=True))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
