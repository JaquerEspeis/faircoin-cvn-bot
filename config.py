import logging
import os

BACKEND = 'TelegramPatched'

TELEGRAM_ID_ELOPIO = '43624396'
BOT_ADMINS = (TELEGRAM_ID_ELOPIO,)
BOT_IDENTITY = {
    'token': os.environ.get('FAIRCOIN_CVN_BOT_TELEGRAM_TOKEN'),
}
CHATROOM_PRESENCE = ()
BOT_PREFIX = '/'
CORE_PLUGINS = ()
BOT_DATA_DIR = os.environ.get('SNAP_USER_DATA')
BOT_EXTRA_PLUGIN_DIR = os.path.join(os.environ.get('SNAP'), 'plugins')
BOT_EXTRA_BACKEND_DIR = os.path.join(os.environ.get('SNAP'), 'backends')
BOT_LOG_FILE = os.path.join(BOT_DATA_DIR, 'err.log')
BOT_LOG_LEVEL = logging.DEBUG
