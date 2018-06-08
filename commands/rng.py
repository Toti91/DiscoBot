import discord
from discord.ext import commands
import random

class Rng:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Skipun sem velur random leik til að spila?")
    async def veljaleik(self, *leikir: str):
        """Velur einn random leik, t.d !veljaleik lol pugb rocketleague"""

        await self.bot.say(random.choice(leikir))

    @commands.command(description="Hvað á stebbi að spila í lol?")
    async def hvaðástebbiaðspila(self):
        """Hvað á stebbi að spila í lol"""

        heroes = ["Xin Zhao", "Gnarr", "Quinn"]

        await self.bot.say(random.choice(heroes))

    @commands.command(description="Slot machine woo")
    async def slots(self):
        winner = '100'
        slots = ['chocolate_bar', 'star', 'grapes', 'apple', 'gem', winner]
        slot1 = slots[random.randint(0, 5)]
        slot2 = slots[random.randint(0, 5)]
        slot3 = slots[random.randint(0, 5)]
        slot4 = slots[random.randint(0, 5)]

        slotOutput = '|\t:{}:\t|\t:{}:\t|\t:{}:\t|\t:{}:\t|\n'.format(slot1, slot2, slot3, slot4)
        res = ''

        if slot1 == slot2 and slot2 == slot3 and slot3 == slot4 and slot4 != winner:
            res = slotOutput + '-----------\n$$ WOW $$'

        elif slot1 == winner and slot2 == winner and slot3 == winner and slot4 == winner:
            res = slotOutput + '----------------\n$$$ ROYAAAAL $$$'

        elif slot1 == slot2 and slot3 == slot4 or slot1 == slot3 and slot2 == slot4 or slot1 == slot4 and slot2 == slot3:
            res = slotOutput + '----------\n$ NICE $'

        else:
            res = slotOutput

        await self.bot.say(res)

def setup(bot):
    bot.add_cog(Rng(bot))