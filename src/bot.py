#imports
import discord
from discord.ext import commands
from random import choice
import os
import asyncio
import sys

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', help_command=None, intents=intents)
bot.ver = "202106111837-Σ$Cog1"
status = ['E', 'with 1 user', 'games', 'TOS-DOS', 'music', 'cytus2', 'Myself', 'phigros', 'nothing', '$man all', '$ask', 'maths', 'Dancerail3','MEMZ','Cytus','$about','CentOS','kali-linux','PUBG','Ubuntu','java','python','WannaCry']
#very basic things:
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

@bot.command()
async def restart(ctx):
  if ctx.author.id != 469038475371479041:
    await ctx.message.add_reaction("❌")
    return
  await ctx.send("Restarting... Allow up to 5 seconds")
  print("Caught restart command, restarting......")
  restart_program()

@bot.event
async def on_ready():
  while True:
    await bot.change_presence(activity=discord.Game(name=choice(status)))
    await asyncio.sleep(60)

bot.cmdlist = {}
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    print("Loaded cog " + filename[:-3] + " from file: " + filename)
    bot.load_extension(f'cogs.{filename[:-3]}')

print('No santax exception, running')
token = open("../E.key","r+")
bot.run(token.read())
token.close()