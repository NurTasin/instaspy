from os import system
from sys import argv
import json
import time


while True:
    with open("./conf.json") as handle:
        data=json.load(handle)
    options=""
    if data["update"]:
        options+=" -F "
    if data["fetch-comments"]:
        options+=" --comments "
    system("instaloader "+options+" --dirname-pattern='./data/{target}' -l "+data["login-data"]["username"]+" ".join(data["targets"]))
    time.sleep(data["delay"])
