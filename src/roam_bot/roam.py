from pprint import pprint
import logging

import requests
import yaml
from .wormhole import check_if_system_is_wormhole

from .EVE_DATA import LIVABLE_WORMHOLES


def roam(jump_range: int):
    with open("stagings.yaml", "r") as file:
        stagings = yaml.safe_load(file)

    message = None
    connections = False
    for static in LIVABLE_WORMHOLES:
        logging.info(f"Analyzing {static}")

        for region, data in stagings.items():
            for system in data["systems"]:
                get_route_length_response = requests.get(
                    f"https://api.eve-scout.com/v2/public/routes/signatures?from={system}&system_name={static.capitalize()}&preference=shortest-gates"  # noqa: E501
                )

                get_thera_whs = requests.get(
                    "https://api.eve-scout.com/v2/public/signatures"
                )

                if get_route_length_response:
                    route_data = get_route_length_response.json()

                    for path in [x for x in route_data if x["jumps"] <= jump_range]:
                        jumps = path["jumps"]
                        system_exit = path["to"]

                        if jumps <= jump_range and not check_if_system_is_wormhole(
                            system=system_exit
                        ):
                            connections = True
                            remaining_hours = [
                                x["remaining_hours"]
                                for x in get_thera_whs.json()
                                if x["id"] == path["signature_id"]
                            ]
                            out_sig = [
                                x["out_signature"]
                                for x in get_thera_whs.json()
                                if x["id"] == path["signature_id"]
                            ]

                            link = f"https://eve-gatecheck.space/eve/#{system_exit}:{system}:shortest"
                            message = f"""
                                [{jumps} jumps to {system} from {system_exit}({out_sig[0]}) using {static}!]({link})
                                {remaining_hours[0]} hours remain...
                                region: {region}
                                notes: {data["notes"]}
                            """
                            yield message

                            logging.debug(message)

    if not connections:
        logging.debug(("No connections from target regions up!"))
        message = "No connections from target regions up! - Use Signal"
        yield message
