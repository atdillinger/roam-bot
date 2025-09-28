import re


def check_if_system_is_wormhole(system: str) -> bool:
    wh_regex = re.compile(r"[a-zA-Z]\d{6}")
    return bool(re.search(wh_regex, system))
