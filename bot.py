import discord
import os
from cogs.errors import logger
import sys
from resources.checks import is_command_enabled

intents = discord.Intents.all()


bot = discord.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    """
    Event handler for when the bot is ready and connected.

    This function is triggered when the bot has successfully connected to
    Discord and is ready to start receiving events and interacting with
    guilds, channels, and users. It prints information about the bot's
    successful login and the number of guilds the bot is currently connected to.

    Actions:
        - Prints the bot's username and ID when it logs in.
        - Prints the number of guilds the bot is currently connected to.

    Returns:
        None: This function does not return a value; it executes print statements
        to show the bot's connection status.
    """
    print(f'Logged in as {bot.user}')
    print(f'Connected to {len(bot.guilds)} guilds')

    channel_id = int(os.getenv('NOTIFICATION_CHANNEL_ID'))
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send('Bot has been deployed and is now online!')

    total_members = sum(guild.member_count for guild in bot.guilds)
    total_guilds = len(bot.guilds)
    await bot.change_presence(activity=discord.Game(name=f'{os.getenv("ACTIVITY")} | {total_members} Users | {total_guilds} Guilds'))
    for command in bot.application_commands:
        command.add_check(is_command_enabled())

@bot.event
async def on_error(event, *args, **kwargs):
    error = sys.exc_info()[1]
    logger.error(f"Error in {event}: {str(error)}")

@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Command error in {ctx.command}: {str(error)}")

cogs_list = [
    'accounts',
    'anime',
    'errors',
    'helpers',
    'leaderboard',
    'help',
    'general'
]


if __name__ == '__main__':
    for cog in cogs_list:
        try:
            bot.load_extension(f'cogs.{cog}')
            print(f'Loaded cog: {cog}')
        except Exception as e:
            print(f'Failed to load cog {cog}: {e}')
    bot.run(TOKEN)



