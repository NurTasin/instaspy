from os import system
from sys import argv
import json
import time

cycle=0
while True:
    cycle+=1
    startingTime=time.time()
    with open("./conf.json") as handle:
        data=json.load(handle)
    options=""
    if data["update"]:
        options+=" -F "
    if data["fetch-comments"]:
        options+=" --comments "
    system("instaloader "+options+" --dirname-pattern=\"./data/{target}\" -l "+data["login-data"]["username"]+" "+" ".join(data["targets"]))
    endingTime=time.time()
    if data["delay"]-(endingTime-startingTime) > 0:
        print(f"Cycle {cycle} ended and waiting {data['delay']-(endingTime-startingTime)} s before starting the next cycle.")
        time.sleep(data["delay"]-(endingTime-startingTime))

