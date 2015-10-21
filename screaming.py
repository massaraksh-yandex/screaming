import logging
import telegram
from commands import load
from replier import Replier
import daemon
import os
import sys

LAST_UPDATE_ID = None

def main(key):
    global LAST_UPDATE_ID

    logging.basicConfig(filename='log/screaming.log', level=logging.WARNING,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    bot = telegram.Bot(key)

    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except Exception:
        LAST_UPDATE_ID = None

    default, other = load('config.json')
    replier = Replier(bot, default, *other)

    while True:
        for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
            LAST_UPDATE_ID = replier.reply(update)

if __name__ == '__main__':
    try:
        with daemon.DaemonContext(working_directory=os.getcwd()):
            main(sys.argv[1])
    except Exception as e:
        print (str(e))
        logging.critical(str(e))
        raise
