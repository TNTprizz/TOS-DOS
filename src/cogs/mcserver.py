# Imports
from discord.ext import commands
import subprocess
import discord
# A class called mcserver is ready to be imported as a cog
class mcserver(commands.Cog): # Showing that it is a cog object
    def __init__(self, bot): # Import the cog
        self.bot = bot # self.bot -> bot
        bot.exitcode = 0 # Declare the exit code
    # Start the mc server ($tntserverstart)
    @commands.command(aliases=["startsmp","smpstart","startserver","server"])
    async def tntserverstart(self, ctx):
        exitcode = self.bot.exitcode # Get the exit code
        try:
            exitcode = self.bot.server.poll() # Try to get the exit code fro the process
        except: pass
        if exitcode == 0: # If the server isn't started
            self.bot.server = subprocess.Popen(["bash","start.sh"],cwd="../papermc/") # Start a process for the mcserver
            print("\a") # Alert the user
            exitcode = 1 # Set the exit code to 1
            # Announce the user
            await ctx.send("Server is starting, please wait until server started message appears at <#838308356745330728>")
        else: # If the server is started
            raise Exception("Server has started.") # Raise exception
    # Show the server log ($serverlog)
    @commands.command()
    async def serverlog(self, ctx):
        await ctx.send("update when server start again.")
        await ctx.send(file=discord.File('../papermc/minecraft.log')) # Send out the server log file
# Do these when importing the cog
def setup(bot):
    try:
        E = open("../papermc/start.sh","r+") # Try to open the start bash file
        bot.cmdlist["mcserver"] = { # Import the manual list
            "intro": "Commands for mcserver.",
            "tntserverstart": "`tntserverstart`\nStart the minecrat server.\nAliases: `startsmp` `smpstart` `startserver` `server`",
            "serverlog": "`serverlog`\nExport the server log."
        }
        bot.add_cog(mcserver(bot)) # Add the cog into the bot
        E.close() # Close the object if possible
    except: # Or
        raise FileNotFoundError("start.sh") # Raise error
    

    