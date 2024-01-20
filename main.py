#!./.venv/bin/python3
import logging
import os
import re

import discord
import requests
import yaml
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

api_token = os.environ["DISCORD_KEY"]
# This example requires the 'members' and 'message_content' privileged intents to function.


description = """An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)


with open("stagings.yml", "r") as file:
    stagings = yaml.safe_load(file)

target_systems = list(stagings.keys())


@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logging.info("------")


@bot.command()
async def roam(ctx):
    """Lists connnections that we can roam from"""
    connections = False
    for staging_system in target_systems:
        get_route_length_response = requests.get(
            f"https://api.eve-scout.com/v2/public/routes/signatures?from={staging_system}&system_name=Thera&preference=shortest-gates"  # noqa: E501
        )
        route_data = get_route_length_response.json()
        for path in route_data:
            jumps = path["jumps"]
            thera_exit = path["to"]
            group = stagings[staging_system]["group"]
            wh_regex = re.compile(r"[a-zA-Z]\d{6}")
            if jumps <= 10 and not bool(re.search(wh_regex, thera_exit)):
                connections = True
                logging.info(f"{jumps} jumps from {group} in {staging_system} using {thera_exit}!")
                embed = discord.Embed()
                link = f"https://eve-gatecheck.space/eve/#{thera_exit}:{staging_system}:shortest"
                embed.description = f"{jumps} jumps from {group} in {staging_system} using [{thera_exit}]({link})!"
                await ctx.send(embed=embed)
    if not connections:
        logging.info(("No connections from target regions up!"))
        await ctx.send("No connections from target regions up!")
    logging.info("!roam complete...")


@bot.command()
async def jita(ctx):
    """Closet Jita all HS"""
    connections = False
    get_route_length_response = requests.get(
        "https://api.eve-scout.com/v2/public/routes/signatures?from=Jita&system_name=Thera&preference=safer"
    )
    route_data = get_route_length_response.json()
    for paths in route_data:
        jumps = paths["jumps"]
        thera_enterance = paths["to"]
        wh_regex = re.compile(r"[a-zA-Z]\d{6}")
        if paths["jumps"] <= 8 and not bool(re.search(wh_regex, thera_enterance)):
            connections = True
            logging.info(f"{thera_enterance} is {jumps} from Jita!")
            embed = discord.Embed()
            link = f"https://eve-gatecheck.space/eve/#{thera_enterance}:Jita:secure"
            embed.description = f"{thera_enterance} is {jumps} from [Jita]({link})!"
            await ctx.send(embed=embed)

    if not connections:
        logging.info("No connections within 8 jumps from Jita!")
        await ctx.send("No connections within 8 jumps from Jita!")

    logging.info("!jita complete...")


@bot.command()
async def thera(ctx):
    """Thera Zkill Page"""

    get_system_kills_response = requests.get("https://zkillboard.com/api/kills/systemID/31000005/pastSeconds/3600/")
    activity = get_system_kills_response.json()

    if activity:
        losses = len(activity[0])
        embed = discord.Embed()
        embed.description = f"[There have been {losses} losses in the last hour in Thera!](https://zkillboard.com/system/31000005/)!"  # noqa: E501
        await ctx.send(embed=embed)
    else:
        logging.info("No activity in Thera!")
        await ctx.send("No activity in the last hour in Thera!")
    logging.info("!thera complete...")


bot.run(api_token)
