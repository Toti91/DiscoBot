import discord
from discord.ext import commands
import random
import json

class Rng:
    def __init__(self, bot):
        self.bot = bot
        self.winner = '100'

    @commands.command(description="Skipun sem velur random leik til að spila?")
    async def veljaleik(self, *leikir: str):
        """Velur einn random leik, t.d !veljaleik lol pugb rocketleague"""

        await self.bot.say(random.choice(leikir))

    @commands.command(description="Hvað á stebbi að spila í lol?")
    async def hvaðástebbiaðspila(self):
        """Hvað á stebbi að spila í lol"""

        heroes = ["Xin Zhao", "Gnarr", "Quinn"]

        await self.bot.say(random.choice(heroes))

    @commands.command(description="Slot machine woo", pass_context=True)
    async def slots(self, ctx):
        channel = ctx.message.channel.id
        slotsChannel = '454690355431079966'

        if channel != slotsChannel:
            await self.bot.say('Þú verður að vera á slots channelinu til að spila slots.')
            return

        slots = ['chocolate_bar', 'star', 'grapes', 'apple', 'gem', self.winner]

        row1 = [slots[random.randint(0, 5)], slots[random.randint(0, 5)], slots[random.randint(0, 5)], slots[random.randint(0, 5)]]
        row2 = [slots[random.randint(0, 5)], slots[random.randint(0, 5)], slots[random.randint(0, 5)], slots[random.randint(0, 5)]]
        row3 = [slots[random.randint(0, 5)], slots[random.randint(0, 5)], slots[random.randint(0, 5)], slots[random.randint(0, 5)]]
        row4 = [slots[random.randint(0, 5)], slots[random.randint(0, 5)], slots[random.randint(0, 5)], slots[random.randint(0, 5)]]

        rows = [row1, row2, row3, row4]

        # 15% líkur að vinna automatically
        oddBoost = random.randint(0, 100)
        if oddBoost < 15:
            index = random.randint(0, 3)
            slotIndex = random.randint(0, 5)
            rowCol = random.randint(0, 1)

            if rowCol:
                for i in range(0, 4):
                    rows[index][i] = slots[slotIndex]
            else:
                for i in range(0, 4):
                    rows[i][index] = slots[slotIndex]

        col1 = [row1[0], row2[0], row3[0], row4[0]]
        col2 = [row1[1], row2[1], row3[1], row4[1]]
        col3 = [row1[2], row2[2], row3[2], row4[2]]
        col4 = [row1[3], row2[3], row3[3], row4[3]]
                

        slotOutput = '''|\t:{}:\t|\t:{}:\t|\t:{}:\t|\t:{}:\t|\n
|\t:{}:\t|\t:{}:\t|\t:{}:\t|\t:{}:\t|\n
|\t:{}:\t|\t:{}:\t|\t:{}:\t|\t:{}:\t|\n
|\t:{}:\t|\t:{}:\t|\t:{}:\t|\t:{}:\t|\n'''.format(row1[0], row1[1], row1[2], row1[3],
                                                row2[0], row2[1], row2[2], row2[3],
                                                row3[0], row3[1], row3[2], row3[3],
                                                row4[0], row4[1], row4[2], row4[3])
        res = ''
        user = ctx.message.author.id
        slotOutput += '-----------------------------------------'

        if self.checkJackpot(row1) or self.checkJackpot(row2) or self.checkJackpot(row3) or self.checkJackpot(row4):
            res = slotOutput + '\n$$$ ROYAAAAL $$$\t$200 Aparólu Dollarar\n```Staða: $' + str(self.winSlots(user, 200)) + '```'

        elif self.checkJackpot(col1) or self.checkJackpot(col2) or self.checkJackpot(col3) or self.checkJackpot(col4):
            res = slotOutput + '\n$$$ ROYAAAAL $$$\t$200 Aparólu Dollarar\n```Staða: $' + str(self.winSlots(user, 200)) + '```'

        elif self.checkEqual(row1) or self.checkEqual(row2) or self.checkEqual(row3) or self.checkEqual(row4):
            res = slotOutput + '\nWin!\t$20 Aparólu Dollarar\n```Staða: $' + str(self.winSlots(user, 20)) + '```'

        elif self.checkEqual(col1) or self.checkEqual(col2) or self.checkEqual(col3) or self.checkEqual(col4):
            res = slotOutput + '\nWin!\t$20 Aparólu Dollarar\n```Staða: $' + str(self.winSlots(user, 20)) + '```'

        else:
            res = slotOutput + '\nEnginn vinningur'

        await self.bot.say(res)

    @commands.command(description="Sýnir hvað þú átt mikið af aparólu dollurum", pass_context=True)
    async def balance(self, ctx):
        """Sýnir hvað þú átt mikið af aparólu dollurum"""

        user = ctx.message.author.id
        res = '```$' + str(self.winSlots(user, 0)) + ' Aparólu Dollarar```'

        await self.bot.say(res)

    @commands.command(description="Sýnir hvað allir eiga mikla aparólu dollara", pass_context=True)
    async def balanceall(self, ctx):
        '''Sýnir hvað allir eiga mikla aparólu dollara'''

        server = ctx.message.server
        path = 'slots.json'
        res = ''
        users = []

        with open(path, 'r') as file:
            data = json.load(file)
            for u in data['slots']:
                user = {
                    'name': server.get_member(u['id']).name,
                    'balance': u['money']
                }
                users.append(user)
        
        users.sort(key=lambda x: x['balance'], reverse=True)

        for u in users:
            res += '```'+u['name']+': $'+str(u['balance'])+'```'

        await self.bot.say(res)
                



    def winSlots(self, user, amount):
        found = False
        value = 0
        data = None
        path = 'slots.json'
        with open(path, 'r') as file:
            data = json.load(file)
            for u in data['slots']:
                if u['id'] == user:
                    found = True
                    value = int(u['money']) + amount
                    u['money'] = value

        if not found:
            value = amount
            player = {
                'id': user,
                'money': value
            }
            data['slots'].append(player)

        with open(path, 'w+') as file:
            json.dump(data, file)

        return value

    def checkEqual(self, iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return True
        return all(first == rest for rest in iterator)

    def checkJackpot(self, list):
        if self.checkEqual(list) and list[0] == self.winner:
            return True
        
        return False
                

def setup(bot):
    bot.add_cog(Rng(bot))