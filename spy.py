from os import system
from sys import argv
import json
import time


while True:
    startingTime=time.time()
    with open("./conf.json") as handle:
        data=json.load(handle)
    options=""
    if data["update"]:
        options+=" -F "
    system("instaloader "+options+" --dirname-pattern='./data/{target}' -l "+data["login-data"]["username"]+" ".join(data["targets"]))
    options=""
    if data["fetch-comments"]:
        options+=" --no-videos --no-video-thumbnails --no-pictures --comments "
        system("instaloader "+options+" --dirname-pattern='./data/{target}' -l "+data["login-data"]["username"]+" ".join(data["targets"]))
    endingTime=time.time()
    if (endingTime-startingTime) > 0:
        time.sleep(data["delay"]-(endingTime-startingTime))

