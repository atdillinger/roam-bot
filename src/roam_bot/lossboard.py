import logging

import requests

from .eve_data import GALAXY_MAP

logger = logging.getLogger(__name__)


def analyze_system(system_name: str):
    """System Zkill Page"""

    message = None

    system_id = GALAXY_MAP.get(system_name.lower(), None)
    if system_id is None:
        return "Invalid Input"

    get_system_kills_response = requests.get(
        f"https://zkillboard.com/api/kills/systemID/{system_id}/pastSeconds/3600/"
    )
    activity = get_system_kills_response.json()

    if activity:
        losses = len(activity[0])
        logger.debug(
            f"[There have been {losses} losses in the last hour in {system_name}!](https://zkillboard.com/system/{system_id}/)!"
        )
        message = f"[There have been {losses} losses in the last hour in {system_name}!](https://zkillboard.com/system/{system_id}/)!"

    else:
        logger.debug(f"No activity in the last hour in {system_name}!")
        message = f"No activity in the last hour in {system_name}!"

    return message
