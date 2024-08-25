"""BrawlBot common utilities"""
from logging import info

import discord

async def reply(ctx: discord.Interaction, msg: str):
    """Reply to the user"""
    await ctx.response.send_message(content=msg, ephemeral=True)

def get_user(ctx: discord.Interaction):
    """Get the user information for an interaction"""
    if ctx.user is not None:
        return f'User {ctx.user.name} ({ctx.user.id})'

    return 'Unknown user'

def get_command(ctx: discord.Interaction):
    """Get the command run for an interaction"""
    if ctx.command is not None:
        return f'command {ctx.command.qualified_name}'

    return 'unknown command'

def log_success(ctx: discord.Interaction):
    """Log a successful command interaction"""
    info(f'{get_user(ctx)} ran {get_command(ctx)} with {ctx.data}')
