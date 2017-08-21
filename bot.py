from discord.ext.commands import Bot
import discord
import wikipedia
import requests
import random
import json
import textwrap
import praw
import datetime
import asyncio
from secret import Secret

description = "Botti sem Tóti er að gera og vonandi verður gaman"
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

@bot.command(description="Skipun til að velja random leik þegar við getum ekki ákveðið neitt sem vinahópur")
async def veljaleik(*leikir : str):
    """Velur einn random hlut af því sem þú segir, t.d !veljaleik lol pugb rocketleague"""

    await bot.say(random.choice(leikir))

@bot.command(description="Veður fyrir næstu daga")
async def veður():
    """Veður fréttir fyrir næstu daga"""

    r = requests.get("http://apis.is/weather/texts?types=5")
    if r.status_code == 200:
        parsed = r.json()
        dumped = json.dumps(parsed, ensure_ascii=False, indent=4, sort_keys=True)
        result = json.loads(dumped)
        final = result["results"][0]

        await bot.say("```" + final["content"] + "```")
    else:
        await bot.say("Úbbs ég kúkaði á mig.. Reyndu aftur")

@bot.command(description="Næstu leikir Keflavíkur")
async def keflavík():
    """Næstu leikir Keflavíkur, meistaraflokkur karla og kvenna"""

    r = requests.get("http://apis.is/sports/football")
    if r.status_code == 200:
        parsed = r.json()
        dumped = json.dumps(parsed, ensure_ascii=False, indent=4, sort_keys=True)
        result = json.loads(dumped)
        final = result["results"]
        final = sorted(final, key=lambda k: k['counter'])
        streng = ""
        deildir = ["Inkasso-deildin", "Pepsi-deild karla", "Meistaradeild UEFA", "Borgunarbikar karla"]
        kvenna = ["1. deild kvenna", "Pepsi-deild kvenna"]

        for i in range(len(final)):
            for key, value in final[i].items():
                if value == "Keflavík":
                    if final[i]["tournament"] in deildir:
                        streng += ("```fix" + "\n" + "Deild: " + final[i]["tournament"] + "\n"
                                    + final[i]["date"] + " kl: " + final[i]["time"] + "\n" + final[i]["homeTeam"]
                                    + " - " + final[i]["awayTeam"] + "\n" + "Staðsetning: " + final[i]["location"]
                                    + "\n" + "\n" + "```")
                    elif final[i]["tournament"] in kvenna:
                        streng += ("```" + "\n" + "Deild: " + final[i]["tournament"] + "\n"
                                    + final[i]["date"] + " kl: " + final[i]["time"] + "\n" + final[i]["homeTeam"]
                                    + " - " + final[i]["awayTeam"] + "\n" + "Staðsetning: " + final[i]["location"]
                                    + "\n" + "\n" + "```")

        if not streng:
            await bot.say("Fann enga leiki með Keflavík á næstu dögum.")
        else:
            await bot.say(streng)
    else:
        await bot.say("Úbbs ég kúkaði á mig.. Reyndu aftur")

@bot.command(description="Næstu leikir tiltekins liðs")
async def fótbolti(lið : str):
    """Næstu leikir tiltekins liðs, t.d !fótbolti íbv"""

    r = requests.get("http://apis.is/sports/football")
    if r.status_code == 200:
        parsed = r.json()
        dumped = json.dumps(parsed, ensure_ascii=False, indent=4, sort_keys=True)
        result = json.loads(dumped)
        final = result["results"]
        final = sorted(final, key=lambda k: k['counter'])
        streng = ""
        deildir = ["Inkasso-deildin", "Pepsi-deild karla", "Meistaradeild UEFA", "Borgunarbikar karla"]
        kvenna = ["1. deild kvenna", "Pepsi-deild kvenna"]

        for i in range(len(final)):
            for key, value in final[i].items():
                if str(value).lower() == lið.lower():
                    if final[i]["tournament"] in deildir:
                        streng += ("```fix" + "\n" + "Deild: " + final[i]["tournament"] + "\n"
                                    + final[i]["date"] + " kl: " + final[i]["time"] + "\n" + final[i]["homeTeam"]
                                    + " - " + final[i]["awayTeam"] + "\n" + "Staðsetning: " + final[i]["location"]
                                    + "\n" + "\n" + "```")
                    elif final[i]["tournament"] in kvenna:
                        streng += ("```" + "\n" + "Deild: " + final[i]["tournament"] + "\n"
                                    + final[i]["date"] + " kl: " + final[i]["time"] + "\n" + final[i]["homeTeam"]
                                    + " - " + final[i]["awayTeam"] + "\n" + "Staðsetning: " + final[i]["location"]
                                    + "\n" + "\n" + "```")

        if not streng:
            await bot.say("Fann enga leiki með " + lið.title() + " á næstu dögum.")
        else:
            await bot.say(streng)
    else:
        await bot.say("Úbbs ég kúkaði á mig.. Reyndu aftur")

