#imports
import discord
from discord.ext import commands
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
        try:
            self.bot.load_extension("cogs." + cogname)
            await ctx.message.add_reaction("☑️")
        except:
            await ctx.message.add_reaction("❌")

    @commands.command(pass_context=True)
    async def reloadcog(self, ctx, cogname: str):
        if ctx.author.id != 469038475371479041:
            await ctx.message.add_reaction("❌")
            return
        try:
            self.bot.unload_extension("cogs." + cogname)
            self.bot.load_extension("cogs." + cogname)
            await ctx.message.add_reaction("☑️")
        except:
            await ctx.message.add_reaction("❌")

def setup(bot):
    bot.cmdlist["dev"] = {
        "intro": "Commands for devs(a.k.a author himself)",
        "lscog": "`$lscog`\nList all the cogs founded, and report their status.",
        "rmcog": "`$rmcog <cogname> [TNTprizz]`\nRemove the cog with the cog name.\nAliases: `removecog`",
        "loadcog": "`$loadcog <cogname> [TNTprizz]`\nLoad the cog with the cog name.\nAliases: `addcog`",
        "reloadcog": "`$reloadcog <cogname> [TNTprizz]`\nReload the cog with the cog name."
        }
    bot.add_cog(example(bot))
    