import discord
from discord.ext import commands
from secret import Secret
import requests

class Twitch:
    def __init__(self, bot):
        self.bot = bot
        self.s = Secret()

    def getTwitch(self, streamer: str):
        cid = self.s.getTwitchKey()
        lower = streamer.lower()
        r = requests.get("https://api.twitch.tv/kraken/streams?channel=" + lower + "&client_id=" + cid)

        if r.status_code == 200:
            result = r.json()
            em = discord.Embed(color=0xe67e22)

            if result["streams"]:
                game = result["streams"][0]["game"]
                viewers = str(result["streams"][0]["viewers"])

                em.title = streamer + " er live! Smelltu hér til að horfa!"
                em.url = "https://www.twitch.tv/" + lower
                em.description = "Hann er að spila " + game + " og það eru " + viewers + " manns að horfa."

                return em
            else:
                em.title = "NOPE"
                em.description = streamer + " er ekki að streama"

                return em
        else:
            print("Náði ekki sambandi við API")

    @commands.command(description="Er <streamer> að spila?")
    async def stream(self, streamer: str):
        """Checkar hvort <streamer> er að streama"""

        em = self.getTwitch(streamer)

        await self.bot.say(embed=em)

    @commands.command(description="Er Tommi að streama?")
    async def ertommiaðstreama(self):
        """Checkar hvort Tommi er að streama"""

        em = self.getTwitch("QWAAAG")

        await self.bot.say(embed=em)

    @commands.command(description="Er Stebbi að streama?")
    async def erstebbiaðstreama(self):
        """Checkar hvort Stebbi er að streama"""

        em = self.getTwitch("stebiilust")

        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(Twitch(bot))