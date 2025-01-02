import discord
from discord.ext import commands
from db import get_account, update_user_branch  # Import MongoDB functions

from resources.utils import create_embed

class ConfirmBranchChange(discord.ui.View):
    def __init__(self, user_id, new_branch_id, new_branch_name):
        super().__init__()
        self.user_id = user_id
        self.new_branch_id = new_branch_id
        self.new_branch_name = new_branch_name
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        success = update_user_branch(self.user_id, self.new_branch_id, self.new_branch_name)
        if success:
            embed = create_embed("Branch Changed", f"Your branch has been updated to **{self.new_branch_name}**.", discord.Color.green())
        else:
            embed = create_embed("Error", "Failed to update your branch. Please try again later.", discord.Color.red())
        await interaction.response.edit_message(embed=embed, view=None)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = create_embed("Branch Change Cancelled", "Your branch change request has been cancelled.", discord.Color.dark_grey())
        await interaction.response.edit_message(embed=embed, view=None)
        self.stop()

class HelperCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description="Change your branch to the current guild.")       
    async def change_branch(self, ctx):
        user_id = str(ctx.author.id)
        new_branch_id = str(ctx.guild.id)
        new_branch_name = ctx.guild.name

        # Check if the user has an account
        account = get_account(user_id)
        if not account:
            await ctx.respond("You don't have an account! Use `/create_account` to open one.")
            return

        # Check if the user is already in this branch
        if account['branch_name'] == new_branch_name:
            await ctx.respond(f"You are already in the **{new_branch_name}** branch.")
            return

        embed = create_embed("Confirm Branch Change", f"Are you sure you want to change your branch from **{account['branch_name']}** to **{new_branch_name}**?", discord.Color.blue())
        view = ConfirmBranchChange(user_id, new_branch_id, new_branch_name)
        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(HelperCog(bot))
