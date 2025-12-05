import logging

import requests

from .EVE_DATA import LIVABLE_WORMHOLES
from .wormhole import check_if_system_is_wormhole


def connect(system_name: str, jump_range: int):
    connections = False

    message = None

    for static in LIVABLE_WORMHOLES:
        get_route_length_response = requests.get(
            f"https://api.eve-scout.com/v2/public/routes/signatures?from={system_name}&system_name={static}&preference=shortest-kspace"
        )
        route_data = get_route_length_response.json()
        if isinstance(route_data, dict):
            message = "Invalid input"
            yield message
            return message

        for paths in route_data:
            actual_jumps = paths["jumps"]
            thera_enterance = paths["to"]

            get_thera_whs = requests.get(
                "https://api.eve-scout.com/v2/public/signatures"
            )

            remaining_hours = [
                x["remaining_hours"]
                for x in get_thera_whs.json()
                if x["id"] == path["signature_id"]
            ]

            out_sig = [
                x["out_signature"]
                for x in get_thera_whs.json()
                if x["id"] == paths["signature_id"]
            ]

            if actual_jumps <= jump_range and not check_if_system_is_wormhole(
                system=thera_enterance
            ):
                connections = True
                logging.debug(
                    f"{static}: {thera_enterance} is {actual_jumps} from {system_name}!"
                )

                link = f"https://eve-gatecheck.space/eve/#{thera_enterance}:{system_name.capitalize()}:shortest"

                message = f"""
                    [{actual_jumps} jumps to {system_name} from {thera_enterance}({out_sig[0]}) using {static}!]({link})
                    {remaining_hours[0]} hours remain...
                """

                # message = f"[{static}: {thera_enterance} ({out_sig[0]}) is {actual_jumps} from {system_name}!]({link})"  # noqa: E501
                yield message

        if not connections:
            message = (
                f"No {static} connections within {jump_range} jumps from {system_name}!"
            )
            logging.debug(message)

            yield message
