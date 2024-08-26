"""BrawlBot client"""

import discord

from dynamicchannel import DynamicChannel
from gamerole import GameRole
from tree import BrawlBotCommandTree
from util import info

class BrawlBotClient(discord.Client):
    """BrawlBotClient is an implementation of Client for BrawlBot interactions"""

    def __init__(self):
        super().__init__(intents=discord.Intents.default())

        self.tree = BrawlBotCommandTree(self)
        self.dc = DynamicChannel(self)
        self.gr = GameRole()

        self.tree.add_command(self.gr)
        self.tree.add_command(self.dc.generate_command())


    async def on_ready(self):
        """Register comamnds"""
        info("Registering command tree")
        await self.tree.sync()
        info("Initializing Dynamic Channel check loop")
        self.dc.check_channels.start()
        info("Ready to handle requests")
