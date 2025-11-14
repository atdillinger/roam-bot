from pprint import pprint
import logging
import os

import click
import discord

from .functions import (
    analyze_system,
    configure_discord_bot,
    connect,
    analyze_exits,
)

logging.basicConfig(level=logging.INFO)


bot = configure_discord_bot()


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
@click.argument("jump_range", default=6)
@click.argument("source_system", default="thera")
def roam_local(jump_range, source_system):
    """
    default 6 jumps from thera
    override with turnur 10
    override with thera 10
    override with 10
    """

    for message in analyze_exits(source_system, "roam", jump_range):
        logging.info(message)


@cli.command()
@click.argument("system_name")
@click.argument("jump_range", default=6)
def connect_local(system_name, jump_range):
    for message in connect(system_name, jump_range):
        logging.info(message)


# DISCORD


@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logging.info("------")


# @bot.command(name="check", aliases=["check"])
@bot.command()
async def check(ctx, system_name):
    """System Zkill Page"""

    embed = discord.Embed()
    message = analyze_system(system_name)
    embed.description = message
    await ctx.send(embed=embed)

    logging.info(f"!check for {system_name} complete...")


@bot.command()
async def roam(
    ctx,
    jump_range=6,
    system_name="thera",
):
    """Lists connections that we can roam from"""

    embed = discord.Embed()
    messages = analyze_exits(system_name, "roam", jump_range)
    for message in messages:
        embed.description = message
        await ctx.send(embed=embed)

    logging.info("!roam complete...")


@bot.command(name="connect")
async def connect_to(ctx, system_name, jump_range=6):
    """Connection to/from Thera"""

    await ctx.send(f"Thera connections to {system_name}...")

    embed = discord.Embed()
    messages = connect(system_name, jump_range)
    for message in messages:
        embed.description = message
        await ctx.send(embed=embed)

    logging.info("!connect complete...")
