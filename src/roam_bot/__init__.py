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
