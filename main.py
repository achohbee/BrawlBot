"""BrawlBot entry point"""

import logging
from logging import handlers, error
import os
import time
import sys

from dotenv import load_dotenv

from client import BrawlBotClient


# Initialize logging
log_handler = handlers.WatchedFileHandler('../logs/brawlbot.log')
formatter = logging.Formatter(fmt='[%(levelname)s] %(asctime)s: %(message)s',
    datefmt='%b %d %H:%M:%S')
formatter.converter = time.gmtime
log_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

# Load token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    error("Cannot run without a token")
    sys.exit(-1)

# Run client
client = BrawlBotClient()
client.run(TOKEN)
