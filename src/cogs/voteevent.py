#imports
import discord
from discord.ext import commands

class voteevent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.votelist = {}
        bot.multivotelist = {}
        bot.votehuman = {}
        

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        bot = self.bot
        votelist = bot.votelist
        multivotelist = bot.multivotelist
        emoji = payload.emoji.name
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        try:
            if emoji == "✅":
                votelist[int(message.id)][0] = votelist[int(message.id)][0] + 1
            elif emoji == "❎":
                votelist[int(message.id)][1] = votelist[int(message.id)][1] + 1
        except:
            pass
        try:
            E = multivotelist[int(message.id)]
            if emoji == "1️⃣":
                multivotelist[int(message.id)]["number"][0] = multivotelist[int(message.id)]["number"][0] + 1
            elif emoji == "2️⃣":
                multivotelist[int(message.id)]["number"][1] = multivotelist[int(message.id)]["number"][1] + 1
            elif emoji == "3️⃣":
                multivotelist[int(message.id)]["number"][2] = multivotelist[int(message.id)]["number"][2] + 1
            elif emoji == "4️⃣":
                multivotelist[int(message.id)]["number"][3] = multivotelist[int(message.id)]["number"][3] + 1
            elif emoji == "5️⃣":
                multivotelist[int(message.id)]["number"][4] = multivotelist[int(message.id)]["number"][4] + 1
            elif emoji == "6️⃣":
                multivotelist[int(message.id)]["number"][5] = multivotelist[int(message.id)]["number"][5] + 1
            elif emoji == "7️⃣":
                multivotelist[int(message.id)]["number"][6] = multivotelist[int(message.id)]["number"][6] + 1
            elif emoji == "8️⃣":
                multivotelist[int(message.id)]["number"][7] = multivotelist[int(message.id)]["number"][7] + 1
            elif emoji == "9️⃣":
                multivotelist[int(message.id)]["number"][8] = multivotelist[int(message.id)]["number"][8] + 1
            elif emoji == "🔟":
                multivotelist[int(message.id)]["number"][9] = multivotelist[int(message.id)]["number"][9] + 1
        except:
            pass
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        multivotelist = self.bot.multivotelist
        votelist = self.bot.votelist
        emoji = payload.emoji.name
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        try:
            if emoji == "✅":
                votelist[int(message.id)][0] = votelist[int(message.id)][0] - 1
            elif emoji == "❎":
                votelist[int(message.id)][1] = votelist[int(message.id)][1] - 1
        except:
            pass
        try:
            E = multivotelist[int(message.id)]["number"]
            if emoji == "1️⃣":
                multivotelist[int(message.id)]["number"][0] = multivotelist[int(message.id)]["number"][0] - 1
            elif emoji == "2️⃣":
                multivotelist[int(message.id)]["number"][1] = multivotelist[int(message.id)]["number"][1] - 1
            elif emoji == "3️⃣":
                multivotelist[int(message.id)]["number"][2] = multivotelist[int(message.id)]["number"][2] - 1
            elif emoji == "4️⃣":
                multivotelist[int(message.id)]["number"][3] = multivotelist[int(message.id)]["number"][3] - 1
            elif emoji == "5️⃣":
                multivotelist[int(message.id)]["number"][4] = multivotelist[int(message.id)]["number"][4] - 1
            elif emoji == "6️⃣":
                multivotelist[int(message.id)]["number"][5] = multivotelist[int(message.id)]["number"][5] - 1 
            elif emoji == "7️⃣":
                multivotelist[int(message.id)]["number"][6] = multivotelist[int(message.id)]["number"][6] - 1
            elif emoji == "8️⃣":
                multivotelist[int(message.id)]["number"][7] = multivotelist[int(message.id)]["number"][7] - 1
            elif emoji == "9️⃣":
                multivotelist[int(message.id)]["number"][8] = multivotelist[int(message.id)]["number"][8] - 1
            elif emoji == "🔟":
                multivotelist[int(message.id)]["number"][9] = multivotelist[int(message.id)]["number"][9] - 1
        except:
            pass
    @commands.command()
    async def vote(self, ctx, messageid: int):
        votelist = self.bot.votelist
        await ctx.message.delete()
        msg = await ctx.fetch_message(messageid)
        await msg.add_reaction("✅")
        await msg.add_reaction("❎")
        votelist[messageid] = [0,0]
    @commands.command()
    async def endvote(self, ctx, messageid: int):
        bot = self.bot
        try:
            votelist = bot.votelist
            F = votelist[messageid]
            msg = await ctx.fetch_message(messageid)
            embed = discord.Embed(title="Vote ended!",url="http://TNTprizz.zapto.org/dc",color=discord.Color.blue(),description="✅: " + str(F[0]) + "\n❎: " + str(F[1]) + "\nMessage id:" + str(messageid))
            await msg.reply(embed = embed)
            del votelist[messageid]
            return
        except:
            try:
                arglist = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
                multivotelist = bot.multivotelist
                messageid = int(messageid)
                F = multivotelist[messageid]
                msg = await ctx.fetch_message(messageid)
                await msg.edit(embed=discord.Embed(title="Multivoting event ended!",url="http://TNTprizz.zapto.org/dc",color=discord.Color.blue(),description="This event is expired, better luck next time!"))
                i = 0
                con = ""
                while i != len(multivotelist[messageid]["number"]):
                    con = con + arglist[i] + ":" + str(multivotelist[messageid]["options"][i]) + " : " + str(multivotelist[messageid]["number"][i]) + "\n"
                    i = i + 1
                embed = discord.Embed(title="Multivote ended!",url="http://TNTprizz.zapto.org/dc",color=discord.Color.blue(),description=con + "\nMessage id:" + str(messageid))
                await msg.reply(embed = embed)
                del multivotelist[messageid]
                return
            except:
                await ctx.message.add_reaction("❌")
    @commands.command(aliases=["mvote"])
    async def multivote(self ,ctx, content: str,*args):
        msg = await ctx.send(embed=discord.Embed(title="Loading......",url="http://TNTprizz.zapto.org/dc"))
        if len(args) > 10:
            await ctx.message.add_reaction("❌")
            return
        arglist = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        i = 0
        con = ""
        multivotelist = self.bot.multivotelist
        multivotelist[int(msg.id)] = {"number":[],"options":[]}
        while i != len(args):
            await msg.add_reaction(arglist[i])
            multivotelist[int(msg.id)]["number"].append(-1)
            multivotelist[int(msg.id)]["options"].append(args[i])
            i = i + 1
        i = 0
        while i != len(args):
            con = con + arglist[i] + ":" + args[i] + "\n"
            i = i + 1
        embed = discord.Embed(title=content,url="http://TNTprizz.zapto.org/dc",color=discord.Color.blue(),description=con + "Message ID:" + str(msg.id))
        await msg.edit(embed = embed)
def setup(bot):
    bot.cmdlist["voteevent"] = {
        "intro": "Commands for voting event.",
        "vote": "`$vote <messageid>`\nRaise a voting event on the message with the id provided.",
        "multivote": "`$multivote <title> <*args>`\nRaise a multivoting event with the embed.(max. 10)\nAliases: `mvote`",
        "endvote": "`$endvote <messageid>`\nEnd a voting event with the message id."
        }
    bot.add_cog(voteevent(bot))
    