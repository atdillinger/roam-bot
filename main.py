#!./.venv/bin/python3
import os
import random
import requests
import logging
import re

import discord
from discord.ext import commands
import yaml

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


with open('stagings.yml', 'r') as file:
    stagings = yaml.safe_load(file)

target_regions = list(stagings.keys())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def roam(ctx):
    """Lists connnections that we can roam from"""

    eve_scout_list_response = requests.get('https://api.eve-scout.com/v2/public/signatures')
    thera_connections = eve_scout_list_response.json()
    for system in thera_connections:
        if system["out_system_name"] == "Thera":
            if system["in_region_name"] in target_regions:
                
                region = system["in_region_name"]
                dest_staging = stagings[region]
                for key, value in stagings[region].items():
                    life = system["remaining_hours"]
                    out_sig = system["out_signature"]
                    system_name = system["in_system_name"]
                    get_route_length_response = requests.get(f'https://api.eve-scout.com/v2/public/routes?from={system_name}&to={key}&preference=shortest-gates')
                    route_data = get_route_length_response.json()
                    jumps = route_data[0]["jumps"]
                    group = value["group"]
                    await ctx.send(f"Region: {region}\nSystem: {system_name}\nOut Sig: {out_sig}\nLife remaining*: {life} hours\nDistance to {group} in {key}: {jumps}")

@bot.command()
async def jita(ctx):
    """Closet Jita all HS"""
    no_connections_close = False
    get_route_length_response = requests.get(f'https://api.eve-scout.com/v2/public/routes/signatures?from=Jita&system_name=Thera&preference=safer')
    route_data = get_route_length_response.json()
    for paths in route_data:
        jumps = paths["jumps"]
        thera_enterance = paths["to"]

        wh_regex = re.compile('[a-zA-Z]\d{6}')
        if paths["jumps"] <= 8 and not bool(re.search(wh_regex, thera_enterance)):
            await ctx.send(f"{thera_enterance} is {jumps} from Jita!")
        else:
            no_connections_close = True
    
    if no_connections_close:
        await ctx.send(f"No connections within 8 jumps from Jita!")

bot.run(api_token)
