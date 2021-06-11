#imports
from discord.ext import commands
import subprocess
import discord

class example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.exitcode = 0
        

    @commands.command(aliases=["startsmp","smpstart","startserver","server"])
    async def tntserverstart(self, ctx):
        exitcode = self.bot.exitcode
        try:
            exitcode = self.bot.server.poll()
        except: pass
        if exitcode == 0:
            self.bot.server = subprocess.Popen(["bash","start.sh"],cwd="../papermc/")
            print("\a")
            exitcode = 1
            await ctx.send("Server is starting, please wait until server started message appears at <#838308356745330728>")
        else:
            await ctx.send("Server has started. You cannot start the server which is started.")
    @commands.command()
    async def serverlog(self, ctx):
        await ctx.send("update when server start again.")
        await ctx.send(file=discord.File('../papermc/minecraft.log'))

def setup(bot):
    bot.cmdlist["mcserver"] = {
        "intro": "Commands for mcserver.",
        "tntserverstart": "`$tntserverstart`\nStart the minecrat server.\nAliases: `startsmp` `smpstart` `startserver` `server`",
        "serverlog": "`$serverlog`\nExport the server log."
        }
    try:
        E = open("../mcserver/start.sh","r+")
        bot.add_cog(example(bot))
        E.close()
    except:
        print("Warning: Cannot found the server start file! Not going to import cog: mcserver.")
    

    