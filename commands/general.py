import discord
from discord.ext import commands
from secret import Secret
import requests
import wikipedia
import textwrap
import random
import praw

class General:
    def __init__(self, bot):
        self.bot = bot
        self.replies = ["Minnsta málið kallinn minn.", "Mín var ánægjan elsku vinur.",
                        "Ég lifi til að þjóna.", "Ekkert mál lambið mitt.",
                        "Þúst, bara gaman að geta hjálpað.", "Ekki minnast á það dúllan mín.",
                        "Np sæti.", "Oki doki pepperobi.", "Beep boop np.", "Hehe þetta var gaman."]
        self.s = Secret()

    @commands.command(description="Nær í gif af giphy útfrá keywordi")
    async def gif(self, *keywords: str):
        """Reynir að finna gif útfrá keywordi, t.d !gif dog"""

        if not keywords:
            await bot.say("Vantar keyword t.d. !gif hitler")
            return

        key = self.s.getGiphyKey()

        searchstring = "+".join(keywords)
        r = requests.get("http://api.giphy.com/v1/gifs/translate?s=" + searchstring + "&api_key=" + key + "&limit=1")

        if r.status_code == 200:
            result = r.json()
            final = result["data"]

            if final:
                await self.bot.say(final["embed_url"])
            else:
                await self.bot.say("Úbbs ég kúkaði á mig og fann ekkert.")
        else:
            await self.bot.say("Náði ekki sambandi við API")

    @commands.command(description="Prentar eina setningu af wikipedia útfrá keywordi")
    async def wiki(self, *keyword: str):
        """Reynir að finna wikipedia grein útfrá keywordi, t.d !wiki hitler"""

        searchstring = " ".join(keyword)

        try:
            result = wikipedia.page(searchstring)
        except wikipedia.PageError:
            result = "Fann ekkert um: " + "```" + searchstring + "```"
            await self.bot.say(result)
            return
        except wikipedia.DisambiguationError as e:
            opts = ', '.join(e.options)
            result = "Of víðtækt, meintiru kannski: " + "```" + opts + "```"
            await self.bot.say(result)
            return

        em = discord.Embed(color=0xe67e22)
        em.title = result.title
        em.url = result.url
        textlist = textwrap.wrap(result.content, 500, break_long_words=True, replace_whitespace=False)
        em.add_field(name="Af Wikipedia:", value=textlist[0] + "...")

        await self.bot.say(embed=em)

    @commands.command(description="Convertar Evru(EUR), Dollara(USD) eða Pund(GBP) yfir í Ísl-krónur")
    async def curr(self, value: float, currency: str):
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

            await self.bot.say(string)
        else:
            await self.bot.say("Náði ekki sambandi við API")

    @commands.command(description="Þakkaðu bottanum fyrir")
    async def takk(self):
        """Þakkaðu bottanum fyrir vel unnin störf"""

        await self.bot.say(random.choice(self.replies))

    @commands.command(description="Nær í handahófskennt grín af reddit.com/r/jokes")
    async def grín(self):
        """Nær í handahófskennt grín af reddit.com/r/jokes"""

        data = self.s.getRedditInfo()

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

        await self.bot.say(embed=em)

    @commands.command(description="Nær í mest upvoteaðasta trailer/teaser af /r/movies")
    async def trailer(self):
        """Nær í mest upvoteaðasta trailer/teaser af /r/movies"""

        data = self.s.getRedditInfo()

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
            await self.bot.say("Fann engann trailer á /r/movies")
            return

        final = sorted(li, key=lambda k: k.score)
        await self.bot.say(final[-1].url)

    @commands.command(description="Er <mynd> í bíó?")
    async def bíó(self, *mynd: str):
        """Er <mynd> í bíó?"""

        if not mynd:
            await self.bot.say("Vantar mynd, t.d: !bíó Dunkirk")
            return

        pw = self.s.getMoviePw()
        r = requests.post("http://api.kvikmyndir.is/authenticate", data={"username": "TotiGunn", "password": pw})

        if r.status_code == 200:
            result = r.json()
            token = result["token"]
            m = ' '.join(mynd)

            r2 = requests.get("http://api.kvikmyndir.is/movies", headers={"x-access-token": token})
            movies = r2.json()
            found = False

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
                await self.bot.say(m + " er ekki í bíó :(")
                return

            await self.bot.say(embed=em)
        else:
            await self.bot.say("Náði ekki sambandi við API")

def setup(bot):
    bot.add_cog(General(bot))