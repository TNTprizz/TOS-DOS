#imports
from gpiozero import CPUTemperature
import psutil
from discord.ext import commands
import discord
import asyncio

class bash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    async def sourcecode(self, ctx):
        await ctx.send(embed = discord.Embed(title="source code link:",url="https://github.com/TNTprizz/TOS-DOS",description="[Github](https://github.com/TNTprizz/TOS-DOS)\nUpdate unevenly",color=discord.Color.blue()))
    @commands.command(aliases=["profile"])
    async def aboutme(self, ctx):
        mention = []
        user = ctx.author
        try:
            act = user.activities[0].name
        except Exception:
            act = "Unknown or not defined."
        status = str(user.status)
        if status == "dnd":
            status = "Do not disturb"
        elif status == "idle":
            status = "AFK"
        if str(act) == None:
            act = "no activity."
        try:
            for role in user.roles:
                if role.name != "@everyone":
                    mention.append(role.mention)
            b = ", ".join(mention)
            trole = user.top_role
            if user.top_role == None:
                trole = "no role"
        except Exception():
            b = "no role."
            trole = "no role."
        embed = discord.Embed(title=user.name + "'s profile",
                            url="http://tntprizz.zapto.org/dc",
                            description="",
                            color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar_url) # this thanks @two slices of cucumber that gives me the user icon method.
        embed.add_field(name="User display name",value=user.display_name)
        embed.add_field(name="User mention",value=user.mention)
        embed.add_field(name="User ID",value=user.id)
        embed.add_field(name="User activity",value=act)
        embed.add_field(name="User status",value=status)
        try:
            embed.add_field(name="User top role", value=trole,inline=False)
            embed.add_field(name="User roles",value=b)
        except:
            embed.add_field(name="User roles", value="You have no role! What a shame.", inline=False)
        await ctx.send(embed=embed)
    @commands.command()
    async def about(self, ctx, user = "bot"):
        cputemp = CPUTemperature()
        temp = str(cputemp.temperature)
        usage = str(psutil.cpu_percent(interval=0.3))
        memory = psutil.virtual_memory().percent
        used = round(memory / 100 * 7629, 3)
        if user == "bot":
            embed = discord.Embed(title="about TOS-DOS:",
                            url="http://TNTprizz.zapto.org/dc",
                            description="about open sourced TOS-DOS",
                            color=discord.Color.gold())
            embed.add_field(name="author",value="TNTprizz80315#6093",inline=True)
            embed.add_field(name="name",value="TOS-DOS(TNTprizz operating server - Don't operate system)",inline=True)
            embed.add_field(name="version",value=self.bot.ver,inline=True)
            embed.add_field(name="stage",value="Cogs",inline=True)
            embed.add_field(name="status",value="running",inline=True)
            embed.add_field(name="source",value="run `$sourcecode` to get the link", inline=True)
            embed.add_field(name="CPU:",value="Temperature: " + temp + "°C\n" + "Usage: " + usage + "%")
            embed.add_field(name="RAM:",value="Used: " + str(used) + "/7629.395 MiB\n" + "Percent: " + str(memory) + "%")
            await ctx.send(embed=embed)
        else:
            converter = discord.ext.commands.MemberConverter()
            user = await converter.convert(ctx, user)
            try:
                act = user.activities[0].name
            except Exception:
                act = "Unknown or not defined."
            status = str(user.status)
            if status == "dnd":
                status = "Do not disturb"
            elif status == "idle":
                status = "AFK"
            if str(act) == None:
                act = "no activity."
            mention = []
            for role in user.roles:
                if role.name != "@everyone":
                    mention.append(role.mention)
            b = ", ".join(mention)
            embed = discord.Embed(title=user.name + "'s profile",
                                url="http://tntprizz.zapto.org/dc",
                                description="",
                                color=discord.Color.blue())
            embed.set_thumbnail(url=user.avatar_url) # this thanks @two slices of cucumber that gives me the user icon method.
            embed.add_field(name="User display name",value=user.display_name)
            embed.add_field(name="User mention",value=user.mention)
            embed.add_field(name="User ID",value=user.id)
            embed.add_field(name="User activity",value=act)
            embed.add_field(name="User status",value=status)
            try:
                embed.add_field(name="User top roles", value=user.top_role,inline=False)
                embed.add_field(name="User roles",value=b)
            except:
                embed.add_field(name="User roles", value="This user has no role! What a shame.", inline=False)
            await ctx.send(embed=embed)
    @commands.command()
    async def secho(self, ctx, user: discord.User,* , args: str):
        await user.send(args)
        await ctx.send("secho executed successfully.")
    @commands.command()
    async def version(self, ctx):
        await ctx.send("version: " + self.bot.ver)
    @commands.command(pass_context=True)
    async def embed(self, ctx, title: str, con: str):
        embed = discord.Embed(title=title,
                              url="http://tntprizz.zapto.org/dc",
                              description=con,
                              color=discord.Color.blue())
        await ctx.send(embed=embed)
    @commands.command()
    async def dembed(self, ctx, title: str, con: str):
        embed = discord.Embed(title=title,
                              url="http://tntprizz.zapto.org/dc",
                              description=con,
                              color=discord.Color.blue())
        await ctx.send(embed=embed)
        await ctx.message.delete()
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('**$pong**')
        await ctx.send('latency = ' + str(round(self.bot.latency * 1000)) + 'ms')
    @commands.command()
    async def pong(self, ctx):
        await ctx.send('**$ping**')
        await ctx.send('latency = ' + str(round(self.bot.latency * 1000)) + 'ms')
    @commands.command()
    async def echo(self, ctx,* ,echoed: str):
        await ctx.send(echoed)
    @commands.command(aliases = ["rolecheck", "checkrole"])
    async def whoamirole(self, ctx):
        mention = []
        user = ctx.author
        for role in user.roles:
            if role.name != "@everyone":
                mention.append(role.mention)
        b = ", ".join(mention)
        embed = discord.Embed(title="Info:", description=f"Info of: {user.mention}", color=discord.Color.orange())
        embed.add_field(name="Top role:", value=user.top_role)
        embed.add_field(name="Roles:", value=b)
        await ctx.send(embed=embed)
    @commands.command(pass_content=True)
    async def whoami(self, ctx):
        await ctx.send(ctx.message.author.mention)
    @commands.command(pass_content=True)
    async def whoamid(self, ctx):
        await ctx.send(ctx.message.author.id)
    @commands.command()
    async def temp(self, ctx):
        await asyncio.sleep(2)
        await ctx.message.delete()
    @commands.command()
    async def decho(self, ctx, echoed):
        await ctx.send(echoed)
        await ctx.message.delete()
    @commands.command(aliases=["image"])
    async def echoimage(self, ctx, *url: str):
        embed = discord.Embed(title="  ",
                             url="http://tntprizz.zapto.org/dc",
                              color=discord.Color.blue())
        url1 = " ".join(url)
        embed.set_image(url=url1)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    @commands.command()
    @commands.has_role("Administrator")
    async def purge(self, ctx, limit:int):
        await ctx.channel.purge(limit=limit)
    @commands.command()
    @commands.has_role("Administrator")
    async def eembed(self ,ctx, messageid: int, title: str, content: str):
        try:
            msg = await ctx.fetch_message(messageid)
            await msg.edit(embed=discord.Embed(title=title,url="http://tntprizz.zapto.org/dc",description=content,color=discord.Color.blue()))
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction("❌")
    @commands.command()
    @commands.has_role("Administrator")
    async def areact(self, ctx, messageid: int, emoji):
        try:
            await ctx.message.delete()
            msg = await ctx.fetch_message(messageid)
            await msg.add_reaction(emoji)
        except:
            await ctx.message.add_reaction("❌")
    @commands.command()
    @commands.has_role("Administrator")
    async def eecho(self, ctx, messageid: int, *content):
        try:
            content = " ".join(content)
            msg = await ctx.fetch_message(messageid)
            await msg.edit(content=content)
            await ctx.message.delete()
        except:
            await ctx.message.add_reaction("❌")
