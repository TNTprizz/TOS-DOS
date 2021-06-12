#imports
import discord
from discord.ext import commands
from discord.utils import get
import ast

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    @commands.has_role('Administrator')
    async def warn(self ,ctx, user: discord.User,*reason):
        message = await self.bot.get_channel(851784439204675584).fetch_message(851784867066282057)
        channel = message.channel
        reason = " ".join(reason)
        embed = discord.Embed(title=user.name + " is WARNED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nFrom " + ctx.author.mention)
        await ctx.send(embed=embed)
        embed = discord.Embed(title="You are warned",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Reason:" + reason + "\nFrom " + ctx.author.mention)
        await user.send(embed=embed)
        embed = discord.Embed(title=user.name + " is WARNED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
        await channel.send(embed=embed)
    @commands.command()
    @commands.has_role("Administrator")
    async def kick(self ,ctx, user: discord.Member, *reason):
        message = await self.bot.get_channel(851784439204675584).fetch_message(851784867066282057)
        channel = message.channel
        reason = " ".join(reason)
        await user.kick(reason=reason)
        embed = discord.Embed(title=user.name + " is KICKED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nFrom " + ctx.author.mention)
        await ctx.send(embed=embed)
        embed = discord.Embed(title="You are kicked",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Reason:" + reason + "\nFrom " + ctx.author.mention)
        await user.send(embed=embed)
        embed = discord.Embed(title=user.name + " is KICKED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
        await channel.send(embed=embed)
    @commands.command()
    @commands.has_role("Administrator")
    async def ban(self , ctx, user: discord.Member, *reason):
        message = await self.bot.get_channel(851784439204675584).fetch_message(851784867066282057)
        channel = message.channel
        reason = " ".join(reason)
        await user.ban(reason=reason)
        embed = discord.Embed(title=user.name + " is BANNED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nFrom " + ctx.author.mention)
        await ctx.send(embed=embed)
        embed = discord.Embed(title="You are banned",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Reason:" + reason + "\nFrom " + ctx.author.mention)
        await user.send(embed=embed)
        embed = discord.Embed(title=user.name + " is BANNED!",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
        await channel.send(embed=embed)
    @commands.command()
    @commands.has_role("Administrator")
    async def mute(self, ctx, user: discord.Member, *reason):
        for role in user.roles:
            if role.name != "@everyone":
                await user.remove_roles(role)
        json = open("../data/admin.json","r")
        userlist = ast.literal_eval(json.read())
        json.close()
        for deuser in userlist["users"]:
            if user.id == deuser:
                await ctx.send("He is already muted, no worth it man.")
                return
        userlist["users"].append(user.id)
        json = open("../data/admin.json","w")
        json.write(str(userlist))
        json.close()
        message = await self.bot.get_channel(851784439204675584).fetch_message(851784867066282057)
        channel = message.channel
        reason = " ".join(reason)
        embed = discord.Embed(title=user.name + " is MUTED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nFrom " + ctx.author.mention)
        await ctx.send(embed=embed)
        embed = discord.Embed(title="You are muted",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Reason:" + reason + "\nFrom " + ctx.author.mention)
        await user.send(embed=embed)
        embed = discord.Embed(title=user.name + " is MUTED!",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
        await channel.send(embed=embed)
    @commands.command()
    @commands.has_role("Administrator")
    async def unmute(self, ctx, user: discord.Member):
        message = await self.bot.get_channel(851784439204675584).fetch_message(851784867066282057)
        channel = message.channel
        json = open("../data/admin.json","r")
        userlist = ast.literal_eval(json.read())
        json.close()
        for deuser in userlist["users"]:
            if user.id == deuser:
                del userlist["users"][userlist["users"].index(user.id)]
                json = open("../data/admin.json","w")
                json.write(str(userlist))
                json.close()
                guild = user.guild
                await user.add_roles(get(guild.roles, id=800681780834992129))
                embed = discord.Embed(title=user.name + " is UNMUTED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention)
                await ctx.send(embed=embed)
                embed = discord.Embed(title="You are unmuted",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention)
                await user.send(embed=embed)
                embed = discord.Embed(title=user.name + " is UNMUTED!",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Thanks for admin's Great Fat Compassion!\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
                await channel.send(embed=embed)
                return
        await ctx.send("He is not muted, idiot")
    @commands.command()
    @commands.has_role("Administrator")
    async def unban(self, ctx, id):
        message = await self.bot.get_channel(851784439204675584).fetch_message(851784867066282057)
        channel = message.channel
        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user)
        embed = discord.Embed(title=user.name + " is UNBANNED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention)
        await ctx.send(embed=embed)
        embed = discord.Embed(title="You are unbanned",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention)
        await user.send(embed=embed)
        embed = discord.Embed(title=user.name + " is BANNED!",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Thanks for admin's Great Fat Compassion!\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
        await channel.send(embed=embed)
def setup(bot):
    bot.cmdlist["admin"] = {
        "intro": "Commands for Admin.",
        "warn": "`$warn <@user> <*reason> [Administrator]`\nWarn a user with the reason provided.",
        "kick": "`$kick <@user> <*reason> [Administrator]`\nKick a user with the reason provided.",
        "ban": "`$ban <@user> <*reason> [Administrator]`\nBan a user with the reason provided.",
        "unban": "`$unban <userid> [Administrator]`\nUnban a user with his id.\n",
        "mute": "`$mute <@user> <*reason> [Administrator]`\nMute a user with the reason provided.\n",
        "unmute": "`$unmute <@user> [Administrator]`\nUnmute the user."
        }
    bot.add_cog(admin(bot))