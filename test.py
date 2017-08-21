import requests
import json
import discord
import wikipedia
import random
import praw
import time
import datetime
import asyncio
from secret import Secret

r = requests.get("http://apis.is/weather/observations/is?stations=1,422,990")

if r.status_code == 200:
    result = r.json()

    rey = result["results"][0]
    ak = result["results"][1]
    kef = result["results"][2]
    reykjavik = "``` " + rey["T"] + " °C í Reykjavík" + "```"
    akureyri = "``` " + ak["T"] + " °C á Akureyri" + "```"
    keflavik = "``` " + kef["T"] + " °C í Keflavík" + "```"

    print(reykjavik)
    print(akureyri)
    print(keflavik)





