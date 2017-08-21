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

s = Secret()
pw = s.getMoviePw()

r = requests.post("http://api.kvikmyndir.is/authenticate", data={"username": "TotiGunn", "password": pw})
result = r.json()
token = result["token"]

r2 = requests.get("http://api.kvikmyndir.is/movies", headers={"x-access-token": token})
movies = r2.json()

#print(movies)

for i in movies:
    print(i["title"])
    for j in i["showtimes"]:
        print(j["cinema"]["name"])
        for x in j["schedule"]:
            print(x["time"])
    print(" ")
    print("-------------")




