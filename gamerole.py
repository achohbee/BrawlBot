"""BrawlBot -- Game Role command"""

from logging import info, error, exception

from util import log_success, reply
import discord

from discord import app_commands
from discord.app_commands.checks import has_permissions
from discord.app_commands import command

def get_gr_name(game):
    """Get a game role name"""
    return f'game:{game.lower()}'

class GameRole(app_commands.Group):
    def __init__(self):
        super().__init__(name="gr", description="Manage membership in game roles", guild_only=True)

    @command(name="join", description="Join the specified game role")
    @has_permissions(read_message_history=True)
    async def gr_join(self, ctx: discord.Interaction,  game: str):
        """Join a game role"""
        rolename = get_gr_name(game)
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        if role is None:
            await reply(ctx, "No such game role!")
            return

        if role in ctx.user.roles:
            await reply(ctx, "You're already in that game role!")
            return

        await ctx.user.add_roles(role)
        await reply(ctx, f'Added you to {rolename}')
        log_success(ctx)

    @command(name="leave", description="Leave the specified game role")
    async def gr_leave(self, ctx: discord.Interaction, game: str):
        """Leave a game role"""
        rolename = get_gr_name(game)
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        if role is None:
            await reply(ctx, "No such game role!")
            return

        if not role in ctx.user.roles:
            await reply(ctx, "You're not in that game role!")
            return

        await ctx.user.remove_roles(role)
        await reply(ctx, f'Removed you from {rolename}')
        log_success(ctx)

    @command(name="list", description="List available game roles")
    async def gr_list(self, ctx: discord.Interaction):
        """List available game roles"""
        roles = sorted([r.name[5:] for r in ctx.guild.roles if r.name.startswith("game:")])
        player_roles = {r.name[5:] for r in ctx.user.roles if r.name.startswith("game:")}
        fmt_roles = [f'**{r}**' if r in player_roles else r for r in roles]
        roles_str = '\n'.join(fmt_roles)
        await reply(ctx, f'**Available roles:**\n{roles_str}')

    @command(name="create", description="Create a new game role")
    @has_permissions(manage_channels=True)
    async def gr_create(self, ctx: discord.Interaction,  game: str):
        """Create a game role"""
        rolename = get_gr_name(game)
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        if role is not None:
            await reply(ctx, "Game role already exists!")
            return

        await ctx.guild.create_role(name=rolename, mentionable=True, \
            reason=f'Created by {ctx.user.name} ({ctx.user.id})')
        await reply(ctx, f'Created new game role {rolename}')
        log_success(ctx)

    @command(name="delete", description="Remove an existing game role")
    @has_permissions(manage_channels=True)
    async def gr_delete(self, ctx: discord.Interaction,  game: str):
        """Delete a game role"""
        rolename = get_gr_name(game)
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        if role is None:
            await reply(ctx, "No such game role!")
            return

        await role.delete(reason=f'Deleted by {ctx.user.name} ({ctx.user.id})')
        await reply(ctx, f'Deleted game role {rolename}')
        log_success(ctx)
