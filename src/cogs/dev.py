# Imports
import discord
from gpiozero import CPUTemperature
from discord.ext import commands
from io import StringIO
from contextlib import redirect_stdout
import os
import time

def nowtime():
    return time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())

# A new class called dev is ready to import as a cog
class dev(commands.Cog): # Show that it is a discord Cog object
    def __init__(self, bot): # Import the bot
        self.bot = bot # self.bot -> bot
    # List the cogs of the bot
    @commands.command(pass_context=True)
    async def lscog(self, ctx):
        embed = discord.Embed( # Create an embed object
            title="Founded cogs of this bot",
            color=discord.Color.blue()
        )
        for filename in os.listdir('./cogs'): # List all the cogs in the directory
            if filename.endswith('.py'): # If it is a python file
                status = "" # Declare a string
                try: # Try to do
                    self.bot.load_extension("cogs." + filename[:-3]) # Load the extension
                    del self.bot.cmdlist[filename[:-3]] # Delete the cog from the command list
                    self.bot.unload_extension("cogs." + filename[:-3]) # Unload the extension
                    status = "Inactive" # Set status to inactive
                except commands.ExtensionAlreadyLoaded: # If extension in line 24 is already loaded
                    status = "Active" # Set status to active
                except: # Else, it must be an error for the cog
                    status = "Error" # Set status to error
                embed.add_field( # Add field for the embed object
                    name=filename[:-3],
                    value="`" + filename + "` - " + status,
                    inline=True
                )
        # Export the embed object
        await ctx.send(embed=embed)
    # Unload a cog ($rmcog <cogname>)
    @commands.command(pass_context=True, aliases=["unloadcog"])
    async def rmcog(self, ctx, cogname: str):
        if not ctx.author.id in self.bot.config["sudoers"]: # If author is not sudoers
            raise commands.NotOwner("You are not sudoers") # Raise exception
        if cogname == "dev": # If trying to unload the dev cog
            raise Exception("The process is unrecoverable")
        self.bot.unload_extension("cogs." + cogname) # Unload the cog
        try: # Try to do
            del self.bot.cmdlist[cogname] # Remove the command from the command list
        except: pass
        print(nowtime() + "\033[1;37;43m Sys   \033[1;32;40m Unloaded cog " + cogname + "\033[1;37;40m")
        await ctx.message.add_reaction("☑️") # Reactsuccess
    # Load a cog ($loadcog <cogname>)
    @commands.command(pass_context=True, aliases=["addcog"])
    async def loadcog(self, ctx, cogname: str):
        if not ctx.author.id in self.bot.config["sudoers"]: # If author is not sudoers
            raise commands.NotOwner("You are not sudoers") # Raise exception
        self.bot.load_extension("cogs." + cogname) # Load the cog
        print(nowtime() + "\033[1;37;43m Sys   \033[1;32;40m Loaded cog " + cogname + "\033[1;37;40m")
        await ctx.message.add_reaction("☑️") # Reactsuccess
    # Reload a cog ($reloadcog <cogname>)
    @commands.command(pass_context=True)
    async def reloadcog(self, ctx, cogname: str):
        if not ctx.author.id in self.bot.config["sudoers"]: # If author is not sudoers
            raise commands.NotOwner("You are not sudoers") # Raise exception
        self.bot.unload_extension("cogs." + cogname) # Unload the extension
        self.bot.load_extension("cogs." + cogname) # Load the extension
        print(nowtime() + "\033[1;37;43m Sys   \033[1;32;40m Reloaded cog " + cogname + "\033[1;37;40m")
        await ctx.message.add_reaction("☑️") # Reactsuccess
    # Check the cpu temperature ($temperature)
    @commands.command(aliases=["CPU","cpu","cputemperature","CPUtemperature"])
    async def temperature(self, ctx):
        cputemp = CPUTemperature() # Get the CPUtemperature object
        temp = str(cputemp.temperature) # Get the cpu temperature and convert it to string
        await ctx.send("CPU temperature = " + temp + "'C") # Print out the temperature
    # Execute python code ($execute <santax textbox string>)
    @commands.command(aliases=["exec","exe"])
    async def execute(self, ctx, *, code:str):
        if not ctx.author.id in self.bot.config["sudoers"]: # If author is not sudoers
            raise commands.NotOwner("You are not sudoers") # Raise exception
        if "```" not in code: # If it is not a santax textbox
            raise commands.BadArgument("Not a santax textbox") # Raise exception
        try: # Try to do
            code = code.split("```")[1].split("py")[1] # Get the pure code from the santax textbox
        except: # If it cannot
            code = code.split("```")[1] # Get the pure code from the santax textbox, but without py
        embed = discord.Embed( # Create an embed object
            title="Executing program",
            color=discord.Color.blue(),
            description="🌀🌀🌀Please wait🌀🌀🌀"
        )
        msg = await ctx.send(embed=embed) # Send out the embed object
        try: # Try to do
            output = StringIO() # Get the StringIO object
            with redirect_stdout(output): # Redirect output using the object
                exec(code) # Execute the code
            exitcode = 0 # If successfully executed the code then exitcode = 0
        except Exception as error: # Except exception from the code and catch the error
            exitcode = 1 # exitcode = 1
            exc = error # Catch the error
        if exitcode == 0: # If exit code is 0
            output = output.getvalue() # Get value from the output object
            if output == "": # If output is empty
                output = "There is no Stdout." # State that there is no output
            embed = discord.Embed( # Create an embed object
                title="Process exit with exit code 0.",
                color=discord.Color.green(),
                description="Stdout:\n```\n" + str(output) + "\n```"
            )
            await ctx.message.add_reaction("☑️") # Reactsuccess
        else: # If exit code is 1
            embed = discord.Embed( # Create an embed object
                title="Error occured when executing program!",
                color=discord.Color.red(),
                description="Stderr:\n```\n" + str(exc) + "\n```"
            )
            await ctx.message.add_reaction("❌") # Reacterror
        await msg.edit(embed=embed) # Replace the message with the embed
    # Evaluate
    @commands.command()
    async def eval(self, ctx, *, code:str):
        # Same as line 76 to 88
        if not ctx.author.id in self.bot.config["sudoers"]: # If author is not sudoers
            raise commands.NotOwner("You are not sudoers") # Raise exception
        if "```" not in code:
            raise commands.BadArgument("Not a santax textbox") # Raise exception
        try:
            code = code.split("```")[1].split("py")[1]
        except:
            code = code.split("```")[1]
        embed = discord.Embed(title="Executing program",color=discord.Color.blue(),description="🌀🌀🌀Please wait🌀🌀🌀")
        msg = await ctx.send(embed=embed)
        try:
            result = eval(code) # Evaluate the code
            exitcode = 0 # Exit code become 0
        except Exception as error: # If exception occured
            exc = error
            exitcode = 1 # Exit code become 1
        if exitcode == 0: # If exit code is 0
            if result == "": # If nothing is evaluated
                result = "Nothing evaluated." # Tell the user about that
            embed = discord.Embed( # Create the embed object
                title="Process exit with exit code 0.",
                color=discord.Color.green(),
                description="Result:\n```\n" + str(result) + "\n```"
            )
            await ctx.message.add_reaction("☑️") # Reactsuccess
        else: # If exit code is 1
            embed = discord.Embed( # Create an embed object
                title="Error occured when finding variable!",
                color=discord.Color.red(),
                description="Stderr:\n```\n" + str(exc) + "\n```"
            )
            await ctx.message.add_reaction("❌") # Reacterror
        await msg.edit(embed=embed) # Replace the message with the embed
# Do these when cog loaded
def setup(bot):
    # For manual commands($man)
    bot.cmdlist["dev"] = {
        "intro": "Commands for devs(a.k.a author himself)",
        "lscog": "`lscog`\nList all the cogs founded, and report their status.",
        "rmcog": "`rmcog <cogname> (sudoers)`\nRemove the cog with the cog name.\nAliases: `removecog`",
        "loadcog": "`loadcog <cogname> (sudoers)`\nLoad the cog with the cog name.\nAliases: `addcog`",
        "reloadcog": "`reloadcog <cogname> (sudoers)`\nReload the cog with the cog name.\n",
        "restart": "`restart (sudoers)`\nRestart the bot.",
        "temperature": "`temperature`\nCheck the temperature of the host\nAliases: `CPU` `cpu` `cputemperature` `CPUtemperature`"
    }
    # Add cog into the bot
    bot.add_cog(dev(bot))
    