@bot.command(description="Nær í gif af giphy útfrá keywordi")
async def gif(*keywords : str):
    """Reynir að finna gif útfrá keywordi, t.d !gif dog"""

    if not keywords:
        await bot.say("Vantar keyword t.d. !gif hitler")
        return

    key = s.getGiphyKey()

    searchstring = "+".join(keywords)
    r = requests.get("http://api.giphy.com/v1/gifs/translate?s="+searchstring+"&api_key="+key+"&limit=1")
    if r.status_code == 200:
        parsed = r.json()
        dumped = json.dumps(parsed, ensure_ascii=False, indent=4, sort_keys=True)
        result = json.loads(dumped)
        final = result["data"]

        if final:
            await bot.say(final["embed_url"])
        else:
            await bot.say("Úbbs ég kúkaði á mig og fann ekkert.")
    else:
        await bot.say("Úbbs ég kúkaði á mig.. Reyndu aftur")

@bot.command(description="Prentar eina setningu af wikipedia útfrá keywordi")
async def wiki(*keyword : str):
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
    em.add_field(name="Af Wikipedia:", value=textlist[0]+"...")

    await bot.say(embed=em)

@bot.command(description="Convertar Evru(EUR), Dollara(USD) eða Pund(GBP) yfir í Ísl-krónur")
async def curr(value : float, currency : str):
    """Convertar EUR, USD eða GBP yfir í ísl-krónur, t.d !curr 50 usd"""

    r = requests.get("http://apis.is/currency/LB")
    if r.status_code == 200:
        parsed = r.json()
        dumped = json.dumps(parsed, ensure_ascii=False, indent=4, sort_keys=True)
        result = json.loads(dumped)
        final = result["results"]
        li = []
        dict = {}
    else:
        await bot.say("Úbbs ég kúkaði á mig.. Reyndu aftur")
        return

    for i in range(3):
        li.append(final[i])

    ''' Vantar Switch statement i Python? '''
    if currency.lower() == "eur":
        dict = li[0]
    elif currency.lower() == "usd":
        dict = li[1]
    elif currency.lower() == "gbp":
        dict = li[2]

    val = dict["value"]
    res = value * val
    streng = "```fix" + "\n" + str(value) + " " + currency.lower() + " = " + str(int(res)) + " kr" + "\n" + "```"

    await bot.say(streng)

@bot.command(description="Hvað er heitt úti?")
async def hvaðerheitt():
    """Nær í nýjustu hitatölur frá veðurstofu"""

    r = requests.get("http://apis.is/weather/observations/is?stations=1,422,990")
    if r.status_code == 200:
        parsed = r.json()
        dumped = json.dumps(parsed, ensure_ascii=False, indent=4, sort_keys=True)
        result = json.loads(dumped)
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
        await bot.say("Úbbs ég kúkaði á mig.. Reyndu aftur")

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

    me = s.getMe()

    if ctx.message.author.id == me:
        await bot.delete_message(ctx.message)
        await bot.logout()
    else:
        await bot.say("Einungis <@"+me+"> má slökkva á mér.")

@bot.command(pass_context=True, no_pm=True)
async def userinfo(ctx, *, user: discord.Member=None):
    """Shows users's informations"""

    author = ctx.message.author
    server = ctx.message.server

    if not user:
        user = author

    roles = [x.name for x in user.roles if x.name != "@everyone"]

    joined_at = user.joined_at
    since_created = (ctx.message.timestamp - user.created_at).days
    since_joined = (ctx.message.timestamp - joined_at).days
    user_joined = joined_at.strftime("%d %b %Y %H:%M")
    user_created = user.created_at.strftime("%d %b %Y %H:%M")
    member_number = sorted(server.members,
                            key=lambda m: m.joined_at).index(user) + 1

    created_on = "{}\n({} days ago)".format(user_created, since_created)
    joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

    game = "Chilling in {} status".format(user.status)

    if user.game is None:
        pass
    elif user.game.url is None:
        game = "Playing {}".format(user.game)
    else:
        game = "Streaming: [{}]({})".format(user.game, user.game.url)

    if roles:
        roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                    if x.name != "@everyone"].index)
        roles = ", ".join(roles)
    else:
        roles = "None"

    data = discord.Embed(description=game, colour=user.colour)
    data.add_field(name="Joined Discord on", value=created_on)
    data.add_field(name="Joined this server on", value=joined_on)
    data.add_field(name="Roles", value=roles, inline=False)
    data.set_footer(text="Member #{} | User ID:{}"
                    "".format(member_number, user.id))

    name = str(user)
    name = " ~ ".join((name, user.nick)) if user.nick else name

    if user.avatar_url:
        data.set_author(name=name, url=user.avatar_url)
        data.set_thumbnail(url=user.avatar_url)
    else:
        data.set_author(name=name)

    try:
        await bot.say(embed=data)
    except discord.HTTPException:
        await bot.say("Úbbs ég kúkaði á mig..")

