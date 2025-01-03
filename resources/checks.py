from discord.ext import commands
from db import get_command_status

def is_command_enabled():
    async def predicate(ctx):
        return get_command_status(ctx.guild.id, ctx.command.name)
    return commands.check(predicate)
