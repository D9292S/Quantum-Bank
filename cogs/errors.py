import discord
from discord.ext import commands
from traceback import format_exc
import logging

logging.basicConfig(level=logging.INFO)

class GlobalErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        """
        Handles errors globally for all slash commands.
        """
        # Log the error to the console
        print(f"Error occurred: {error}")

        # Send a user-friendly message based on the type of error
        if isinstance(error, discord.ApplicationCommandInvokeError):
            await ctx.respond("An error occurred while processing your command. Please try again later.")
            # Optionally, send the detailed traceback to your DMs or log it elsewhere
            me = await self.bot.fetch_user(600502738572279838)  # Replace with your user ID
            full_error = format_exc()
            await me.send(f"**An exception has occurred!** (User {ctx.user} used /{ctx.command.qualified_name})\n``````{full_error}``````")
        else:
            await ctx.respond("An unexpected error occurred. Please try again later.")

def setup(bot):
    bot.add_cog(GlobalErrorHandler(bot))
