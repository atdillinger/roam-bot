import logging
import os

import click
import discord
from discord.ext import commands

from .lossboard import (
    analyze_system,
)
from .roam import roam
from .connect import connect

logging.basicConfig(level=logging.INFO)

description = "Discord Bot for Analyzing Roaming from Thera"
discord.VoiceClient.warn_nacl = False

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)


GLOBAL_JUMP_RANGE = 8


@click.group()
def cli():
    pass


@cli.command()
def start():
    # This example requires the 'members' and 'message_content' privileged intents to function.

    api_token = os.environ["DISCORD_KEY"]

    bot.run(api_token)


@cli.command()
@click.argument("system_name")
def check_local(system_name):
    logging.info(analyze_system(system_name))


@cli.command()
@click.argument("jump_range", default=GLOBAL_JUMP_RANGE)
def roam_local(jump_range):
    for message in roam(jump_range):
        logging.info(message)


@cli.command()
@click.argument("system_name")
@click.argument("jump_range", default=GLOBAL_JUMP_RANGE)
def connect_local(system_name, jump_range):
    logging.info("starting connect local...")
    for message in connect(system_name, jump_range):
        logging.info(message)
    logging.info("finished connect local...")


@bot.command(name="check")
async def check_bot(ctx, system_name):
    """System Zkill Page"""

    embed = discord.Embed()

    message = analyze_system(system_name)
    embed.description = message
    await ctx.send(embed=embed)

    logging.info(f"!check for {system_name} complete...")


@bot.command(name="roam")
async def roam_bot(
    ctx,
    jump_range=GLOBAL_JUMP_RANGE,
):
    """Lists connections that we can roam from"""

    logging.info("!roam starting...")
    embed = discord.Embed()

    await ctx.send(f"Analyzing Thera connections within {jump_range} jumps")

    messages = roam(jump_range)
    for message in messages:
        embed.description = message
        await ctx.send(embed=embed)

    await ctx.send("Finished analyzing Thera connections")

    logging.info("!roam complete...")


@bot.command(name="connect")
async def connect_bot(ctx, system_name, jump_range=GLOBAL_JUMP_RANGE):
    """Connection to/from Thera"""

    logging.info("!connect starting...")
    await ctx.send(
        f"Finding Thera connections to {system_name} within {jump_range} jumps"
    )

    embed = discord.Embed()
    messages = connect(system_name, jump_range)
    for message in messages:
        embed.description = message
        await ctx.send(embed=embed)

    await ctx.send("Finished analyzing Thera connections")
    logging.info("!connect complete...")
