"""BrawlBot command tree implementation"""

from logging import info, error, exception

import discord
from discord import app_commands

from gamerole import GameRole
from util import get_user, get_command, reply

class BrawlBotCommandTree(app_commands.CommandTree):
    """BrawlBotCommandTree is a CommandTree that adds all BrawlBot commands"""
    def __init__(self, client):
        super().__init__(client)
        self.add_command(GameRole())

    async def on_error(self, ctx: discord.Interaction, err: app_commands.AppCommandError, /):
        """Error handler for commands in this command tree"""
        user = get_user(ctx)
        cmd = get_command(ctx)
        if isinstance(err, app_commands.MissingPermissions):
            await reply(ctx, "You do not have sufficient permissions to do that!")
            info(f'{user} was not allowed to run {cmd}. Data: {ctx.data}')
            return

        error(f'Unexpected error when {user} tried to run {cmd}. Data: {ctx.data}')
        exception(err)
        await reply(ctx, "Unexpected error. Please let an admin know.")
