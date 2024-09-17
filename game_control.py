"""BrawlBot game control command (/gamectl)"""

import subprocess
from logging import info, warning
from subprocess import CompletedProcess, PIPE

import discord
from discord.app_commands import choices, Choice, command, guild_only
from discord.app_commands.checks import has_any_role

from util import reply

@command(name="gamectl", description="Allow remote management of game servers")
@guild_only
@has_any_role("Admin", "Moderator")
@choices(game=[Choice(name='TTT2', value='ttt2')],
         cmd=[Choice(name='restart', value='restart')])
async def gamectl(ctx: discord.Interaction, game: Choice[str], cmd: Choice[str]):
    """Manage game server"""
    g:str = game.value
    c:str = cmd.value

    if ctx.guild is None or not isinstance(ctx.user, discord.Member):
        await reply(ctx, "This command can only be used from a server.")
        return

    res:CompletedProcess = subprocess.run(["sudo", "systemctl", c, g], stderr=PIPE, check=False)
    if res.returncode != 0:
        warning(f'{ctx.user.name} failed to run {g} {c} with result {res.returncode}: {res.stderr}')
        await reply(ctx, f'Failed to run {g} {c}: {res.stderr}')
    info(f'{ctx.user.name} ran {g} {c}')
    await reply(ctx, f'Successfully ran {g} {c}')