@bot.command(description="Nær í næstu leiki tiltekins lið í enska")
async def enski(lið : str, leikir : int=1):
    """Nær í næsta leik/leiki hjá tilteknu liði, t.d: !enski arsenal 5"""

    r = requests.get("http://www.football-data.org/v1/competitions/445/fixtures?X-Response-Control=minified")

    if leikir > 20:
        leikir = 20

    if r.status_code == 200:
        parsed = r.json()
        dumped = json.dumps(parsed, ensure_ascii=False, indent=4, sort_keys=True)
        result = json.loads(dumped)

        #--edge cases
        if lið.lower() == "man" or lið.lower() == "united" or lið.lower() == "manu":
            tem = "Manchester United"
        elif lið.lower() == "city":
            tem = "Manchester City"
        elif lið.lower() == "gunners":
            tem = "Arsenal"
        else:
            tem = lið.title()
        #--edge cases END

        fmt = "%Y-%m-%dT%H:%M:%SZ"
        count = leikir
        itercount = 0
        streng = ""

        for i in result["fixtures"]:
            if tem in i["awayTeamName"] or tem in i["homeTeamName"]:
                if datetime.datetime.strptime(i["date"], fmt) > datetime.datetime.now():
                    d = datetime.datetime.strptime(i["date"], fmt)
                    streng += ("```" + "\n" + d.strftime("%B %d, %Y") + " - " + d.strftime("%H:%M") + "\n"
                               + i["homeTeamName"] + " - " + i["awayTeamName"] + "\n" + "```")
                    itercount += 1
                    if itercount == count:
                        break
        if streng:
            await bot.say(streng)
        else:
            await bot.say("Uuu... Fann ekkert um " + tem)

    else:
        await bot.say("Úbbs ég kúkaði á mig.. Reyndu aftur")

@bot.command(description="Er Tommi að streama?")
async def ertommiaðstreama():
    """Checkar hvort Tommi er að streama"""

    cId = s.getTwitchKey()

    r = requests.get("https://api.twitch.tv/kraken/streams?channel=qwaaag&client_id="+cId)
    if r.status_code == 200:
        parsed = r.json()
        dumped = json.dumps(parsed, ensure_ascii=False, indent=4, sort_keys=True)
        result = json.loads(dumped)

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
        await bot.say("Úbbs ég kúkaði á mig.. Reyndu aftur")

@bot.command(description="Er <streamer> að spila?")
async def stream(streamer : str):
    """Checkar hvort <streamer> er að streama"""

    cId = s.getTwitchKey()
    lower = streamer.lower()

    r = requests.get("https://api.twitch.tv/kraken/streams?channel="+lower+"&client_id="+cId)
    if r.status_code == 200:
        parsed = r.json()
        dumped = json.dumps(parsed, ensure_ascii=False, indent=4, sort_keys=True)
        result = json.loads(dumped)

        if result["streams"]:
            game = result["streams"][0]["game"]
            viewers = str(result["streams"][0]["viewers"])

            em = discord.Embed(color=0xe67e22)
            em.title = streamer + " er live! Smelltu hér til að horfa!"
            em.url = "https://www.twitch.tv/"+lower
            em.description = "Hann er að spila " + game + " og það eru " + viewers + " manns að horfa."

            await bot.say(embed=em)
        else:
            await bot.say("Nei, " + streamer + " er ekki að streama.")
    else:
        await bot.say("Fann engann streamer sem heitir " + streamer)

@bot.command(description="Hvað er í bíó?")
async def bíó():
    """Nær í hvaða myndir eru í bíó"""

    pw = s.getMoviePw()
    r = requests.post("http://api.kvikmyndir.is/authenticate", data={"username": "TotiGunn", "password": pw})

    if r.status_code == 200:
        result = r.json()
        token = result["token"]

        r2 = requests.get("http://api.kvikmyndir.is/movies", headers={"x-access-token": token})
        movies = r2.json()

        for i in movies:
            em = discord.Embed(color=0xe67e22)
            em.title = i["title"]

            if i["trailers"]:
                if i["trailers"][0]["results"]:
                    tr = i["trailers"][0]["results"][0]["url"]
                    em.url = tr

            for j in i["showtimes"]:
                em.add_field(name=j["cinema"]["name"], value=", ".join([x["time"] for x in j["schedule"]]))

            await bot.say(embed=em)
            await asyncio.sleep(0.1)




bot.run(t)
