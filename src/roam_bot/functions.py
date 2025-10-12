from pprint import pprint
import logging
import re

import discord
import requests
import yaml
from discord.ext import commands

from .system_map import SYSTEM_MAP


def configure_discord_bot():
    description = "Discord Bot for Analyzing Roaming from Thera"
    discord.VoiceClient.warn_nacl = False

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    return commands.Bot(command_prefix="!", description=description, intents=intents)


def check_if_system_is_wormhole(system: str) -> bool:
    wh_regex = re.compile(r"[a-zA-Z]\d{6}")
    return bool(re.search(wh_regex, system))


def analyze_system(system_name: str):
    """System Zkill Page"""

    system_id = SYSTEM_MAP[system_name.lower()]

    get_system_kills_response = requests.get(
        f"https://zkillboard.com/api/kills/systemID/{system_id}/pastSeconds/3600/"
    )
    activity = get_system_kills_response.json()

    if activity:
        losses = len(activity[0])
        logging.debug(
            f"[There have been {losses} losses in the last hour in {system_name}!](https://zkillboard.com/system/{system_id}/)!"
        )
        return f"[There have been {losses} losses in the last hour in {system_name}!](https://zkillboard.com/system/{system_id}/)!"  # noqa: E501

    else:
        logging.debug(f"No activity in the last hour in {system_name}!")
        return f"No activity in the last hour in {system_name}!"


def analyze_thera_exits():
    with open("stagings.yml", "r") as file:
        stagings = yaml.safe_load(file)

    target_systems = list(stagings.keys())

    connections = False
    for staging_system in target_systems:
        get_route_length_response = requests.get(
            f"https://api.eve-scout.com/v2/public/routes/signatures?from={staging_system}&system_name=Thera&preference=shortest-gates"  # noqa: E501
        )
        route_data = get_route_length_response.json()
        for path in route_data:
            # pprint(path)
            if path != "error":
                jumps = path["jumps"]
                thera_exit = path["to"]
                group = stagings[staging_system]["group"]

                if jumps <= 10 and not check_if_system_is_wormhole(system=thera_exit):
                    connections = True
                    logging.debug(
                        f"{jumps} jumps from {group} in {staging_system} using {thera_exit}!"
                    )
                    link = f"https://eve-gatecheck.space/eve/#{thera_exit}:{staging_system}:shortest"
                    yield f"{jumps} jumps from {group} in {staging_system} using [{thera_exit}]({link})!"
    if not connections:
        logging.debug(("No connections from target regions up!"))
        yield "No connections from target regions up!"


def analyze_turnur_exits():
    with open("stagings.yml", "r") as file:
        stagings = yaml.safe_load(file)

    target_systems = list(stagings.keys())

    connections = False
    for staging_system in target_systems:
        get_route_length_response = requests.get(
            f"https://api.eve-scout.com/v2/public/routes/signatures?from={staging_system}&system_name=Turnur&preference=shortest-gates"  # noqa: E501
        )
        route_data = get_route_length_response.json()
        for path in route_data:
            jumps = path["jumps"]
            thera_exit = path["to"]
            group = stagings[staging_system]["group"]

            if jumps <= 10 and not check_if_system_is_wormhole(system=thera_exit):
                connections = True
                logging.debug(
                    f"{jumps} jumps from {group} in {staging_system} using {thera_exit}!"
                )
                link = f"https://eve-gatecheck.space/eve/#{thera_exit}:{staging_system}:shortest"
                yield f"{jumps} jumps from {group} in {staging_system} using [{thera_exit}]({link})!"
    if not connections:
        logging.debug(("No connections from target regions up!"))
        yield "No connections from target regions up!"


def thera_connect(system_name):
    connections = False
    get_route_length_response = requests.get(
        f"https://api.eve-scout.com/v2/public/routes/signatures?from={system_name}&system_name=Thera&preference=shortest"
    )
    route_data = get_route_length_response.json()
    for paths in route_data:
        jumps = paths["jumps"]
        thera_enterance = paths["to"]
        if paths["jumps"] <= 5 and not check_if_system_is_wormhole(
            system=thera_enterance
        ):
            connections = True
            logging.debug(f"{thera_enterance} is {jumps} from {system_name}!")

            yield f"{thera_enterance} is {jumps} from [{system_name}](https://eve-gatecheck.space/eve/#{thera_enterance}:{system_name.capitalize()}:shortest)!"  # noqa: E501

    if not connections:
        logging.debug(f"No connections within 5 jumps from {system_name}!")
        yield f"No connections within 5 jumps from {system_name}!"


def analyze_jita():
    connections = False
    get_route_length_response = requests.get(
        "https://api.eve-scout.com/v2/public/routes/signatures?from=Jita&system_name=Thera&preference=safer"
    )
    route_data = get_route_length_response.json()
    for paths in route_data:
        jumps = paths["jumps"]
        thera_enterance = paths["to"]
        if paths["jumps"] <= 8 and not check_if_system_is_wormhole(
            system=thera_enterance
        ):
            connections = True
            logging.debug(f"{thera_enterance} is {jumps} from Jita!")

            yield f"{thera_enterance} is {jumps} from [Jita](https://eve-gatecheck.space/eve/#{thera_enterance}:Jita:secure)!"  # noqa: E501

    if not connections:
        logging.debug("No connections within 8 jumps from Jita!")
        yield "No connections within 8 jumps from Jita!"
