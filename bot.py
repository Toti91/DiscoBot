from discord.ext.commands import Bot
import discord
import wikipedia
import requests
import random
import textwrap
import praw
import datetime
from secret import Secret

description = "Ég er skrifaður í Python með hjálp Discord.py"
s = Secret()
t = s.getToken()

bot = Bot(command_prefix="!", description=description)

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    await bot.change_presence(game=discord.Game(name="Bara chilla"))

@bot.command(description="Skipun sem velur random leik til að spila?")
async def veljaleik(*leikir: str):
    """Velur einn random hlut af því sem þú segir, t.d !veljaleik lol pugb rocketleague"""

    await bot.say(random.choice(leikir))

@bot.command(description="Veður fyrir næstu daga")
async def veður():
    """Veður fréttir fyrir næstu daga"""

    r = requests.get("http://apis.is/weather/texts?types=5")

    if r.status_code == 200:
        result = r.json()
        final = result["results"][0]

        # ``` prefixið í mörgum strengjum í þessu forriti er til að Discord formatti strenginn á ákveðinn hátt.
        await bot.say("```" + final["content"] + "```")
    else:
        await bot.say("Náði ekki sambandi við API")

@bot.command(description="Næstu leikir Keflavíkur")
async def keflavík():
    """Næstu leikir Keflavíkur, meistaraflokkur karla og kvenna"""

    r = requests.get("http://apis.is/sports/football")

    if r.status_code == 200:
        result = r.json()
        final = result["results"]
        final = sorted(final, key=lambda k: k['counter'])

        string = ""
        deildir = ["Inkasso-deildin", "Pepsi-deild karla", "Meistaradeild UEFA", "Borgunarbikar karla"]
        kvenna = ["1. deild kvenna", "Pepsi-deild kvenna"]

        for i in range(len(final)):
            for key, value in final[i].items():
                if value == "Keflavík":
                    if final[i]["tournament"] in deildir: # ```fix = yellow
                        string += ("```fix" + "\n" + "Deild: " + final[i]["tournament"] + "\n"
                                    + final[i]["date"] + " kl: " + final[i]["time"] + "\n" + final[i]["homeTeam"]
                                    + " - " + final[i]["awayTeam"] + "\n" + "Staðsetning: " + final[i]["location"]
                                    + "\n" + "\n" + "```")
                    elif final[i]["tournament"] in kvenna:
                        string += ("```" + "\n" + "Deild: " + final[i]["tournament"] + "\n"
                                    + final[i]["date"] + " kl: " + final[i]["time"] + "\n" + final[i]["homeTeam"]
                                    + " - " + final[i]["awayTeam"] + "\n" + "Staðsetning: " + final[i]["location"]
                                    + "\n" + "\n" + "```")

        if not string:
            await bot.say("Fann enga leiki með Keflavík á næstu dögum.")
        else:
            await bot.say(string)
    else:
        await bot.say("Náði ekki sambandi við API")

@bot.command(description="Næstu leikir tiltekins liðs")
async def fótbolti(lið: str):
    """Næstu leikir tiltekins liðs, t.d !fótbolti íbv"""

    r = requests.get("http://apis.is/sports/football")

    if r.status_code == 200:
        result = r.json()
        final = result["results"]
        final = sorted(final, key=lambda k: k['counter'])

        string = ""
        deildir = ["Inkasso-deildin", "Pepsi-deild karla", "Meistaradeild UEFA", "Borgunarbikar karla"]
        kvenna = ["1. deild kvenna", "Pepsi-deild kvenna"]

        for i in range(len(final)):
            for key, value in final[i].items():
                if str(value).lower() == lið.lower():
                    if final[i]["tournament"] in deildir:
                        string += ("```fix" + "\n" + "Deild: " + final[i]["tournament"] + "\n"
                                    + final[i]["date"] + " kl: " + final[i]["time"] + "\n" + final[i]["homeTeam"]
                                    + " - " + final[i]["awayTeam"] + "\n" + "Staðsetning: " + final[i]["location"]
                                    + "\n" + "\n" + "```")
                    elif final[i]["tournament"] in kvenna:
                        string += ("```" + "\n" + "Deild: " + final[i]["tournament"] + "\n"
                                    + final[i]["date"] + " kl: " + final[i]["time"] + "\n" + final[i]["homeTeam"]
                                    + " - " + final[i]["awayTeam"] + "\n" + "Staðsetning: " + final[i]["location"]
                                    + "\n" + "\n" + "```")

        if not string:
            await bot.say("Fann enga leiki með " + lið.title() + " á næstu dögum.")
        else:
            await bot.say(string)
    else:
        await bot.say("Náði ekki sambandi við API")

