"""BrawlBot client"""

import discord

from dynamic_channel import DynamicChannel
from gamerole import GameRole
from game_control import gamectl
from tree import BrawlBotCommandTree
from util import info
from vouch import vouch_cmd

class BrawlBotClient(discord.Client):
    """BrawlBotClient is an implementation of Client for BrawlBot interactions"""

    def __init__(self):
        super().__init__(intents=discord.Intents.default())

        self.tree = BrawlBotCommandTree(self)
        self.dc = DynamicChannel(self)
        self.gr = GameRole()

        self.tree.add_command(self.gr)
        self.tree.add_command(self.dc.dc_cmd)
        self.tree.add_command(vouch_cmd)
        self.tree.add_command(gamectl)

    async def on_ready(self):
        """Register comamnds"""
        info("Registering command tree")
        await self.tree.sync()
        info("Initializing Dynamic Channel check loop")
        self.dc.check_channels.start()
        info("Ready to handle requests")

    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        """Add 'view channel' permission to @everyone on newly creating Gaming voice channels"""
        if isinstance(channel, discord.VoiceChannel) and channel.category is not None \
                and channel.category.name == 'Gaming':
            await channel.set_permissions(channel.guild.default_role, view_channel = True)
