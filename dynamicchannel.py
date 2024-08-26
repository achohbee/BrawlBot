"""BrawlBot dynamic channel system"""

from datetime import datetime, timedelta
from logging import error, exception
from typing import Final

import discord
from discord import CategoryChannel
from discord.app_commands import command, guild_only
from discord.app_commands.checks import has_permissions
from discord.ext import tasks

from util import log_success, reply

# Constants
MAX_CHANNELS: Final[int] = 10
CHECK_RATE: Final[timedelta] = timedelta(seconds=60)
MAX_EMPTY_TIME: Final[timedelta] = timedelta(minutes=10)
DC_CATEGORY_NAME: Final[str] = "Dynamic channels"

class DynamicChannel():
    """DynamicChannel provides a /dc command and a check channels loop"""
    def __init__(self, client: discord.Client):
        self.client = client
        self.full_refresh = False
        self.categories: dict[int, int] = {}
        self.empty_channels: dict[int, timedelta] = {}

    async def check_known_empty_channels(self):
        """Check for empty channels that can be deleted"""
        for channel_id, first in self.empty_channels.items():
            try:
                vc = await self.client.fetch_channel(channel_id)
            except discord.NotFound:
                # Someone already deleted it
                del self.empty_channels[channel_id]
                continue
            except (discord.HTTPException, discord.InvalidData) as ex:
                # Log it but just keep going; we can do a full refresh next cycle
                exception(f"Failure querying empty voice channel id {channel_id}", ex)
                del self.empty_channels[channel_id]
                self.full_refresh = True
                continue

            if len(vc.members) != 0:
                # No longer empty
                del self.empty_channels[id]
            elif (datetime.now() - first) >= MAX_EMPTY_TIME:
                del self.empty_channels[id]
                # Time to die
                try:
                    await vc.delete()
                except discord.HTTPException as ex:
                    # Log it but just keep going; we can do a full refresh next cycle
                    exception(f"Failure deleting empty voice channel {vc.name}", ex)
                    self.full_refresh = True

    async def check_new_empty_channels(self):
        """Check for any empty channels we didn't know about already"""
        for guild_id, channel_id in self.categories.items():
            guild = self.client.get_guild(guild_id)
            if guild is None:
                # Skip this one and do a full refresh next time
                self.full_refresh = True
                continue
            channel = await guild.fetch_channel(channel_id)
            if channel is None or not isinstance(channel, CategoryChannel):
                # Skip this one and do a full refresh next time
                self.full_refresh = True
                continue
            for vc in channel.voice_channels:
                if vc.id not in self.empty_channels and len(vc.members) == 0:
                    self.empty_channels[vc.id] = datetime.now()


    @tasks.loop(seconds=CHECK_RATE.total_seconds())
    async def check_channels(self):
        """Check all dynamic channels for those that need to be deleted"""
        try:
            if self.full_refresh:
                await self.init_channels()
                self.full_refresh = False

            await self.check_known_empty_channels()
            await self.check_new_empty_channels()

        except Exception as ex: # pylint: disable=broad-exception-caught
            # Log an excpetion and do a full refresh but don't actually terminate
            exception("Unexpected error during dynamic channel loop", ex)
            self.full_refresh = True

    @check_channels.before_loop
    async def init_channels(self):
        """Build the map between guilds and the dynamic channels categories"""
        self.categories = {}
        old_empty_channels = self.empty_channels
        self.empty_channels = {}
        for guild in self.client.guilds:
            for channel in await guild.fetch_channels():
                if isinstance(channel, CategoryChannel) and channel.name == DC_CATEGORY_NAME:
                    self.categories[guild.id] = channel.id
                    for vc in channel.voice_channels:
                        if len(vc.members) == 0:
                            self.empty_channels[vc.id] = old_empty_channels[vc.id] \
                                if vc.id in old_empty_channels else datetime.now()
                    break

    def generate_command(self):
        """Generator for Brawlbot /dc command"""
        @command(name="dc", description="Create a dynamic channel")
        @guild_only
        @has_permissions(read_message_history=True)
        async def dc_cmd(ctx: discord.Interaction, name: str):
            """BrawlBot dynamic channel command (/dc)"""
            if ctx.guild is None or not isinstance(ctx.user, discord.Member):
                await reply(ctx, "This command can only be used from a server.")
                return

            guild = ctx.guild

            if guild.id in self.categories:
                await reply(ctx, "This server does not support dynamic channels.")
                return

            channel_id = self.categories[ctx.guild.id]
            category = await guild.fetch_channel(channel_id)

            if category is None or not isinstance(category, discord.CategoryChannel):
                self.full_refresh = True
                error(f"Server {guild.name} ({guild.id}) lost category channel {channel_id}")
                await reply(ctx, "Something went wrong. Please wait a few minutes and try again.")
                return

            if name in category.voice_channels:
                await reply(ctx, "A dynamic channel with that name already exists!")
                return

            if len(category.voice_channels) >= MAX_CHANNELS:
                await reply(ctx, "There are too many dynamic channels already!")
                return

            vc = await category.create_voice_channel(
                name, reason=f'Created by {ctx.user.name} ({ctx.user.id})')

            if vc is None:
                # This should never happen
                await reply(ctx, "Failed to create the new channel.")
                return

            await reply(ctx, "Dynamic channel created")
            log_success(ctx)
            try:
                await ctx.user.move_to(vc)
            except: # pylint: disable=bare-except
                # If it didn't work, just ignore it
                pass
