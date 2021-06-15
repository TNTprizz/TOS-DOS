#imports
import discord
from gpiozero import CPUTemperature
from discord.ext import commands
from io import StringIO
from contextlib import redirect_stdout
import os

class example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def lscog(self ,ctx):
        embed = discord.Embed(title="Founded cogs of this bot",color=discord.Color.blue())
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                status = ""
                try:
                    self.bot.load_extension("cogs." + filename[:-3])
                    self.bot.unload_extension("cogs." + filename[:-3])
                    status = "Inactive"
                except commands.ExtensionAlreadyLoaded:
                    status = "Active"
                except:
                    status = "Error"
                embed.add_field(name=filename[:-3],value="`" + filename + "` - " + status,inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(pass_context=True, aliases=["unloadcog"])
    async def rmcog(self, ctx, cogname: str):
        if ctx.author.id != 469038475371479041:
            await ctx.message.add_reaction("❌")
            return
        try:
            if cogname == "dev":
                await ctx.send("This is unrecoverable! Aborting")
                await ctx.message.add_reaction("❌")
                return
            self.bot.unload_extension("cogs." + cogname)
            try:
                del self.bot.cmdlist[cogname]
            except: pass
            await ctx.message.add_reaction("☑️")
        except:
            await ctx.message.add_reaction("❌")

    @commands.command(pass_context=True, aliases=["addcog"])
    async def loadcog(self, ctx, cogname: str):
        if ctx.author.id != 469038475371479041:
            await ctx.message.add_reaction("❌")
            return
        self.bot.load_extension("cogs." + cogname)
        await ctx.message.add_reaction("☑️")

    @commands.command(pass_context=True)
    async def reloadcog(self, ctx, cogname: str):
        if ctx.author.id != 469038475371479041:
            await ctx.message.add_reaction("❌")
            return
        self.bot.unload_extension("cogs." + cogname)
        self.bot.load_extension("cogs." + cogname)
        await ctx.message.add_reaction("☑️")

    @commands.command(aliases=["CPU","cpu","cputemperature","CPUtemperature"])
    async def temperature(self, ctx):
        cputemp = CPUTemperature()
        temp = str(cputemp.temperature)
        await ctx.send("CPU temperature = " + temp + "'C")
    @commands.command(aliases=["exec","exe"])
    async def execute(self, ctx, *, stuffs: str = "Well, what to execute?"):
        if stuffs == "Well, what to execute?":
            await ctx.send(stuffs)
            await ctx.message.add_reaction("❌")
            return
        if ctx.author.id != 469038475371479041:
            await ctx.message.add_reaction("❌")
            return
        if "```" not in stuffs:
            await ctx.send("well, you should use santax textbox.")
            await ctx.message.add_reaction("❌")
            return
        try:
            stuffs = stuffs.split("```")[1].split("py")[1]
        except:
            stuffs = stuffs.split("```")[1]
        embed = discord.Embed(title="Executing program",color=discord.Color.blue(),description="🌀🌀🌀Please wait🌀🌀🌀")
        msg = await ctx.send(embed=embed)
        try:
            output = StringIO()
            with redirect_stdout(output):
                exec(stuffs)
            exitcode = 0
        except Exception as error:
            exitcode = 1
            exc = error
        if exitcode == 0:
            output = output.getvalue()
            if output == "":
                output = "There is no Stdout."
            embed = discord.Embed(
                title="Process exit with exit code 0.",
                color=discord.Color.green(),
                description="Stdout:\n```\n" + str(output) + "\n```"
            )
            await ctx.message.add_reaction("☑️")
        else:
            embed = discord.Embed(
                title="Error occured when executing program!",
                color=discord.Color.red(),
                description="Stderr:\n```\n" + str(exc) + "\n```"
            )
            await ctx.message.add_reaction("❌")
        await msg.edit(embed=embed)
    @commands.command()
    async def eval(self, ctx, *, stuffs: str = "Well, what to execute?"):
        if stuffs == "Well, what to execute?":
            await ctx.send(stuffs)
            await ctx.message.add_reaction("❌")
            return
        if ctx.author.id != 469038475371479041:
            await ctx.message.add_reaction("❌")
            return
        if "```" not in stuffs:
            await ctx.send("well, you should use santax textbox.")
            await ctx.message.add_reaction("❌")
            return
        try:
            stuffs = stuffs.split("```")[1].split("py")[1]
        except:
            stuffs = stuffs.split("```")[1]
        embed = discord.Embed(title="Executing program",color=discord.Color.blue(),description="🌀🌀🌀Please wait🌀🌀🌀")
        msg = await ctx.send(embed=embed)
        try:
            result = eval(stuffs)
            exitcode = 0
        except Exception as error:
            exc = error
            exitcode = 1
        if exitcode == 0:
            output = result
            if output == "":
                output = "There is no Stdout."
            embed = discord.Embed(
                title="Process exit with exit code 0.",
                color=discord.Color.green(),
                description="Result:\n```\n" + str(output) + "\n```"
            )
            await ctx.message.add_reaction("☑️")
        else:
            embed = discord.Embed(
                title="Error occured when finding variable!",
                color=discord.Color.red(),
                description="Stderr:\n```\n" + str(exc) + "\n```"
            )
            await ctx.message.add_reaction("❌")
        await msg.edit(embed=embed)

def setup(bot):
    bot.cmdlist["dev"] = {
        "intro": "Commands for devs(a.k.a author himself)",
        "lscog": "`$lscog`\nList all the cogs founded, and report their status.",
        "rmcog": "`$rmcog <cogname> [TNTprizz]`\nRemove the cog with the cog name.\nAliases: `removecog`",
        "loadcog": "`$loadcog <cogname> [TNTprizz]`\nLoad the cog with the cog name.\nAliases: `addcog`",
        "reloadcog": "`$reloadcog <cogname> [TNTprizz]`\nReload the cog with the cog name.\n",
        "restart": "`$restart`\nRestart the bot.",
        "temperature": "`$temperature`\nCheck the temperature of the host\nAliases: `CPU` `cpu` `cputemperature` `CPUtemperature`"
        }
    bot.add_cog(example(bot))
    