@bot.command(description="Nær í gif af giphy útfrá keywordi")
async def gif(*keywords: str):
    """Reynir að finna gif útfrá keywordi, t.d !gif dog"""

    if not keywords:
        await bot.say("Vantar keyword t.d. !gif hitler")
        return

    key = s.getGiphyKey()

    searchstring = "+".join(keywords)
    r = requests.get("http://api.giphy.com/v1/gifs/translate?s=" + searchstring + "&api_key=" + key + "&limit=1")

    if r.status_code == 200:
        result = r.json()
        final = result["data"]

        if final:
            await bot.say(final["embed_url"])
        else:
            await bot.say("Úbbs ég kúkaði á mig og fann ekkert.")
    else:
        await bot.say("Náði ekki sambandi við API")

@bot.command(description="Prentar eina setningu af wikipedia útfrá keywordi")
async def wiki(*keyword: str):
    """Reynir að finna wikipedia grein útfrá keywordi, t.d !wiki hitler"""

    searchstring = " ".join(keyword)

    try:
        result = wikipedia.page(searchstring)
    except wikipedia.PageError:
        result = "Fann ekkert um: " + "```" + searchstring + "```"
        await bot.say(result)
        return
    except wikipedia.DisambiguationError as e:
        opts = ', '.join(e.options)
        result = "Of víðtækt, meintiru kannski: " + "```" + opts + "```"
        await bot.say(result)
        return

    em = discord.Embed(color=0xe67e22)
    em.title = result.title
    em.url = result.url
    textlist = textwrap.wrap(result.content, 500, break_long_words=True, replace_whitespace=False)
    em.add_field(name="Af Wikipedia:", value=textlist[0] + "...")

    await bot.say(embed=em)

@bot.command(description="Convertar Evru(EUR), Dollara(USD) eða Pund(GBP) yfir í Ísl-krónur")
async def curr(value: float, currency: str):
    """Convertar EUR, USD eða GBP yfir í ísl-krónur, t.d !curr 50 usd"""

    r = requests.get("http://apis.is/currency/LB")

    if r.status_code == 200:
        result = r.json()

        final = result["results"]
        li = []
        di = {}

        for i in range(3):
            li.append(final[i])

        if currency.lower() == "eur":
            di = li[0]
        elif currency.lower() == "usd":
            di = li[1]
        elif currency.lower() == "gbp":
            di = li[2]

        val = di["value"]
        res = value * val
        string = "```fix" + "\n" + str("{:,.2f}".format(value)) + " " + currency.lower() + " = " + str("{:,}".format(int(res))) + " kr" + "\n" + "```"

        await bot.say(string)
    else:
        await bot.say("Náði ekki sambandi við API")

@bot.command(description="Hvað er heitt úti?")
async def hvaðerheitt():
    """Nær í nýjustu hitatölur frá veðurstofu"""

    r = requests.get("http://apis.is/weather/observations/is?stations=1,422,990")

    if r.status_code == 200:
        result = r.json()

        rey = result["results"][0]
        ak = result["results"][1]
        kef = result["results"][2]

        reykjavik = "``` " + rey["T"] + " °C í Reykjavík" + "```"
        akureyri = "``` " + ak["T"] + " °C á Akureyri" + "```"
        keflavik = "``` " + kef["T"] + " °C í Keflavík" + "```"

        await bot.say(keflavik)
        await bot.say(reykjavik)
        await bot.say(akureyri)
    else:
        await bot.say("Náði ekki sambandi við API")

