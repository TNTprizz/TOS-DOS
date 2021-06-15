#imports
import discord
from discord.ext import commands
import asyncio

class error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title="E! You typed in a wrong command!!!",
                                  url="http://tntprizz.zapto.org/dc",
                                  description="Use `$man all` for a list of commands.",
                                  color=discord.Color.red())
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="E! You missed some arguments!",
                                  url="http://tntprizz.zapto.org/dc",
                                  description="You may run `$man <command>` for further help.",
                                  color=discord.Color.red())
        elif isinstance(error, commands.TooManyArguments):
            embed = discord.Embed(title="E! You typed in too many arguments!!",
                                  url="http://tntprizz.zapto.org/dc",
                                  description="You may use `''` to state one argument with blankspace\n"
                                              "or run `$man <command>` for further help.",
                                  color=discord.Color.red())
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="E! You typed in bad argument!",
                                  url="http://tntprizz.zapto.org/dc",
                                  description="You should use the correct arguement\n"
                                              "or run `$man <command>` for further help.",
                                  color=discord.Color.red())
        elif isinstance(error, KeyError):
            embed = discord.Embed(title="E! I am not in the voice channel!!!",
                                  url="http://tntprizz.zapto.org/dc",
                                  description="You should let the bot join voice channel first!\n"
                                              "run `$man music` for further help.",
                                  color=discord.Color.red())
        else:
            embed = discord.Embed(title="E! Something went wrong!",
                                  url="http://tntprizz.zapto.org/dc",
                                  description="try use `$man <command>` for help.",
                                  color=discord.Color.red())
        embed.add_field(name="Debug:",value=str(error))
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(10)
        await ctx.message.add_reaction("❌")
        await msg.delete()

def setup(bot):
    bot.add_cog(error(bot))
    