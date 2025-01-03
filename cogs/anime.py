import discord
from discord.ext import commands
import requests
import os

base_url = os.getenv("BASE_URL")  
filter_url = os.getenv("FILTER_URL")
info_url = os.getenv("INFO_URL")
headers = {
    "Content-Type": os.getenv("CONTENT_TYPE"),
    "Accept": os.getenv("ACCEPT")
}

class AnimeView(discord.ui.View):
    def __init__(self, anime_data):
        super().__init__()
        self.anime_data = anime_data
        self.add_item(discord.ui.Button(label="More Info", url=info_url + anime_data["id"]))

    @discord.ui.select(
        placeholder="Select anime information",
        options=[
            discord.SelectOption(label="Status", value="status"),
            discord.SelectOption(label="Type", value="type"),
            discord.SelectOption(label="Episodes", value="episodes"),
            discord.SelectOption(label="Rating", value="rating"),
            discord.SelectOption(label="Rank", value="rank"),
        ]
    )
    async def select_callback(self, select, interaction):
        y = self.anime_data["attributes"]
        if select.values[0] == "status":
            await interaction.response.send_message(f"Status: {y['status']}", ephemeral=True)
        elif select.values[0] == "type":
            await interaction.response.send_message(f"Type: {y['subtype']}", ephemeral=True)
        elif select.values[0] == "episodes":
            await interaction.response.send_message(f"Total Episodes: {y['episodeCount']}", ephemeral=True)
        elif select.values[0] == "rating":
            await interaction.response.send_message(f"Average Rating: {y['averageRating']}", ephemeral=True)
        elif select.values[0] == "rank":
            await interaction.response.send_message(f"Rank: {y['ratingRank']}", ephemeral=True)

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Search for anime information")
    async def anime(self, ctx, name: str):
        await ctx.defer()
        complete_url = base_url + filter_url + name
        response = requests.get(complete_url)
        x = response.json()

        if not x["data"]:
            await ctx.respond("No anime found with that name.")
            return

        anime_data = x["data"][0]
        y = anime_data["attributes"]

        embed = discord.Embed(title=y["titles"]["en_jp"], description=y["synopsis"], colour=ctx.author.colour)
        embed.set_thumbnail(url=y["posterImage"]["large"])
        embed.add_field(name="Status", value=y["status"])
        embed.add_field(name="Type", value=y["subtype"])
        embed.add_field(name="Created At", value=y["createdAt"])
        embed.add_field(name="Updated At", value=y["updatedAt"])

        view = AnimeView(anime_data)
        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Anime(bot))
