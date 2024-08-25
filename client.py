"""BrawlBot client"""

import discord

from tree import BrawlBotCommandTree
from util import info

class BrawlBotClient(discord.Client):
    """BrawlBotClient is an implementation of Client for BrawlBot interactions"""

    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = BrawlBotCommandTree(self)

    async def on_ready(self):
        """Register comamnds"""
        info("Registering command tree")
        await self.tree.sync()
        info("Ready to handle requests")