def setup(bot):
    bot.cmdlist["bash"] = {
        "intro": "Basically some basic commands.",
        "version": "Print out the version of this bot.",
        "sourcecode": "`$sourcecode`\nPrint out the source code.",
        "aboutme": "`$aboutme`\nPrint out the profile of the author.",
        "about": "`$about <@user>`\nPrint out the profile of the mentioned user.",
        "embed": "`$embed <title> <content>`\nExport an embed table with the given title and content",
        "dembed": "`$dembed <title> <content>`\nExport an embed table with the given title and content but delete the command message.",
        "eembed": "`$eembed <messageid> <title> <content> [Administrator]`\nOverwrite the message with message id with the embed table.",
        "echo": "`$echo <content>`\nPrint out the content.",
        "decho": "`$decho <content>`\nPrint out the content but delete the command message.",
        "eecho": "`$eecho <messageid> <title> <content> [Administrator]`\nOverwrite the message with message id with the embed table.",
        "secho": "`$secho <@user> <content>`\nSend a DM to the specified user.",
        "echoimage": "`$echoimage <url>`\nExport an embed table with the image.",
        "ping": "`$ping`\nPrint out `pong` and return the latency of the bot.",
        "pong": "`$pong`\nPrint out `ping` and return the latency of the bot.",
        "whoami": "`$whoami`\nPrint out your mention.",
        "whoamid": "`$whoamid`\nPrint out your user id.",
        "whoamirole": "`$whoamid`\nExport all your roles.",
        "temp": "`$temp`\nDelete the command message after 2 seconds.",
        "purge": "`$purge <number of message> [Administrator]`\nPurge numbers of message.",
        "areact": "`$areact <messageid> <emoji>`\nMake the bot react the message using id with the emoji."
        }
    bot.add_cog(bash(bot))
    