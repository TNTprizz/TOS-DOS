#imports
import discord
from discord.ext import commands, tasks
from discord.utils import get
import ast
from random import choice
status = ['E', 'with 1 user', 'games', 'TOS-DOS', 'music', 'cytus2', 'Myself', 'phigros', 'nothing', '$man all', '$ask', 'maths', 'Dancerail3','MEMZ','Cytus','$about','CentOS','kali-linux','PUBG','Ubuntu','java','python','WannaCry']

class auto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chpre.start()
        
    @tasks.loop(minutes=1)
    async def chpre(self):
        await self.bot.change_presence(activity=discord.Game(name =choice(status)))
    
    @commands.Cog.listener()
    async def on_member_join(self, user):
        if user.guild.id != 800679086955167775:
            return
        guild = user.guild
        json = open("../data/admin.json","r")
        userlist = ast.literal_eval(json.read())
        json.close()
        for muteduser in userlist[str(guild.id)]["mutedusers"]:
            if muteduser.id == user.id:
                await user.send("You think that getting into the server again can unmute you? How naive")
                return
        await user.add_roles(get(guild.roles, id=800681780834992129))
        message = await self.bot.get_channel(800679087541583944).fetch_message(827789950606901309)
        channel = message.channel
        embed = discord.Embed(title="Welcome new user!",url="http://TNTprizz.zapto.org/dc",color=discord.Color.blue(),description="Welcome " + user.mention + " !\nHope you enjoy staying in this server!")
        await channel.send(embed=embed)
        await channel.send(file=discord.File('../welcome.gif'))
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji = payload.emoji.name
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        channel = message.channel
        guild = channel.guild
        user = get(guild.members, id=payload.user_id)
        json = open("../data/auto.json","r")
        roledict = ast.literal_eval(json.read())
        try:
            msglist = roledict[str(guild.id)][str(message.id)]
        except KeyError:
            json.close()
            return
        for emo in msglist:
            if emo == emoji:
                await user.remove_roles(get(guild.roles, id=int(msglist[emoji])))
                break
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji.name
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        channel = message.channel
        guild = channel.guild
        user = get(guild.members, id=payload.user_id)
        json = open("../data/auto.json","r")
        roledict = ast.literal_eval(json.read())
        try:
            msglist = roledict[str(guild.id)][str(message.id)]
        except KeyError:
            json.close()
            return
        for emo in msglist:
            if emo == emoji:
                await user.add_roles(get(guild.roles, id=int(msglist[emoji])))
                break
def setup(bot):
    bot.add_cog(auto(bot))