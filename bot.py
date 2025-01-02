import discord
import os

intents = discord.Intents.all()

bot = discord.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f"Connected to {len(bot.guilds)} guilds")

@bot.event
async def on_message(message):
    # Avoid responding to the bot's own messages
    if message.author == bot.user:
        return

    # Log the message content
    print(f"Message from {message.author}: {message.content}")

    # You can add additional logic here if needed

cogs_list = [
    'accounts',
    'errors',
    'helpers',
    'leaderboard'
]

for cog in cogs_list:
    try:
        bot.load_extension(f'cogs.{cog}')
        print(f'Loaded cog: {cog}')
    except Exception as e:
        print(f'Failed to load cog {cog}: {e}')

bot.run(TOKEN)


