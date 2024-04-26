from json import load, dump
from typing import Dict, List


class FILE_PATH:
    user_settings = "./cogs/keep_alive_tool/users_setting.json"
    domains_status = "./cogs/keep_alive_tool/domains_status.json"


def read(file_path:str) -> Dict[str, List[str]]:
    with open(file_path, "r") as jfile:
        return load(jfile)


def write(file_path:str, data: Dict[str, List[str]]):
    with open(file_path, "w") as jfile:
        dump(data, jfile)
