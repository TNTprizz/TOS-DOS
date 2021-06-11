#imports
from discord.ext import commands
import discord

class example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases = ["?", "manual", "help"])
    async def man(self, ctx, *cmds):
        bot = self.bot
        if len(cmds) == 0 or cmds[0] == "Cogs":
            cmdlist = bot.cmdlist
            cogs = bot.cmdlist.keys()
            embed = discord.Embed(title="Manual", description="Here are the cogs loaded:", color=discord.Color.blue())
            for cogname in cogs:
                try:
                    E = cmdlist[cogname]
                    embed.add_field(name=cogname, value=cmdlist[cogname]['intro'], inline=True)
                except KeyError():
                    pass
            await ctx.send(embed=embed)
        elif cmds[0] == "all":
            cmdlist = bot.cmdlist
            cogs = bot.cmdlist.keys()
            embed = discord.Embed(title="Manual", description="Here are all the commands:", color=discord.Color.blue())
            for cogname in cogs:
                try:
                    E = cmdlist[cogname]
                    cmds = cmdlist[cogname].keys()
                    cmdstr = ""
                    for cmdname in cmds:
                        if cmdname != "intro":
                            cmdstr = cmdstr + "`" + cmdname + "` "
                    embed.add_field(name=cogname, value=cmdstr, inline=False)
                except KeyError():
                    pass
            await ctx.send(embed=embed)
        else:
            cmdlist = bot.cmdlist
            cogs = cmdlist.keys()
            for name in cogs:
                if name == cmds[0]:
                    embed = discord.Embed(title="Manual", description="Here is the cog you are finding:", color=discord.Color.blue())
                    cmdstr = ""
                    for content in cmdlist[name].keys():
                        if content != "intro":
                            cmdstr = cmdstr + "`" + content + "` "
                    embed.add_field(name=name, value=cmdlist[name]["intro"] + "\n**Commands**:\n" + cmdstr)
                    await ctx.send(embed=embed)
                    return
            for cogname in cogs:
                command = cmdlist[cogname].keys()
                for cmdname in command:
                    if cmdname != "intro" and cmdname == cmds[0]:
                        embed = discord.Embed(title="Manual", description="Here is the command you are finding:", color=discord.Color.blue())
                        help = cmdlist[cogname][cmdname]
                        embed.add_field(name=cmdname,value=help)
                        await ctx.send(embed=embed)
                        return
            embed = discord.Embed(title="Manual", description="Well, command or cogs not founded.\nUse `$man all` to get a list of commands.", color=discord.Color.red())
            await ctx.send(embed=embed)
def setup(bot):
    bot.cmdlist["man"] = {
        "intro": "Manual, which is the helping system.",
        "man": "`$man (*Arguments)`\nThis is the manual system.\nUsage:\n"
        "`$man all`: list all the commands of the loaded cogs\n"
        "developing in progress......"
        }
    bot.add_cog(example(bot))
    
