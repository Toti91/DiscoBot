import discord
from discord.ext import commands
import requests
import datetime

class Sports:
    def __init__(self, bot):
        self.bot = bot
        self.deildir = ["Inkasso-deildin", "Pepsi-deild karla", "Meistaradeild UEFA", "Borgunarbikar karla"]
        self.kvenna = ["1. deild kvenna", "Pepsi-deild kvenna"]

    def getSoccer(self, team: str):
        r = requests.get("http://apis.is/sports/football")
        string = ""

        if r.status_code == 200:
            result = r.json()
            final = result["results"]
            final = sorted(final, key=lambda k: k['counter'])

            for i in range(len(final)):
                for key, value in final[i].items():
                    if str(value).lower() == team.lower():
                        if final[i]["tournament"] in self.deildir or team.lower() == "ísland":
                            string += ("```fix" + "\n" + "Deild: " + final[i]["tournament"] + "\n"
                                    + final[i]["date"] + " kl: " + final[i]["time"] + "\n" + final[i]["homeTeam"]
                                    + " - " + final[i]["awayTeam"] + "\n" + "Staðsetning: " + final[i]["location"]
                                    + "\n" + "\n" + "```")
                        elif final[i]["tournament"] in self.kvenna:
                            string += ("```" + "\n" + "Deild: " + final[i]["tournament"] + "\n"
                                    + final[i]["date"] + " kl: " + final[i]["time"] + "\n" + final[i]["homeTeam"]
                                    + " - " + final[i]["awayTeam"] + "\n" + "Staðsetning: " + final[i]["location"]
                                    + "\n" + "\n" + "```")

            return string
        else:
            string = "Náði ekki sambandi við API"
            return string

    @commands.command(description="Næstu leikir Keflavíkur")
    async def keflavík(self):
        """Næstu leikir Keflavíkur, meistaraflokkur karla og kvenna"""

        string = self.getSoccer("keflavík")

        if not string:
            await self.bot.say("Fann enga leiki með Keflavík á næstu dögum.")
        else:
            await self.bot.say(string)

    @commands.command(description="Næstu leikir tiltekins liðs")
    async def fótbolti(self, lið: str):
        """Næstu leikir tiltekins liðs, t.d !fótbolti íbv"""

        string = self.getSoccer(lið)

        if not string:
            await self.bot.say("Fann enga leiki með " + lið.title() + " á næstu dögum.")
        else:
            await self.bot.say(string)

    @commands.command(description="Nær í næstu leiki tiltekins lið í enska eða leiki næstu viku ef slept er að setja inn lið")
    async def enski(self, lið: str="", leikir: int=1):
        """Nær í næsta leik/leiki hjá tilteknu liði, t.d: !enski arsenal 5 --
        eða leiki næstu viku, t.d.: !enski"""

        r = requests.get("http://www.football-data.org/v1/competitions/445/fixtures",
                        headers={"X-Response-Control": "minified"})

        if leikir > 20:
            leikir = 20

        if r.status_code == 200:
            result = r.json()
            fmt = "%Y-%m-%dT%H:%M:%SZ"
            string = ""

            if not lið:
                u = datetime.datetime.now()
                d = datetime.timedelta(days=7)
                weekfromnow = u + d

                for i in result["fixtures"]:
                    if (datetime.datetime.strptime(i["date"], fmt) > datetime.datetime.now()
                    and datetime.datetime.strptime(i["date"], fmt) < weekfromnow):
                        d = datetime.datetime.strptime(i["date"], fmt)
                        string += ("```" + "\n" + d.strftime("%B %d, %Y") + " - " + d.strftime("%H:%M") + "\n"
                                    + i["homeTeamName"] + " - " + i["awayTeamName"] + "\n" + "```")

                if string:
                    await self.bot.say(string)
                    return
                else:
                    await self.bot.say("Fann enga leiki á næstu viku.")
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

            count = leikir
            itercount = 0

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
                await self.bot.say(string)
            else:
                await self.bot.say("Uuu... Fann ekkert um " + team)

        else:
            await self.bot.say("Náði ekki sambandi við API")

def setup(bot):
    bot.add_cog(Sports(bot))