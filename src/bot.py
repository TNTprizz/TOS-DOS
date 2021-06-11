#imports
import discord
from discord.ext import commands
import os

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', help_command=None, intents=intents)
bot.ver = "202106111837-Σ$Cog1"
#very basic things:
@bot.event
async def on_ready():
  while True:
    await bot.change_presence(activity=discord.Game(name="Somethings"))
bot.cmdlist = {}
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    print("Loaded cog " + filename[:-3] + " from file: " + filename)
    bot.load_extension(f'cogs.{filename[:-3]}')

print('No santax exception, running')
token = open("../E.key","r+")
bot.run(token.read())
token.close()