@bot.command(description="Nær í handahófskennt grín af reddit.com/r/jokes")
async def grín():
    """Nær í handahófskennt grín af reddit.com/r/jokes"""

    data = s.getRedditInfo()

    redd = praw.Reddit(client_id=data["clientId"],
                         client_secret=data["clientSecret"],
                         password=data["password"],
                         username=data["username"],
                         user_agent=data["userAgent"])

    post = redd.subreddit("jokes").hot(limit=10)
    li = []

    for sub in post:
        li.append(sub)

    rand = random.choice(li)


    em = discord.Embed(color=0xe67e22)
    em.title = "Link"
    em.url = rand.url
    if rand.selftext:
        em.add_field(name=rand.title, value=rand.selftext)

    await bot.say(embed=em)

@bot.command(description="Nær í mest upvoteaðasta trailer/teaser af /r/movies")
async def trailer():
    """Nær í mest upvoteaðasta trailer/teaser af /r/movies"""

    data = s.getRedditInfo()

    redd = praw.Reddit(client_id=data["clientId"],
                       client_secret=data["clientSecret"],
                       password=data["password"],
                       username=data["username"],
                       user_agent=data["userAgent"])

    post = redd.subreddit("movies").hot(limit=50)
    li = []

    for sub in post:
        if "trailer" in sub.title.lower() or "teaser" in sub.title.lower():
            li.append(sub)

    if len(li) == 0:
        await bot.say("Fann engann trailer á /r/movies")
        return

    final = sorted(li, key=lambda k: k.score)
    await bot.say(final[-1].url)

@bot.command(description="Þakkaðu bottanum fyrir")
async def takk():
    """Þakkaðu bottanum fyrir vel unnin störf"""

    replies = ["Minnsta málið kallinn minn.", "Mín var ánægjan elsku vinur.", "Ég lifi til að þjóna.",
               "Ekkert mál lambið mitt.", "Þúst, bara gaman að geta hjálpað.",
               "Ekki minnast á það dúllan mín.", "Np sæti.", "Oki doki pepperobi.",
               "Beep boop np.", "Hehe þetta var gaman."]

    await bot.say(random.choice(replies))

@bot.command(pass_context=True, hidden=True)
async def bæ(ctx):
    """Command til að slökkva á bottanum fyrir development purposes"""

    me = s.getMe()

    if ctx.message.author.id == me:
        await bot.delete_message(ctx.message)
        await bot.logout()
    else:
        await bot.say("Einungis <@" + me + "> má slökkva á mér.")

@bot.command(description="Nær í næstu leiki tiltekins lið í enska eða leiki næstu viku ef slept er að setja inn lið")
async def enski(lið: str="", leikir: int=1):
    """Nær í næsta leik/leiki hjá tilteknu liði, t.d: !enski arsenal 5 --
    eða leiki næstu viku, t.d.: !enski"""

    r = requests.get("http://www.football-data.org/v1/competitions/445/fixtures",
                     headers={"X-Response-Control": "minified"})

    if leikir > 20:
        leikir = 20

    if r.status_code == 200:
        result = r.json()

        if not lið:
            u = datetime.datetime.now()
            d = datetime.timedelta(days=7)
            weekfromnow = u + d
            string = ""
            fmt = "%Y-%m-%dT%H:%M:%SZ"

            for i in result["fixtures"]:
                if (datetime.datetime.strptime(i["date"], fmt) > datetime.datetime.now()
                and datetime.datetime.strptime(i["date"], fmt) < weekfromnow):
                    d = datetime.datetime.strptime(i["date"], fmt)
                    string += ("```" + "\n" + d.strftime("%B %d, %Y") + " - " + d.strftime("%H:%M") + "\n"
                                + i["homeTeamName"] + " - " + i["awayTeamName"] + "\n" + "```")

            if string:
                await bot.say(string)
                return
            else:
                await bot.say("Fann enga leiki á næstu viku.")
                return

        # edge cases
        if lið.lower() == "man" or lið.lower() == "united" or lið.lower() == "manu":
            team = "Manchester United"
        elif lið.lower() == "city":
            team = "Manchester City"
        elif lið.lower() == "gunners":
            team = "Arsenal"
        else:
            team = lið.title()
        # edge cases END

        fmt = "%Y-%m-%dT%H:%M:%SZ"
        count = leikir
        itercount = 0
        string = ""

        for i in result["fixtures"]:
            if team in i["awayTeamName"] or team in i["homeTeamName"]:
                if datetime.datetime.strptime(i["date"], fmt) > datetime.datetime.now():
                    d = datetime.datetime.strptime(i["date"], fmt)
                    string += ("```" + "\n" + d.strftime("%B %d, %Y") + " - " + d.strftime("%H:%M") + "\n"
                               + i["homeTeamName"] + " - " + i["awayTeamName"] + "\n" + "```")
                    itercount += 1

                    if itercount == count:
                        break
        if string:
            await bot.say(string)
        else:
            await bot.say("Uuu... Fann ekkert um " + team)

    else:
        await bot.say("Náði ekki sambandi við API")

