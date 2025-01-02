import discord
from discord.ext import commands
import time
import platform

from discord import Option

class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="Check the bot's latency")
    async def ping(self, ctx):
        start_time = time.time()
        message = await ctx.respond("Pinging...")
        end_time = time.time()

        latency = round((end_time - start_time) * 1000, 2)
        api_latency = round(self.bot.latency * 1000, 2)

        embed = discord.Embed(title="🏓 Pong!", color=discord.Color.green())
        embed.add_field(name="Bot Latency", value=f"{latency}ms", inline=True)
        embed.add_field(name="API Latency", value=f"{api_latency}ms", inline=True)

        await message.edit_original_response(content=None, embed=embed)

    @discord.user_command(name="User Info")
    async def userinfo(ctx, user: discord.Member):
        embed = discord.Embed(title=f"User Info - {user}", color=user.color)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Nickname", value=user.nick or "None", inline=True)
        embed.add_field(name="Account Created", value=discord.utils.format_dt(user.created_at, style='F'), inline=False)
        embed.add_field(name="Joined Server", value=discord.utils.format_dt(user.joined_at, style='F'), inline=False)
        embed.add_field(name="Top Role", value=user.top_role.mention, inline=True)
        embed.add_field(name="Bot?", value="Yes" if user.bot else "No", inline=True)
        
        roles = [role.mention for role in user.roles if role != ctx.guild.default_role]
        roles_str = ", ".join(roles) if roles else "No roles"
        embed.add_field(name="Roles", value=roles_str, inline=False)

        await ctx.respond(embed=embed)

    @discord.slash_command(name="serverinfo", description="Get information about the server")
    async def serverinfo(self, ctx):
        guild = ctx.guild

        embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Created On", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Member Count", value=guild.member_count, inline=True)
        embed.add_field(name="Role Count", value=len(guild.roles), inline=True)
        embed.add_field(name="Channel Count", value=len(guild.channels), inline=True)

        await ctx.respond(embed=embed)

    @discord.slash_command(name="botinfo", description="Get information about the bot")
    async def botinfo(self, ctx):
        embed = discord.Embed(title=f"Bot Info - {self.bot.user.name}", color=discord.Color.purple())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Created On", value=self.bot.user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=len(set(self.bot.get_all_members())), inline=True)
        embed.add_field(name="Python Version", value=platform.python_version(), inline=True)
        embed.add_field(name="Pycord Version", value=discord.__version__, inline=True)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(GeneralCog(bot))
