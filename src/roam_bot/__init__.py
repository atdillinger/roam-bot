from pprint import pprint
import logging
import os

import click
import discord

from .functions import (
    analyze_jita,
    analyze_thera_exits,
    analyze_system,
    configure_discord_bot,
    analyze_turnur_exits,
    # analyze_siseide,
    thera_connect,
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
def jita_local():
    for message in analyze_jita():
        logging.info(message)


@cli.command()
def roam_local():
    for message in analyze_thera_exits():
        logging.info(message)


@cli.command()
def roam_turnur_local():
    for message in analyze_turnur_exits():
        logging.info(message)


@cli.command()
@click.argument("system_name")
@click.argument("jump_range", default=6)
def connect_local(system_name, jump_range):
    for message in thera_connect(system_name, jump_range):
        logging.info(message)


# @cli.command()
# def home_to_thera_local():
#     for message in analyze_siseide():
#         logging.info(message)


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
async def thera(ctx):
    """Lists connections that we can roam from"""

    embed = discord.Embed()
    messages = analyze_thera_exits()
    for message in messages:
        embed.description = message
        await ctx.send(embed=embed)

    logging.info("!roam_thera complete...")


@bot.command()
async def turnur(ctx):
    """Lists connections that we can roam from"""

    embed = discord.Embed()
    messages = analyze_turnur_exits()
    for message in messages:
        embed.description = message
        await ctx.send(embed=embed)

    logging.info("!roam_turnur complete...")


@bot.command()
async def jita(ctx):
    """Closet Jita all HS"""

    await ctx.send("Thera connections to Jita...")

    embed = discord.Embed()
    messages = analyze_jita()
    for message in messages:
        embed.description = message
        await ctx.send(embed=embed)

    logging.info("!jita complete...")


@bot.command()
async def connect(ctx, system_name, jump_range=6):
    """Connection to/from system to Thera"""

    await ctx.send(f"Thera connections to {system_name}...")

    embed = discord.Embed()
    messages = thera_connect(system_name, jump_range)
    for message in messages:
        embed.description = message
        await ctx.send(embed=embed)

    logging.info("!connect complete...")