@bot.command(description="Er Tommi að streama?")
async def ertommiaðstreama():
    """Checkar hvort Tommi er að streama"""

    cid = s.getTwitchKey()
    r = requests.get("https://api.twitch.tv/kraken/streams?channel=qwaaag&client_id=" + cid)

    if r.status_code == 200:
        result = r.json()

        if result["streams"]:
            game = result["streams"][0]["game"]
            viewers = str(result["streams"][0]["viewers"])

            em = discord.Embed(color=0xe67e22)
            em.title = "Tommi er live! Smelltu hér til að horfa!"
            em.url = "https://www.twitch.tv/qwaaag"
            em.description = "Hann er að spila " + game + " og það eru " + viewers + " manns að horfa."

            await bot.say(embed=em)
        else:
            await bot.say("Nei, Tommi er ekki að streama.")
    else:
        await bot.say("Náði ekki sambandi við API")

@bot.command(description="Er <streamer> að spila?")
async def stream(streamer: str):
    """Checkar hvort <streamer> er að streama"""

    cid = s.getTwitchKey()
    lower = streamer.lower()
    r = requests.get("https://api.twitch.tv/kraken/streams?channel=" + lower + "&client_id=" + cid)

    if r.status_code == 200:
        result = r.json()

        if result["streams"]:
            game = result["streams"][0]["game"]
            viewers = str(result["streams"][0]["viewers"])

            em = discord.Embed(color=0xe67e22)
            em.title = streamer + " er live! Smelltu hér til að horfa!"
            em.url = "https://www.twitch.tv/" + lower
            em.description = "Hann er að spila " + game + " og það eru " + viewers + " manns að horfa."

            await bot.say(embed=em)
        else:
            await bot.say("Nei, " + streamer + " er ekki að streama.")
    else:
        await bot.say("Náði ekki sambandi við API")

@bot.command(description="Er <mynd> í bíó?")
async def bíó(*mynd: str):
    """Er <mynd> í bíó?"""

    if not mynd:
        await bot.say("Vantar mynd, t.d: !bíó Dunkirk")
        return

    pw = s.getMoviePw()
    r = requests.post("http://api.kvikmyndir.is/authenticate", data={"username": "TotiGunn", "password": pw})

    if r.status_code == 200:
        result = r.json()
        token = result["token"]

        r2 = requests.get("http://api.kvikmyndir.is/movies", headers={"x-access-token": token})
        movies = r2.json()
        found = False
        m = " ".join(mynd)

        for i in movies:
            if i["title"].lower() == m.lower() or i["title"].lower() in m.lower():
                found = True
                em = discord.Embed(color=0xe67e22)
                em.title = i["title"] + " (trailer)"
                em.set_image(url=i["poster"])

                if i["trailers"]:
                    if i["trailers"][0]["results"]:
                        tr = i["trailers"][0]["results"][0]["url"]
                        em.url = tr

                for j in i["showtimes"]:
                    em.add_field(name=j["cinema"]["name"], value=", ".join([x["time"] for x in j["schedule"]]))

                footer = "IMDB: " + i["ratings"]["imdb"] + ", Rotten Tomatoes: " + i["ratings"]["rotten_critics"]
                em.set_footer(text=footer)

        if not found:
            await bot.say(m + " er ekki í bíó :(")
            return

        await bot.say(embed=em)
    else:
        await bot.say("Náði ekki sambandi við API")

bot.run(t)
