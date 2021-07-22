"""
For vote/poll events
~TNTprizz

format of bot.tfvote:
{
    msgid:
        [0,0,title,content]
}
format of bot.mvote:
{
    msgid:
        {
            number:
                [0,0,0,0,0]
            options:
                [opt1,opt2,opt3,opt4]
            title:
                ""
            content:
                ""
        }
}
"""
import discord
from discord.ext import commands

mvotelist = "🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹"
tfvotelist = "✅❎"

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji.name
        messageid = payload.message_id
        try:
            self.bot.tfvote[messageid][tfvotelist.index(emoji)] += 1
        except:
            try:
                self.bot.mvote[messageid]["count"][mvotelist.index(emoji)] += 1
            except: pass
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji = payload.emoji.name
        messageid = payload.message_id
        try:
            self.bot.tfvote[messageid][tfvotelist.index(emoji)] -= 1
        except:
            try:
                self.bot.mvote[messageid]["count"][mvotelist.index(emoji)] -= 1
            except: pass

    @commands.command(aliases=["vote"])
    async def poll(self, ctx, title: str, content: str, *args):
        loademb = discord.Embed(
            title="Processing, please wait.",
            color=discord.Color.gold()
        )
        msg = await ctx.send(embed = loademb)
        if len(args) == 0:
            self.bot.tfvote[msg.id] = [-1, -1 , title, content]
            await msg.add_reaction("✅")
            await msg.add_reaction("❎")
            emb = discord.Embed(
                title=title,
                description=content,
                color=discord.Color.gold()
            )
        else:
            self.bot.mvote[msg.id] = {"count":[], "options":[], "title":title, "content":content}
            counta = 0
            options = ""
            for opts in args:
                self.bot.mvote[msg.id]["count"].append(-1)
                self.bot.mvote[msg.id]["options"].append(opts)
                await msg.add_reaction(mvotelist[counta])
                options = options + "\n" + mvotelist[counta] + ": " + self.bot.mvote[msg.id]["options"][counta]
                counta += 1
            emb = discord.Embed(
                title=title,
                description=content + options,
                color=discord.Color.gold()
            )
        emb.set_footer(text="Message id: " + str(msg.id))
        await msg.edit(embed = emb)
    @commands.command(aliases=["endvote"])
    async def endpoll(self, ctx, messageid: int):
        msg = await ctx.fetch_message(messageid)
        try:
            con = "✅: " + str(self.bot.tfvote[messageid][0]) + "\n❎: " + str(self.bot.tfvote[messageid][1])
            emb = discord.Embed(
                title="Poll event ended!",
                description="> " + self.bot.tfvote[messageid][2] + "\n```\n" + self.bot.tfvote[messageid][3] + "\n```\n" + con,
                color=discord.Color.gold()
            )
            del self.bot.tfvote[messageid]
        except:
            try:
                counta = 0
                con = ""
                for options in self.bot.mvote[messageid]["count"]:
                    con = con + str(mvotelist[counta]) + ": " + self.bot.mvote[messageid]["options"][counta] + ": \n> " + str(options) + "\n"
                    counta += 1
                emb = discord.Embed(
                    title="Poll event ended!",
                    description="> " + self.bot.mvote[messageid]["title"] + "\n```\n" + self.bot.mvote[messageid]["content"] + "\n```\n" + con,
                    color=discord.Color.gold()
                )
                del self.bot.mvote[messageid]
            except:
                raise commands.BadArgument("'" + str(messageid) + "' is not a valid message id")
        for r in msg.reactions:
            await msg.clear_reaction(r.emoji)
        await msg.add_reaction("🛑")
        await msg.reply(embed = emb)

def setup(bot):
    bot.cmdlist["voteevent"] = {
        "intro": "Voting events",
        "poll": "`poll <title> <content> [*arguments]`\nStart a poll event with embed title and content\nIf no arguments then true and false event\nIf there are arguments then multipoll event\nAliases: `vote`",
        "endpoll": "`endpoll <messageid>`\nEnd a poll event with the poll event's message id.\nAliases: `endvote`"
    }
    bot.tfvote = {}
    bot.mvote = {}
    bot.add_cog(Vote(bot))
