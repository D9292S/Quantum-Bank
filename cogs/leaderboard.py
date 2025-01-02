import discord
from discord.ext import commands
from db import get_leaderboard  # Import MongoDB functions

class LeaderboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="View the leaderboard for your branch.")
    async def leaderboard(self, ctx):
        """Displays the top users based on their balance in the Your branch."""
        branch_name = ctx.guild.name  # Get the guild name as the branch name
        top_users = get_leaderboard(branch_name)

        if not top_users:
            await ctx.respond(f"No accounts found in the **'{branch_name}'** branch.")
            return

        embed = discord.Embed(
            title=f"🏆 Leaderboard for {branch_name} Branch",
            description="Top users based on their balance:",
            color=discord.Color.gold()
        )

        for idx, user in enumerate(top_users, start=1):
            embed.add_field(
                name=f"{idx}. {user['username']}",
                value=f"Balance: ${user.get('balance', 0):,.2f}",
                inline=False
            )

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(LeaderboardCog(bot))
