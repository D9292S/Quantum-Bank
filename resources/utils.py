import discord
import asyncio

def create_embed(title:str, description:str, color:discord.Color = discord.Color.blue()) -> discord.Embed:
    """
    Creates an embed with the given title, description and optional color.
    :param title: The title of the embed.
    :param description: The description of the embed.
    :param color: The color of the embed (default is blue).
    :return: discord.Embed object.
    """
    embed = discord.Embed(title=title,
                           description=description, 
                           color=color)
    return embed

