import discord
from discord.ext import commands
from discord.utils import get
from secret import Secret
import time
from PIL import Image
from io import BytesIO
import urllib.request as urllib

class Mod:
    def __init__(self, bot):
        self.bot = bot
        self.cs = ["csgo", "cs:go", "cs"]
        self.lol = ["lol", "league", "leagueoflegends"]
        self.rocket = ["rl", "rocketleague", "rocket-league"]
        self.pugb = ["pubg", "battlegrounds", "playerunknowbattlegrounds"]
        self.s = Secret()

    def getRole(self, user, rl):
        if rl.lower() in self.cs:
            return get(user.server.roles, name="cs:go")
        elif rl.lower() == "overwatch":
            return get(user.server.roles, name="overwatch")
        elif rl.lower() in self.lol:
            return get(user.server.roles, name="lol")
        elif rl.lower() in self.rocket:
            return get(user.server.roles, name="rocket-league")
        elif rl.lower() in self.pugb:
            return get(user.server.roles, name="pubg")

    @commands.command(pass_context=True, hidden=True)
    async def bæ(self, ctx):
        """Command til að slökkva á bottanum fyrir development purposes"""

        me = self.s.getMe()

        if ctx.message.author.id == me:
            await self.bot.delete_message(ctx.message)
            await self.bot.logout()
        else:
            await self.bot.say("Einungis <@" + me + "> má slökkva á mér.")

    @commands.command(description="Vote-a að kicka <user>", pass_context=True)
    async def votekick(self, ctx, member: discord.Member=None):
        try:
            member = member or ctx.message.author

            timeout = 15
            afk = self.bot.get_channel(self.s.getAfkChannel()) # Channel id á AFK rás
            msg = "Viljið þið kicka <@" + str(member.id) + ">? Reactið með 👍 eða 👎, þið hafið " + str(timeout) + " sek."
            
            reply = await self.bot.say(msg)
            await self.bot.add_reaction(reply, "👍")
            await self.bot.add_reaction(reply, "👎")

            time.sleep(timeout)

            res = await self.bot.get_message(reply.channel, reply.id)
            reacts = res.reactions

            thumbsUp = reacts[0].count
            thumbsDown = reacts[1].count

            if thumbsUp > thumbsDown and thumbsUp > 2:
                await self.bot.say("Bæ <@" + str(member.id) + ">!")
                await self.bot.move_member(member, afk)
            else:
                await self.bot.say("Þú færð að lifa <@" + str(member.id) + ">!")
        except:
            await self.bot.say("Þú verður að @Mention-a þann sem þú vilt kicka.")

    @commands.command(description="Adda role á sjálfan þig fyrir leik", pass_context=True)
    async def addrole(self, ctx, rl: str=None):
        if not rl:
            await self.bot.say("Verður að velja role: csgo, lol, pubg, rocketleague, overwatch")
            return

        user = ctx.message.author
        role = self.getRole(user, rl)

        if not role:
            await self.bot.say("Ekkert role til sem heitir " + str(role))
            await self.bot.say("Roles: csgo, lol, pubg, rocketleague, overwatch")
            return

        await self.bot.add_roles(user, role)
        await self.bot.say("Addaði <@" + str(user.id) + "> í " + str(role) + " role-ið.")

    @commands.command(description="Remova role leikja frá sjálfum þér", pass_context=True)
    async def removerole(self, ctx, rl: str=None):
        if not rl:
            await self.bot.say("Verður að velja role: csgo, lol, pubg, rocketleague, overwatch")
            return

        user = ctx.message.author
        role = self.getRole(user, rl)

        if not role:
            await self.bot.say("Ekkert role til sem heitir " + str(role))
            await self.bot.say("Roles: csgo, lol, pubg, rocketleague, overwatch")
            return

        await self.bot.remove_roles(user, role)
        await self.bot.say("Deletaði <@" + str(user.id) + "> úr " + str(role) + " role-inu.")

    @commands.command(description="Gerir emoji úr <nafn> og <image-link>", pass_context=True)
    async def emoji(self, ctx, name: str=None, imgLink: str=None):
        if not imgLink or not name:
            await self.bot.say("Vantar nafn og/eða link á image! eg: !emoji broskall http://linkur_á_mynd.com")
            return
        
        user = ctx.message.author
        size = 128, 128
        fd = urllib.urlopen(imgLink)
        image_file = BytesIO(fd.read())
        im = Image.open(image_file)

        im.thumbnail(size)

        byteArr = BytesIO()
        im.save(byteArr, format="PNG")
        byteArr = byteArr.getvalue()

        em = await self.bot.create_custom_emoji(server=user.server, name=name, image=byteArr)
        msg = await self.bot.say("Takk fyrir emoji.")
        await self.bot.add_reaction(msg, em)

def setup(bot):
    bot.add_cog(Mod(bot))