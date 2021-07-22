# Imports
import discord
from discord.ext import commands
import asyncio
import time

def nowtime():
    return time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
# A new class called error is ready to import as a cog
class error(commands.Cog): # Discord cog object
    def __init__(self, bot): # Import the bot
        self.bot = bot # self.bot -> bot
    # Listener which detect command error
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound): # If the command typed in is not founded
            embed = discord.Embed( # Create the embed object
                title="E! You typed in a wrong command!!!",
                url="http://tntprizz.zapto.org/dc",
                description="Use `$man all` for a list of commands.",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.MissingRequiredArgument): # If arguments are missing in a command
            embed = discord.Embed( # Create the embed object
                title="E! You missed some arguments!",
                url="http://tntprizz.zapto.org/dc",
                description="You may run `$man <command>` for further help.",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.BadArgument): # If arguments don't satisfy the requirement
            embed = discord.Embed(
                title="E! You typed in bad argument!",
                url="http://tntprizz.zapto.org/dc",
                description="You should use the correct arguement\nor run `$man <command>` for further help.",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.MissingPermissions): # If permission denieded
            embed = discord.Embed( # Create the embed object
                title="E! Permissions DENIED!",
                url="http://tntprizz.zapto.org/dc",
                description="You don't have the permission to run this command.\nRefer to `$man admin` for further help if you are an Administrator.",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.TooManyArguments):
            embed = discord.Embed( # Create the embed object
                title="E! Too may arguments!",
                url="http://tntprizz.zapto.org/dc",
                description="You typed in too many arguments\nUse `$man [command]` for help",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed( # Create the embed object
                title="E! You are not sudoers of the bot!",
                url="http://tntprizz.zapto.org/dc",
                description="This command is only for the sudoers of this bot,\nShould there be any questions, contact <@469038475371479041>",
                color=discord.Color.red()
            )
        elif isinstance(error, (commands.BotMissingAnyRole, commands.BotMissingPermissions, commands.BotMissingRole)):
            embed = discord.Embed( # Create the embed object
                title="E! I don't have permissions to do that!",
                url="http://tntprizz.zapto.org/dc",
                description="The bot don't have permissions to do the commands.\nShould there be any questions, contact the server owner/moderator/admins",
                color=discord.Color.red()
            )
        else: # If the error cannot be defined
            embed = discord.Embed(
                title="E! Something went wrong!",
                url="http://tntprizz.zapto.org/dc",
                description="try use `$man [command]` for help.\nIf you think that this is an issue of the bot, report the issue [here](https://github.com/TNTprizz/TOS-DOS/issues).",
                color=discord.Color.red()
            )
        embed.add_field( # Add a field showing the traceback
            name="Traceback:",
            value="```\n" + str(error) + "```"
            )
        print(nowtime() + "\033[1;37;41m Error \033[1;31;40m Command error: "+ str(error) +"\033[1;37;40m")
        try:
            msg = await ctx.send(embed=embed) # Export the embed
        except:
            return
        await asyncio.sleep(10) # Sleep for 10 seconds
        try:
            await msg.delete() # Try to delete the error message
            await ctx.message.add_reaction("❌") # Reacterror
        except: pass

def setup(bot):
    bot.add_cog(error(bot))
    