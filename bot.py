from discord.ext.commands import Bot
import discord
from secret import Secret
from os import listdir
from os.path import isfile, join
import sys, traceback

description = "Ég er skrifaður í Python 3.6 með hjálp Discord.py"
s = Secret()
t = s.getToken()
cogs_dir = 'commands'
playing = discord.Game(name="Half-Life 3", type=0)
bot = Bot(command_prefix="!", description=description)

# Load commands
if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    await bot.change_presence(game=playing)

bot.run(t)
