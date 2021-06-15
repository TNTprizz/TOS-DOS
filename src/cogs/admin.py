#imports
import discord
from discord.ext import commands
from discord.utils import get
import ast

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addadmin(self, ctx, *user: discord.User):
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": []}
        for admins in user:
            jdict[str(ctx.guild.id)]["admins"].append(str(admins.id))
        json = open("../data/admin.json","w")
        json.write(str(jdict))
        json.close()
        await ctx.message.add_reaction("☑️")
    @commands.command(aliases = ["adminls"])
    async def lsadmin(self, ctx):
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        con = ""
        for user in jdict[str(ctx.guild.id)]["admins"]:
            con = con + get(ctx.guild.members, id=int(user)).mention + "\n"
        embed = discord.Embed(
            title = "Admins of this server",
            color = discord.Color.blue(),
            description = con
        )
        await ctx.send(embed = embed)
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rmadmin(self, ctx, *user: discord.User):
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": []}
        for admins in user:
            try:
                del jdict[str(ctx.guild.id)]["admins"][jdict[str(ctx.guild.id)]["admins"].index(admins)]
            except:
                await ctx.send(admins.name + " is not an admin before!")
        json = open("../data/admin.json","w")
        json.write(str(jdict))
        json.close()
        await ctx.message.add_reaction("☑️")
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reactrole(self, ctx, title, description, *content):
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": []}
        try:
            E = jdict[str(ctx.guild.id)]["admins"].index(str(ctx.author.id))
        except:
            await ctx.message.add_reaction("❌")
            return
        if description == "" or title == "":
            await ctx.message.add_reaction("❌")
            return
        if len(content) == 0 or (len(content) % 2) != 0:
            await ctx.message.add_reaction("❌")
            return
        if len(content) > 26:
            await ctx.message.add_reaction("❌")
            return
        json = open("../data/auto.json","r")
        rrole = ast.literal_eval(json.read())
        print(str(rrole))
        msg = await ctx.send(embed = discord.Embed(
            title="Configuring......"
        ))
        try:
            E = rrole[str(ctx.guild.id)]
        except:
            rrole[str(ctx.guild.id)] = {}
        rrole[str(ctx.guild.id)][str(msg.id)] = {}
        count = 0
        for con in content:
            if (content.index(con) % 2) == 0:
                await msg.add_reaction(str(con))
            else:
                rrole[str(ctx.guild.id)][str(msg.id)][content[count]] = str(get(ctx.guild.roles, mention=con).id)
                count = count + 1
        embdes = ""
        for emoji in rrole[str(ctx.guild.id)][str(msg.id)]:
            id = rrole[str(ctx.guild.id)][str(msg.id)][emoji]
            emo = str(get(ctx.guild.roles, id=int(id)).mention)
            embdes = embdes + emoji + ": " + emo + "\n"
        embed = discord.Embed(
            title = title,
            description = embdes + "\n" + description,
            color = discord.Color.blue()
        )
        await msg.edit(embed = embed)
        json.close()
        json = open("../data/auto.json","w")
        json.write(str(rrole))
        json.close()
    @commands.command()
    async def warn(self ,ctx, user: discord.User,*reason):
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": []}
        try:
            E = jdict[str(ctx.guild.id)]["admins"].index(str(ctx.author.id))
        except:
            await ctx.message.add_reaction("❌")
            return
        message = await self.bot.get_channel(851784439204675584).fetch_message(851784867066282057)
        channel = message.channel
        reason = " ".join(reason)
        embed = discord.Embed(title=user.name + " is WARNED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nFrom " + ctx.author.mention)
        await ctx.send(embed=embed)
        embed = discord.Embed(title=user.name + " is WARNED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
        await channel.send(embed=embed)
        embed = discord.Embed(title="You are warned",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Reason:" + reason + "\nFrom " + ctx.author.mention)
        await user.send(embed=embed)
    @commands.command()
    async def kick(self ,ctx, user: discord.Member, *reason):
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": []}
        try:
            E = jdict[str(ctx.guild.id)]["admins"].index(str(ctx.author.id))
        except:
            await ctx.message.add_reaction("❌")
            return
        message = await self.bot.get_channel(851784439204675584).fetch_message(851784867066282057)
        channel = message.channel
        reason = " ".join(reason)
        await user.kick(reason=reason)
        embed = discord.Embed(title=user.name + " is KICKED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nFrom " + ctx.author.mention)
        await ctx.send(embed=embed)
        embed = discord.Embed(title=user.name + " is KICKED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
        await channel.send(embed=embed)
        embed = discord.Embed(title="You are kicked",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Reason:" + reason + "\nFrom " + ctx.author.mention)
        await user.send(embed=embed)
    @commands.command()
    async def ban(self , ctx, user: discord.Member, *reason):
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": []}
        try:
            E = jdict[str(ctx.guild.id)]["admins"].index(str(ctx.author.id))
        except:
            await ctx.message.add_reaction("❌")
            return
        message = await self.bot.get_channel(851784439204675584).fetch_message(851784867066282057)
        channel = message.channel
        reason = " ".join(reason)
        await user.ban(reason=reason)
        embed = discord.Embed(title=user.name + " is BANNED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nFrom " + ctx.author.mention)
        await ctx.send(embed=embed)
        embed = discord.Embed(title=user.name + " is BANNED!",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
        await channel.send(embed=embed)
        embed = discord.Embed(title="You are banned",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Reason:" + reason + "\nFrom " + ctx.author.mention)
        await user.send(embed=embed)
    @commands.command()
    async def mute(self, ctx, user: discord.Member, *reason):
        for role in user.roles:
            if role.name != "@everyone":
                await user.remove_roles(role)
        json = open("../data/admin.json","r")
        userlist = ast.literal_eval(json.read())
        json.close()
        try:
            E = userlist[str(ctx.guild.id)]
        except:
            userlist[str(ctx.guild.id)] = {"mutedusers": [], "admins": []}
        for deuser in userlist[str(ctx.guild.id)]["mutedusers"]:
            if user.id == deuser:
                await ctx.send("He is already muted, no worth it man.")
                return
        userlist[str(ctx.guild.id)]["users"].append(user.id)
        json = open("../data/admin.json","w")
        json.write(str(userlist))
        json.close()
        message = await self.bot.get_channel(851784439204675584).fetch_message(851784867066282057)
        channel = message.channel
        reason = " ".join(reason)
        embed = discord.Embed(title=user.name + " is MUTED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nFrom " + ctx.author.mention)
        await ctx.send(embed=embed)
        embed = discord.Embed(title=user.name + " is MUTED!",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
        await channel.send(embed=embed)
        embed = discord.Embed(title="You are muted",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Reason:" + reason + "\nFrom " + ctx.author.mention)
        await user.send(embed=embed)
    @commands.command()
    async def unmute(self, ctx, user: discord.Member):
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": []}
        try:
            E = jdict[str(ctx.guild.id)]["admins"].index(str(ctx.author.id))
        except:
            await ctx.message.add_reaction("❌")
            return
        message = await self.bot.get_channel(851784439204675584).fetch_message(851784867066282057)
        channel = message.channel
        json = open("../data/admin.json","r")
        userlist = ast.literal_eval(json.read())
        json.close()
        for deuser in userlist[str(ctx.guild.id)]["mutedusers"]:
            if user.id == deuser:
                del userlist[str(ctx.guild.id)]["mutedusers"][userlist[str(ctx.guild.id)]["mutedusers"].index(user.id)]
                json = open("../data/admin.json","w")
                json.write(str(userlist))
                json.close()
                guild = user.guild
                await user.add_roles(get(guild.roles, id=800681780834992129))
                embed = discord.Embed(title=user.name + " is UNMUTED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention)
                await ctx.send(embed=embed)
                embed = discord.Embed(title=user.name + " is UNMUTED!",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Thanks for admin's Great Fat Compassion!\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
                await channel.send(embed=embed)
                embed = discord.Embed(title="You are unmuted",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention)
                await user.send(embed=embed)
                return
        await ctx.send("He is not muted, idiot")
    @commands.command()
    async def unban(self, ctx, id):
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": []}
        try:
            E = jdict[str(ctx.guild.id)]["admins"].index(str(ctx.author.id))
        except:
            await ctx.message.add_reaction("❌")
            return
        message = await self.bot.get_channel(851784439204675584).fetch_message(851784867066282057)
        channel = message.channel
        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user)
        embed = discord.Embed(title=user.name + " is UNBANNED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention)
        await ctx.send(embed=embed)
        embed = discord.Embed(title=user.name + " is BANNED!",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Thanks for admin's Great Fat Compassion!\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
        await channel.send(embed=embed)
        embed = discord.Embed(title="You are unbanned",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention)
        await user.send(embed=embed)
    @commands.command()
    async def lsuser(self, ctx):
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": []}
        try:
            E = jdict[str(ctx.guild.id)]["admins"]
            E.index(str(ctx.author.id))
        except:
            await ctx.message.add_reaction("❌")
            return
        listuser = ""
        for user in ctx.guild.members:
            listuser = listuser + user.mention + " ,"
        await ctx.send(embed = discord.Embed(
            title="Users in this server:",color=discord.Color.blue(),description=listuser
        ))
    @commands.command()
    async def lsserver(self, ctx):
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": []}
        try:
            E = jdict[str(ctx.guild.id)]["admins"].index(str(ctx.author.id))
        except:
            await ctx.message.add_reaction("❌")
            return
        listserver = ""
        for guild in self.bot.guilds:
            listserver = listserver + guild.name + "\n"
        await ctx.send(embed = discord.Embed(
            title="Server joined:",color=discord.Color.blue(),description=listserver
        ))
def setup(bot):
    bot.cmdlist["admin"] = {
        "intro": "Commands for Admin.",
        "warn": "`$warn <@user> <*reason> [Admin]`\nWarn a user with the reason provided.",
        "kick": "`$kick <@user> <*reason> [Admin]`\nKick a user with the reason provided.",
        "ban": "`$ban <@user> <*reason> [Admin]`\nBan a user with the reason provided.",
        "unban": "`$unban <userid> [Admin]`\nUnban a user with his id.",
        "mute": "`$mute <@user> <*reason> [Admin]`\nMute a user with the reason provided.",
        "unmute": "`$unmute <@user> [Admin]`\nUnmute the user.",
        "lsuser": "`$lsuser [Admin]`\nList users in current server.",
        "lsserver": "`$lsserver [Admin]`\nList server this bot joined.",
        "reactrole": "`$reactrole <title> <content> <*reactors> [Admin]`\nMake a reaction embed.\n[*reactors] format: <emoji> <role ping>",
        "addadmin": "`$addadmin <*users> [Administrator permission]`\nAdd users into the admin list.",
        "lsadmin": "`$lsadmin`\nList users in the admin list.\nAliases: `adminls`",
        "rmadmin": "`$rmadmin <*users>`\nRemove users from the admin list"
        }
    bot.add_cog(admin(bot))