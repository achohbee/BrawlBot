"""BrawlBot user management"""

from discord import Interaction, Member, utils
from discord.app_commands import command, guild_only
from discord.app_commands.checks import has_role

from util import log_success, reply

@command(name="vouch", description="Vouch for another member, promoting them to Regular")
@guild_only
@has_role("Regular")
async def vouch_cmd(ctx: Interaction, member: Member):
    """BrawlBot vouch command (/vouch)"""
    if ctx.guild is None or not isinstance(ctx.user, Member):
        await reply(ctx, "This command can only be used from a server.")
        return

    role = utils.get(ctx.guild.roles, name="Regular")
    if role is None:
        await reply(ctx, "This server is not configured for this command.")
        return

    if role in member.roles:
        await reply(ctx, "That user is already a Regular")
        return

    await member.add_roles(role,  reason = f"Vouched for by {ctx.user.name} ({ctx.user.id})")

    await reply(ctx, f"You have vouched for {member.name}!")
    log_success(ctx)
