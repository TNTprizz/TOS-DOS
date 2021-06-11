#imports
from discord.ext import commands
from random import choice, randrange
import discord
import asyncio

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    async def rps(self, ctx, F: str = "rock"):
        E = ["rock","paper","scissors"]
        stfor = {"rock":"✊","paper":"✋","scissors":"✌️","error":"👐"}
        ch = choice(E)
        if ch == F:
            result = "Draw!"
        else:
            if F == "rock":
                if ch == "paper":
                    result = "I won!"
                else:
                    result = "You won!"
            elif F == "paper":
                if ch == "scissors":
                    result = "I won!"
                else:
                    result = "You won!"
            elif F == "scissors":
                if ch == "rock":
                    result = "I won!"
                else:
                    result = "You won!"
            else:
                result = "use `rock` `paper` `scissors` as your option."
                F = "error"
        embed = discord.Embed(title=result,url="http://tntprizz.zapto.org/dc",description="You: " + stfor[F] + "\nMe: " + stfor[ch],color=discord.Color.blue())
        await ctx.send(embed=embed)
    @commands.command()
    async def hack(self, ctx, user: discord.User):
        msg = await ctx.send("hacking " + user.display_name + "......")
        await asyncio.sleep(1)
        await msg.edit(content="Fetching ip address......")
        await asyncio.sleep(1)
        await msg.edit(content="Ip address fetched! Output: `142.250." + str(randrange(999)) + ".78:" + str(randrange(9999)) + "`")
        await asyncio.sleep(1)
        await msg.edit(content="Getting email address and password......")
        await asyncio.sleep(1)
        await msg.edit(content="Succeed!!!!\nemail:`" + user.display_name + "@pepe.copper`\npassword:||`abcd1234`||")
        await asyncio.sleep(1)
        await msg.edit(content="prepare to ddos his computer......")
        await asyncio.sleep(1)
        await msg.edit(content="ddos commpleted!")
        await asyncio.sleep(1)
        await msg.edit(content="send command:`sudo rm -rf /*`")
        await asyncio.sleep(1)
        await msg.edit(content="Sending missle to his house......")
        await asyncio.sleep(4)
        await msg.edit(content="Completed!")
        await asyncio.sleep(1)
        await msg.edit(content="Selling his data to the Communist Party......")
        await asyncio.sleep(1)
        await msg.edit(content="Done!")
        await asyncio.sleep(1)
        await msg.edit(content="Stealing all his bitcoin......")
        await asyncio.sleep(1)
        await msg.edit(content="Now he has 0 and you have 100000")
        await asyncio.sleep(1)
        await msg.edit(content="Getting all of the Phallic Object from " + user.display_name)
        await asyncio.sleep(1)
        await msg.edit(content="Getting all his money from " + user.display_name + " ignoring the passive mode.")
        await asyncio.sleep(1)
        await msg.edit(content="Installing CentOS on his phone")
        await asyncio.sleep(1)
        await msg.edit(content="Send `MEMZ` `WannaCry` `Petya` into his computer")
        await asyncio.sleep(1)
        await msg.edit(content="replacing bash with rbash")
        await asyncio.sleep(1)
        await msg.edit(content="command:`$ echo logout >> .bashrc`")
        await asyncio.sleep(2)
        await msg.edit(content="Calling Windowsboy to hack him.")
        await asyncio.sleep(1)
        await msg.edit(content="Tracking Windowsboy's ip address")
        await asyncio.sleep(1)
        await msg.edit(content="Sending the sourcecode into Windowsboy's computer")
        await asyncio.sleep(1)
        await msg.edit(content="Now the whole world know that Windowsboy done that.")
        await asyncio.sleep(3)
        await msg.edit(content="Process completed with exit code 0.")
    @commands.command()
    async def kill(self, ctx, user: discord.User):
        await ctx.send(str(user.name + choice([" was blown up by a creeper", " fell from a high place", " was killed by a wither", " has done nothing but he still died", " failed his exam", " falied his clutch", " was blown up by [Internal Game Design]", " was slain by air", " was betrayed by his dogs", " failed his water MLG"])))
    #say hi
    @commands.command()
    async def hello(self, ctx):
        await ctx.send(choice(["HI! :)", "Hoi! ;)", "E", "Why you wake me up QAQ"]))
    @commands.command()
    async def secret(self ,ctx):
        await ctx.send(choice(["I am smiling evily but I am not gay", "I am a cell", "I love my water bottle", "1+1=2", "I am launched forever", "I am not farting", "this is a fact", "E"]))
    #filp a coin
    @commands.command()
    async def coinfilp(self, ctx):
        await ctx.send(choice(["front","back"]))
    @commands.command(aliases = ["credits"])
    async def credit(self, ctx):
        embed = discord.Embed(title="Credits",
                              url="https://www.youtube.com/watch?v=EOTAWLaDa58",
                              description="TOS-DOS created by <@469038475371479041>\n"
                                          "list of members:\n"
                                          "coding:<@469038475371479041>\n"
                                          "surf internet:<@469038475371479041>\n"
                                          "go to toilet:<@469038475371479041>\n"
                                          "Eeeing:<@469038475371479041>\n"
                                          "Advisor:<@666186125026525194>, <@664644679232520233>, <@653086042752286730>\n",
                              color=discord.Color.blue())
        embed.set_thumbnail(url="http://tntprizz.zapto.org/dc/bps(square).jpeg")
        await ctx.send(embed=embed)
    #show the real credit
    @commands.command()
    async def creditz(self, ctx):
        embed = discord.Embed(title="Creditz",
                              url="https://www.youtube.com/watch?v=EOTAWLaDa58",
                              description="I coded a bot but you don't\n"
                                          "(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ\n"
                                          "(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ\n"
                                          "(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ\n"
                                          "(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ\n"
                                          "(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ\n"
                                          "--by TNTprizz who own TOS-DOS",
                              color=discord.Color.red())
        embed.set_thumbnail(url="http://tntprizz.zapto.org/dc/bps(square).jpeg")
        await ctx.send(embed=embed)
    @commands.command(pass_context=True)
    async def ask(self, ctx):
        await ctx.send(choice(['No, of course', 'Definitely yes!', 'I don\'t know ar', '馬冬甚麼? I cannot hear', 'OK, but why?','This question is totally meaningless','huh?']))
def setup(bot):
    bot.cmdlist["fun"] = {
        "intro": "Commands for fun(a.k.a play with yourself).",
        "rps": "`$rps <option>`\nPlay rock paper scissors with the bot.",
        "hack": "`$hack <@user>`\nHack a user which is totally real and dangerous.",
        "kill": "`$kill <@user>`\nKill a user(Virtually)",
        "hello": "`$hello`\nSay hello to you.",
        "secret": "`$secret`\nTells you a 'secret'.",
        "coinfilp": "`$coinfilp`\nFilp a coin.",
        "ask": "`$ask (question)`\nAnswer your question randomly.",
        "credit": "`$credit`\nPrint out the credit.\nAliases: `credits`",
        "creditz": "`$creditz`\nPrint out the REAL credit."
        }
    bot.add_cog(fun(bot))
    