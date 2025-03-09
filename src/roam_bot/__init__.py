import logging
import os

import click
import discord

from .functions import (
    analyze_jita,
    analyze_thera_exits,
    anaylze_thera,
    configure_discord_bot,
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
def thera_local():
    logging.info(anaylze_thera())


@cli.command()
def jita_local():
    for message in analyze_jita():
        logging.info(message)


@cli.command()
def roam_local():
    for message in analyze_thera_exits():
        logging.info(message)


# DISCORD


@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logging.info("------")


@bot.command()
async def thera(ctx):
    """Thera Zkill Page"""

    embed = discord.Embed()
    message = anaylze_thera()
    embed.description = message
    await ctx.send(embed=embed)

    logging.info("!thera complete...")


@bot.command()
async def roam(ctx):
    """Lists connnections that we can roam from"""

    embed = discord.Embed()
    messages = analyze_thera_exits()
    for message in messages:
        embed.description = message
        await ctx.send(embed=embed)

    logging.info("!roam complete...")


@bot.command()
async def jita(ctx):
    """Closet Jita all HS"""

    embed = discord.Embed()
    messages = analyze_jita()
    for message in messages:
        embed.description = message
        await ctx.send(embed=embed)

    logging.info("!jita complete...")
