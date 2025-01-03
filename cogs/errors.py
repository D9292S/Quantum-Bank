import discord
from discord.ext import commands
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)

class GlobalErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.debug_channel_id = 823956476887302194
        self.owner_id = 600502738572279838  # Replace with your debug channel ID

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        """Handles errors globally for all slash commands."""
        # Log the error to the console
        print(f"Error occurred: {error}")

        # Format the error message
        error_message = "**An exception has occurred!**\n"
        error_message += f"**User:** {ctx.user}\n"
        error_message += f"**Command:** /{ctx.command.qualified_name}\n"
        error_message += f"**Error:** {str(error)}\n"
        error_message += "**Traceback:**\n``````"

        # Send error to debug channel
        debug_channel = self.bot.get_channel(self.debug_channel_id)

        if debug_channel:
            embed = discord.Embed(title="Bot Error", description=error_message, color=discord.Color.red())
            await debug_channel.send(embed=embed)

        # Send error to owner's DM
        owner = await self.bot.fetch_user(self.owner_id)
        if owner:
            try:
                await owner.send(error_message)
            except discord.errors.HTTPException:
                print("Failed to send error message to owner's DM.")


        # Send a user-friendly message to the user
        if isinstance(error, discord.ApplicationCommandInvokeError):
            await ctx.respond("An error occurred while processing your command. Please try again later.")
        else:
            await ctx.respond("An unexpected error occurred. Please try again later.")

        # Log the error using the logger
        logger.error(error_message)

def setup(bot):
    """
    Sets up the GlobalErrorHandler cog for the bot.

    This function is called when the cog is loaded and is responsible
    for adding the `GlobalErrorHandler` cog to the bot. The cog handles
    global error events and ensures that errors are managed gracefully
    throughout the bot's execution.

    Parameters:
        bot (discord.Bot): The bot instance to which the cog is being added.

    Returns:
        None: This function doesn't return any value; it simply adds the cog
        to the bot for it to start processing error events.
    """
    bot.add_cog(GlobalErrorHandler(bot))
