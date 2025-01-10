import random
import typing
from datetime import datetime

import discord
from discord.ext import commands
from discord import app_commands

from helpers.converters import FetchUserConverter, TimeDelta, strfdelta

from . import mongo

class Administration(commands.GroupCog, group_name="admin"):
    """Commands for bot administration."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="suspend", description="Suspend one or more users.")
    @app_commands.checks.has_permissions(administrator=True)
    async def suspend(self, interaction: discord.Interaction, users: commands.Greedy[FetchUserConverter], reason: str = None):
        await self.bot.mongo.db.member.update_many(
            {"_id": {"$in": [x.id for x in users]}},
            {"$set": {"suspended": True, "suspension_reason": reason}},
        )
        await self.bot.redis.hdel("db:member", *[int(x.id) for x in users])
        users_msg = ", ".join(f"**{x}**" for x in users)
        await interaction.response.send_message(f"Suspended users: {users_msg}")

    @app_commands.command(name="tempsuspend", description="Temporarily suspend one or more users.")
    @app_commands.checks.has_permissions(administrator=True)
    async def tempsuspend(self, interaction: discord.Interaction, duration: TimeDelta, users: commands.Greedy[FetchUserConverter], reason: str = None):
        await self.bot.mongo.db.member.update_many(
            {"_id": {"$in": [x.id for x in users]}},
            {"$set": {"suspended_until": datetime.utcnow() + duration, "suspension_reason": reason}},
        )
        await self.bot.redis.hdel("db:member", *[int(x.id) for x in users])
        users_msg = ", ".join(f"**{x}**" for x in users)
        await interaction.response.send_message(f"Temporarily suspended users: {users_msg} for {strfdelta(duration)}")

    @app_commands.command(name="unsuspend", description="Unsuspend one or more users.")
    @app_commands.checks.has_permissions(administrator=True)
    async def unsuspend(self, interaction: discord.Interaction, users: commands.Greedy[FetchUserConverter]):
        await self.bot.mongo.db.member.update_many(
            {"_id": {"$in": [x.id for x in users]}},
            {"$unset": {"suspended": 1, "suspended_until": 1, "suspension_reason": 1}},
        )
        await self.bot.redis.hdel("db:member", *[int(x.id) for x in users])
        users_msg = ", ".join(f"**{x}**" for x in users)
        await interaction.response.send_message(f"Unsuspended users: {users_msg}")

    @app_commands.command(name="randomspawn", description="Spawn a random Pokémon.")
    @app_commands.checks.has_permissions(administrator=True)
    async def randomspawn(self, interaction: discord.Interaction):
        await self.bot.get_cog("Spawning").spawn_pokemon(interaction.channel)
        await interaction.response.send_message("Spawned a random Pokémon.", ephemeral=True)

    @app_commands.command(name="addredeem", description="Give a redeem to a user.")
    @app_commands.checks.has_permissions(administrator=True)
    async def addredeem(self, interaction: discord.Interaction, user: FetchUserConverter, num: int = 1):
        await self.bot.mongo.update_member(user, {"$inc": {"redeems": num}})
        await interaction.response.send_message(f"Added {num} redeem(s) to {user}")

    @app_commands.command(name="addcoins", description="Add coins to a user's balance.")
    @app_commands.checks.has_permissions(administrator=True)
    async def addcoins(self, interaction: discord.Interaction, user: FetchUserConverter, amt: int):
        await self.bot.mongo.update_member(user, {"$inc": {"balance": amt}})
        await interaction.response.send_message(f"Added {amt} coin(s) to {user}'s balance")

    @app_commands.command(name="addshard", description="Add shards to a user's balance.")
    @app_commands.checks.has_permissions(administrator=True)
    async def addshard(self, interaction: discord.Interaction, user: FetchUserConverter, amt: int):
        await self.bot.mongo.update_member(user, {"$inc": {"premium_balance": amt}})
        await interaction.response.send_message(f"Added {amt} shard(s) to {user}'s balance")

    @app_commands.command(name="addvote", description="Add to a user's vote streak.")
    @app_commands.checks.has_permissions(administrator=True)
    async def addvote(self, interaction: discord.Interaction, user: FetchUserConverter, amt: int = 1):
        await self.bot.mongo.update_member(
            user,
            {
                "$set": {"last_voted": datetime.utcnow()},
                "$inc": {"vote_total": amt, "vote_streak": amt},
            },
        )
        await interaction.response.send_message(f"Added {amt} vote(s) to {user}'s streak")

    @app_commands.command(name="addbox", description="Give boxes to a user.")
    @app_commands.checks.has_permissions(administrator=True)
    async def addbox(self, interaction: discord.Interaction, user: FetchUserConverter, box_type: str, amt: int = 1):
        if box_type not in ("normal", "great", "ultra", "master"):
            return await interaction.response.send_message("Invalid box type.")

        await self.bot.mongo.update_member(
            user,
            {
                "$set": {"last_voted": datetime.utcnow()},
                "$inc": {f"gifts_{box_type}": amt},
            },
        )
        await interaction.response.send_message(f"Added {amt} {box_type} box(es) to {user}")

    @app_commands.command(name="give", description="Give a Pokémon to a user.")
    @app_commands.checks.has_permissions(administrator=True)
    async def give(self, interaction: discord.Interaction, user: FetchUserConverter, pokemon: str, shiny: bool = False):
        species = self.bot.data.species_by_name(pokemon)

        if species is None:
            return await interaction.response.send_message(f"Unknown Pokémon: {pokemon}")

        ivs = [mongo.random_iv() for i in range(6)]

        await self.bot.mongo.db.pokemon.insert_one(
            {
                "owner_id": user.id,
                "owned_by": "user",
                "species_id": species.id,
                "level": 1,
                "xp": 0,
                "nature": mongo.random_nature(),
                "iv_hp": ivs[0],
                "iv_atk": ivs[1],
                "iv_defn": ivs[2],
                "iv_satk": ivs[3],
                "iv_sdef": ivs[4],
                "iv_spd": ivs[5],
                "iv_total": sum(ivs),
                "shiny": shiny,
                "idx": await self.bot.mongo.fetch_next_idx(user),
            }
        )

        await interaction.response.send_message(f"Gave {species} to {user}")

    @app_commands.command(name="setup", description="Test setup Pokémon.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction, user: FetchUserConverter, num: int = 100):
        pokemon = []
        idx = await self.bot.mongo.fetch_next_idx(user, reserve=num)

        for i in range(num):
            spid = random.randint(1, 905)
            ivs = [mongo.random_iv() for i in range(6)]
            pokemon.append(
                {
                    "owner_id": user.id,
                    "owned_by": "user",
                    "species_id": spid,
                    "level": 80,
                    "xp": 0,
                    "nature": mongo.random_nature(),
                    "iv_hp": ivs[0],
                    "iv_atk": ivs[1],
                    "iv_defn": ivs[2],
                    "iv_satk": ivs[3],
                    "iv_sdef": ivs[4],
                    "iv_spd": ivs[5],
                    "iv_total": sum(ivs),
                    "shiny": False,
                    "idx": idx + i,
                }
            )

        await self.bot.mongo.db.pokemon.insert_many(pokemon)
        await interaction.response.send_message(f"Set up {num} Pokémon for {user}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Administration(bot))
