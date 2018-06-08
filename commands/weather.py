import discord
from discord.ext import commands
import requests

class Weather:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Veður fyrir næstu daga")
    async def veður(self):
        """Veður fréttir fyrir næstu daga"""

        r = requests.get("http://apis.is/weather/texts?types=5")

        if r.status_code == 200:
            result = r.json()
            final = result["results"][0]

            # ``` prefixið í mörgum strengjum í þessu forriti er til að Discord formatti strenginn á ákveðinn hátt.
            await self.bot.say("```" + final["content"] + "```")
        else:
            await self.bot.say("Náði ekki sambandi við API")

    @commands.command(description="Hvað er heitt úti?")
    async def hvaðerheitt(self):
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

            await self.bot.say(keflavik)
            await self.bot.say(reykjavik)
            await self.bot.say(akureyri)
        else:
            await self.bot.say("Náði ekki sambandi við API")
    

def setup(bot):
    bot.add_cog(Weather(bot))