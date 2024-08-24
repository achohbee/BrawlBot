
"""BrawlBot"""
import logging
import os
import time

from client import BrawlBotClient

from dotenv import load_dotenv
from logging import handlers

log_handler = handlers.WatchedFileHandler('../logs/brawlbot.log')
formatter = logging.Formatter(fmt='[%(levelname)s] %(asctime)s: %(message)s',
    datefmt='%b %d %H:%M:%S')
formatter.converter = time.gmtime
log_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

client = BrawlBotClient()

client.run(TOKEN)
