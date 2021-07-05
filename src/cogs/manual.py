# Imports
from discord.ext import commands
import discord
# A class called manual is going to be imported as a discord cog 
class manual(commands.Cog): # Showing that it is a discord cog object
    def __init__(self, bot): # Import the bot
        self.bot = bot # self.bot -> bot
    
    # The Manual command ($man <arguments>)
    @commands.command(aliases = ["?", "manual", "help"])
    async def man(self, ctx, *cmds):
        try: # Try to get the prefix of the current server
            prefix = self.bot.custom_prefixes[ctx.guild.id][0]
        except:
            prefix = "$"
        bot = self.bot # Variable shortcut
        if len(cmds) == 0 or cmds[0] == "Cogs": # If no arguments are provided
            cmdlist = bot.cmdlist # Get the global command list
            cogs = bot.cmdlist.keys() # Get a list of the imported cogs with command
            embed = discord.Embed( # Make the embed object
                title="Manual",
                description="```\n/Manual/*```",
                color=discord.Color.blue()
                )
            for cogname in cogs: # Get all the cog name
                try:
                    E = cmdlist[cogname] # Check if the cogname exists
                    embed.add_field(name=cogname, value=cmdlist[cogname]['intro'], inline=True) # Add field to the embed
                except KeyError():
                    pass
            embed.set_footer(text="Prefix of this bot in this server: [" + prefix + "]") # Set the footer to the prefix of the bot of this server
            await ctx.send(embed=embed) # Export the embed
        elif cmds[0] == "all": # If the argument is all
            cmdlist = bot.cmdlist # Get the command list
            cogs = bot.cmdlist.keys() # Get the cog list
            embed = discord.Embed( # Make an embed object
                title="Manual",
                description="```\nManual/Cogs/*/*/```",
                color=discord.Color.blue()
                )
            for cogname in cogs: # List all the cogs out
                try:
                    E = cmdlist[cogname] # Check if the cogname exists
                    cmds = cmdlist[cogname].keys() # Get all the commands of the cogs
                    cmdstr = "" # Declare a command string
                    for cmdname in cmds: # List all the commands out
                        if cmdname != "intro": # Ignore the intro category
                            cmdstr = cmdstr + "`" + cmdname + "` " # Append the command to the command string
                    embed.add_field(name=cogname, value=cmdstr, inline=False) # Add field to the embed
                except KeyError(): # If the cogname don't exist
                    pass # Do nothing
            embed.set_footer(text="Prefix of this bot in this server: [" + prefix + "]") # Set footer to the prefix of this server
            await ctx.send(embed=embed) # Export the embed table
        else: # If what user inserted is anything else
            cmdlist = bot.cmdlist # Get the command list first
            cogs = cmdlist.keys() # Get the cognames
            for name in cogs: # List all the cogs of the bot
                if name == cmds[0]: # If argument is the cogname
                    embed = discord.Embed( # Make an embed object
                        title="Manual",
                        description="```\n/Manual/Cogs/" + name + "/```",
                        color=discord.Color.blue()
                        )
                    cmdstr = "" # Declare a command string
                    for content in cmdlist[name].keys(): # Get all the commands of the cog
                        if content != "intro": # Ignore the intro category
                            cmdstr = cmdstr + "`" + content + "` " # Append them to the string
                    embed.add_field(name=name, value=cmdlist[name]["intro"] + "\n**Commands**:\n" + cmdstr) # Add field to the embed
                    embed.set_footer(text="Prefix of this bot in this server: [" + prefix + "]") # Set footer to the prefix of this server
                    await ctx.send(embed=embed) # Export the embed table
                    return # Terminate the function
            for cogname in cogs: # List all the cogs of the bot
                command = cmdlist[cogname].keys() # Get the command list
                for cmdname in command: # Get all the commands from the command list
                    if cmdname != "intro" and cmdname == cmds[0]: # If argument is not intro and is the command name
                        embed = discord.Embed( # Make an embed object
                            title="Manual",
                            description="```\n/Manual/Cogs/" + cogname + "/" + cmdname + "/```",
                            color=discord.Color.blue()
                            )
                        help = cmdlist[cogname][cmdname] # Get the help content
                        embed.add_field(name=cmdname,value=help) # Add the field about the command
                        embed.set_footer(text="Prefix of this bot in this server: [" + prefix + "]") # Set footer to the prefix of the bot in the server
                        await ctx.send(embed=embed) # Export the embed table
                        return # Terminate the function
            embed = discord.Embed( # Create the embed object about command not found
                title="Manual",
                description="```\nError: " + cmds[0] + ": No such File or directory```\nCommand or cogs not founded.\nUse `$man all` to get a list of commands.",
                color=discord.Color.red())
            embed.set_footer(text="Prefix of this bot in this server: `" + prefix + "`") # Set footer to the prefix of this server
            await ctx.send(embed=embed) # Export the embed object

def setup(bot): # Do this when cog loaded
    bot.cmdlist["manual"] = { # manual for manual commands
        "intro": "Manual, which is the helping system.",
        "man": "`man (*Arguments)`\nThis is the manual system.\nUsage:\n"
        "`man all`: list all the commands of the loaded cogs\n"
        "`man <cog>`: print out the imformation of the cog\n"
        "`man <command>`: print out the imformation of the command\n"
        "Aliases: `help` `?` `manual`"
        }
    bot.add_cog(manual(bot)) # Add the cog into the bot
    
