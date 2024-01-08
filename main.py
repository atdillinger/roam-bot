#!./.venv/bin/python3
import os
import random
import requests

import discord
from discord.ext import commands

from pprint import pprint

api_token = os.environ["DISCORD_KEY"]
# This example requires the 'members' and 'message_content' privileged intents to function.


description = """An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)


target_regions = [
    "Providence",
    "Catch",
    "Tenerifis",
    "Scalding Pass",
    "Querious",
    "Wicked Creek",
    "Deteroid",
    "Esoteria",
    "Etherium Reach",
    "Pure Blind",
]


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def connections(ctx):
    """Lists connnections that we can roam from"""
    thera_connections = requests.get('https://api.eve-scout.com/v2/public/signatures')
    thera_data = thera_connections.json()
    for system in thera_data:
        if system["in_region_name"] in target_regions and system["out_system_name"] == "Thera":

            region = system["in_region_name"]
            life = system["remaining_hours"]
            out_sig = system["out_signature"]
            system_name = system["in_system_name"]
            pprint(system["in_region_name"])
            pprint(system["remaining_hours"])
            pprint(system["out_signature"])
            pprint(system["in_system_name"])
            await ctx.send(f"Region: {region}")
            await ctx.send(f"System: {system_name}")
            await ctx.send(f"Out Sig: {out_sig}")
            await ctx.send(f"Life remaining*: {life}")
            await ctx.send("------")
        # await ctx.send("""We should roam...\n""")


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f"No, {ctx.subcommand_passed} is not cool")


@cool.command(name="bot")
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send("Yes, the bot is cool.")


bot.run(api_token)
