# Imports
import discord
from discord.ext import commands, tasks
from discord.utils import get
import ast
from random import choice
# Status list(Static)
status = ['E', 'with 1 user', 'games', 'TOS-DOS', 'music', 'cytus2', 'Myself', 'phigros', 'nothing', '$man all', '$ask', 'maths', 'Dancerail3','MEMZ','Cytus','$about','CentOS','kali-linux','PUBG','Ubuntu','java','python','WannaCry']

# A new class called auto which is ready to import as a cog
class auto(commands.Cog): # Showing it is a Cog object
    def __init__(self, bot): # Do this on start
        self.bot = bot # Import the bot into the cog
        self.chpre.start() # Start the background which is in line 16
    # Do these once per minute
    @tasks.loop(minutes=1)
    async def chpre(self):
        await self.bot.change_presence( # Let the bot change its presence
            activity=discord.Game(name=choice(status)) # Presence name: random thing in line 8
            )
        guild = get( # Get the guild object of my server
            self.bot.guilds,
            id=800679086955167775
            )
        channel = get( # Get the channel using the channel id
            guild.channels,
            id=855302366261674014
            )
        # Get the number of online user of this server
        usernum = sum(member.status!=discord.Status.offline and not member.bot for member in guild.members)
        # Edit the channel name and show the online user
        await channel.edit(name="🟢｜Members Online: " + str(usernum))
        channel = get( # Get the channel using the channel id
            guild.channels,
            id=855313169102929970
            )
        # Get the number of bot in this server
        usernum = sum(member.bot for member in guild.members)
        # Edit the channel name and show the number of bots
        await channel.edit(name="🤖｜Bot: " + str(usernum))
        channel = get( # Get the channel using the channel id
            guild.channels,
            id=855313907971653655
            )
        # Get the number of member in this server(Including those who is offline)
        usernum = sum(not member.bot for member in guild.members)
        # Edit the channel name and show all the users
        await channel.edit(name="⚪｜All Members: " + str(usernum))
    # Do these things when member join the server
    @commands.Cog.listener()
    async def on_member_join(self, user):
        guild = user.guild # Get the guild object from the user
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        userlist = ast.literal_eval(json.read()) # Read and convert the json to dictionary
        json.close() # Close the object to save resources
        for muteduser in userlist[str(guild.id)]["mutedusers"]: # Get all the muted user [See line 312 of ~/src/cogs/admin.py]
            if muteduser.id == user.id: # If the user joined is muted
                await user.send("You think that getting into the server again can unmute you? How naive") # Tease the user
                return # Terminate all the object
        await user.add_roles(get( # Autorole
            guild.roles,
            id=int(userlist[str(guild.id)]["autorole"])
            ))
        channel = get( # Welcome the user
            guild.channels,
            id=int(userlist[str(guild.id)]["welcome"])
            )
        embed = discord.Embed( # Create an embed object
            title="Welcome new user!",
            url="http://TNTprizz.zapto.org/dc",
            color=discord.Color.blue(),
            description="Welcome " + user.mention + " !\nHope you enjoy staying in this server!"
            )
        # Read the ~/welcome.gif
        gif = discord.File('../welcome.gif', filename="welcome.gif")
        # Set ~/welcome.gif to the embed image object
        embed.set_image(url="attachment://welcome.gif")
        await channel.send(file = gif, embed=embed) # Send out the welcome object
    # Do this when reaction is removed
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji = payload.emoji.name # Get the emoji name
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id) # To get the guild object in line 85
        channel = message.channel # To get the guild object in line 85
        guild = channel.guild # Get the guild object
        user = get(guild.members, id=payload.user_id) # Get the user object
        json = open("../data/auto.json","r") # Prepare to open and read ~/data/auto.json
        roledict = ast.literal_eval(json.read()) # Read the file and convert it to dictionary
        try: # Try to do
            msglist = roledict[str(guild.id)][str(message.id)] # See if the messageid of the reacted message exists in the dictionary
        except KeyError: # If not, then
            json.close() # Close the file object
            return # Terminate the function
        for emo in msglist: # List all the emojis
            if emo == emoji: # If emoji equal to the reacted emoji
                await user.remove_roles(get(guild.roles, id=int(msglist[emoji]))) # Remove the roles
                break # Break
    # Do this when reaction is added
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji.name # Get the emoji name
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id) # To get the guild object in line 104
        channel = message.channel # To get the guild object in line 104
        guild = channel.guild # Get the guild object
        user = get(guild.members, id=payload.user_id) # Get the user object using the userid
        json = open("../data/auto.json","r") # Prepare to open and read ~/data/auto.json
        roledict = ast.literal_eval(json.read()) # Read the file and convert it to dictionary
        try: # Try to do
            msglist = roledict[str(guild.id)][str(message.id)] # See if the messageid of the reacted message exists in the dictionary
        except KeyError: # If not, then
            json.close() # Close the file object
            return # Terminate the function
        for emo in msglist: # List all the emojis
            if emo == emoji: # If emoji equal to the reacted emoji
                await user.add_roles(get(guild.roles, id=int(msglist[emoji]))) # Add the role
                break # Break
# Do this when the cog is loaded
def setup(bot):
    # Add the cog into the bot
    bot.add_cog(auto(bot))
    