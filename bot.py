import discord
import os
from cogs.errors import logger
import sys

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.messages = True
intents.guilds = True


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

    total_members = sum(guild.member_count for guild in bot.guilds)
    total_guilds = len(bot.guilds)
    await bot.change_presence(activity=discord.Game(name=f'{os.getenv("ACTIVITY")} | {total_members} Users | {total_guilds} Guilds'))

@bot.event
async def on_error(event, *args, **kwargs):
    error = sys.exc_info()[1]
    logger.error(f"Error in {event}: {str(error)}")

@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Command error in {ctx.command}: {str(error)}")


@bot.event
async def on_message(message):
    """
    Event handler for when a message is sent in a channel.

    This function is triggered whenever a message is sent in any of the channels
    that the bot has access to. It processes incoming messages and ensures that
    the bot does not respond to its own messages.

    Actions:
        - Checks if the message was sent by the bot itself.
        - If the message is from the bot, it returns early without processing further.

    Parameters:
        message (discord.Message): The message object that was sent in the channel.

    Returns:
        None: This function does not return a value, but it may interact with the message
        (e.g., by sending a response) depending on further processing logic.
    """
    # Avoid responding to the bot's own messages
    if message.author == bot.user:
        return

    # Log the message content
    print(f"Message from {message.author}: {message.content}")

cogs_list = [
    'accounts',
    'anime',
    'errors',
    'helpers',
    'leaderboard',
    'help',
    'general'
]

for cog in cogs_list:
    try:
        bot.load_extension(f'cogs.{cog}')
        print(f'Loaded cog: {cog}')
    except Exception as e:
        print(f'Failed to load cog {cog}: {e}')

bot.run(TOKEN)


