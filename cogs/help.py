import discord
from discord.ext import commands

class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/Z5u4FvDJ5C"))

    @discord.ui.select(
        placeholder="Select a category",
        options=[
            discord.SelectOption(label="General", description="General commands", emoji="🌐"),
            discord.SelectOption(label="Economy", description="Economy related commands", emoji="💰"),
            discord.SelectOption(label="Fun", description="Fun and game commands", emoji="🎉"),
            discord.SelectOption(label="Moderation", description="Moderation commands", emoji="🛡️"),
        ]
    )
    async def select_callback(self, select, interaction):
        if select.values[0] == "General":
            await self.show_general_commands(interaction)
        elif select.values[0] == "Economy":
            await self.show_economy_commands(interaction)
        elif select.values[0] == "Fun":
            await self.show_fun_commands(interaction)
        elif select.values[0] == "Moderation":
            await self.show_moderation_commands(interaction)

    async def show_general_commands(self, interaction):
        embed = discord.Embed(title="General Commands", color=discord.Color.blue())
        embed.add_field(name="/help", value="Shows this help message", inline=False)
        embed.add_field(name="/ping", value="Check the bot's latency", inline=False)
        # Add more general commands here
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_economy_commands(self, interaction):
        embed = discord.Embed(title="Economy Commands", color=discord.Color.green())
        embed.add_field(name="/create_account", value="To create your bank account", inline=False)
        embed.add_field(name="/passbook", value="Check your balance", inline=False)
        embed.add_field(name="/generate_upi", value="Enable transfer in your bank account.", inline=False)
        embed.add_field(name="/upi_transfer", value="To transfer money to another user account.", inline=False)
        embed.add_field(name="/change_branch", value="To change home branch of your account.", inline=False)
        # Add more economy commands here
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_fun_commands(self, interaction):
        embed = discord.Embed(title="Fun Commands", color=discord.Color.purple())
        embed.add_field(name="/joke", value="Get a random joke", inline=False)
        embed.add_field(name="/meme", value="Get a random meme", inline=False)
        # Add more fun commands here
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def show_moderation_commands(self, interaction):
        embed = discord.Embed(title="Moderation Commands", color=discord.Color.red())
        embed.add_field(name="/kick", value="Kick a member from the server", inline=False)
        embed.add_field(name="/ban", value="Ban a member from the server", inline=False)
        # Add more moderation commands here
        await interaction.response.send_message(embed=embed, ephemeral=True)

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="help", description="Show the help menu")
    async def help(self, ctx):
        embed = discord.Embed(
            title="Bot Help Menu",
            description="Welcome to the help menu! Select a category below to see available commands.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Categories", value="• General\n• Economy\n• Fun\n• Moderation", inline=False)
        embed.set_footer(text="Use the dropdown menu to navigate through command categories.")

        view = HelpView(self.bot)
        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(HelpCog(bot))
