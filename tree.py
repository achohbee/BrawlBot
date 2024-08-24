"""BrawlBot command tree"""

import discord
from gamerole import GameRole

from discord import app_commands

from util import error, exception, get_user, get_command, reply

class BrawlBotCommandTree(app_commands.CommandTree):
    def __init__(self, client):
        super().__init__(client)
        self.add_command(GameRole())

    async def on_error(self, ctx: discord.Interaction, err: app_commands.AppCommandError):
        """Error handler for app commands"""
        if isinstance(err, app_commands.MissingPermissions):
            await reply(ctx, "You do not have sufficient permissions to do that!")
            info(f'{get_user(ctx)} was not allowed to run {get_command(ctx)} with {ctx.data}')
            return

        error(f'Unexpected error when {get_user(ctx)} tried to run {get_command(ctx)} with {ctx.data}')
        exception(err)
        await reply(ctx, "Unexpected error. Please let an admin know.")
