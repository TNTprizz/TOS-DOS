# Imports
import discord
from discord.ext import commands
from discord.utils import get
import ast
import asyncio


# A new class called admin which is ready to import as a cog
class admin(commands.Cog): # Show that it is a discord Cog object.
    def __init__(self, bot): # import the bot
        self.bot = bot # self.bot -> bot
        
    # Configure auto role ($autorole <@Role>)
    @commands.command()
    @commands.guild_only() # Cannot run in a DMChannel
    @commands.has_permissions(administrator=True) # Administrator permission required to run this command
    async def autorole(self, ctx, role):
        role = get(ctx.guild.roles, mention=role)
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json file and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(ctx.guild.id)] # Check if the guild id exists in the guild list
        except: # If not, then......
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "warn": {},  "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Create a new guild field
        jdict[str(ctx.guild.id)]["autorole"] = str(role.id) # Apply autorole into the dictionary
        json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
        json.write(str(jdict)) # Write the dictionary into the json file
        json.close() # Close the object to save resources
        await ctx.message.add_reaction("☑️") # React to message if succeed
    # Configure the welcome channel of the server ($welcomechannel <#Channel>)
    @commands.command()
    @commands.guild_only() # Cannot run in a DMChannel
    @commands.has_permissions(administrator=True) # Administrator permission required to run this command
    async def welcomechannel(self, ctx, channel):
        channel = get(ctx.guild.channels, mention=channel)
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json file and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(ctx.guild.id)] # Check if the guild id exists in the guild list
        except: # If not, then......
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "warn": {}, "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Create a new guild field
        jdict[str(ctx.guild.id)]["welcome"] = str(channel.id) # Apply welcomechannel into the dictionary
        json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
        json.write(str(jdict)) # Write the dictionary into the json file
        json.close() # Close the object to save resources
        await ctx.message.add_reaction("☑️") # React to message if succeed
    # Add user to the admin list ($addadmin <*@Members>)
    @commands.command()
    @commands.guild_only() # Cannot run in a DMChannel
    @commands.has_permissions(administrator=True) # Administrator permission required to run this command
    async def addadmin(self, ctx, *user: discord.Member):
        guildid = ctx.guild.id
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)] # See if guild id exists in the guild list
        except: # If not, then......
            jdict[str(guildid)] = {"mutedusers": [], "warn": {}, "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Add the guild template into the list
            json.close() # Close the object to save resources
            json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
            json.write(str(jdict)) # Write the dictionary into the json file
            json.close() # Close the object to save resources
        for admins in user: # Supports multi user
            if admins.id in jdict[str(ctx.guild.id)]["admins"]: # If the user is already in the list
                break # End the for loop
            jdict[str(ctx.guild.id)]["admins"].append(str(admins.id)) # Append the user's id into the field
        json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
        json.write(str(jdict)) # Write the dictionary into the json file
        json.close() # Close the object to save resources
        await ctx.message.add_reaction("☑️") # React to message if succeed
    # List user in the admin list($lsadmin)
    @commands.command(aliases = ["adminls"]) # Aliases: "adminls"
    @commands.guild_only() # Cannot run in DMChannel
    async def lsadmin(self, ctx):
        guildid = ctx.guild.id
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)] # See if guild id exists in the guild list
        except: # If not, then......
            jdict[str(guildid)] = {"mutedusers": [], "warn": {}, "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Add the guild template into the list
            json.close() # Close the object to save resources
            json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
            json.write(str(jdict)) # Write the dictionary into the json file
            json.close() # Close the object to save resources
        con = "" # Declare a string
        for user in jdict[str(ctx.guild.id)]["admins"]: # List all the admins from the list
            con = con + get(ctx.guild.members, id=int(user)).mention + "\n" # Combine them together
        embed = discord.Embed( # An embed object
            title = "Admins of this server", # Title of the embed
            color = discord.Color.blue(), # Color of the embed
            description = con # Descroption is combined in line 37
        )
        await ctx.send(embed = embed) # Send out the embed
    # Remove user from the admin list($rmadmin <*@Members>)
    @commands.command()
    @commands.guild_only() # Cannot run in DMChannel
    @commands.has_permissions(administrator=True) # Administrator permission required to run this command
    async def rmadmin(self, ctx, *user: discord.Member):
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json file and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the commands
            E = jdict[str(ctx.guild.id)] # Check if the guild id exists in the guild list
        except: # If not, then......
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "warn":{}, "admins": [], "warnchannel": "", "autorole": ""} # Create a new guild field
        for admins in user: # List all the members that are included in the command.
            try: # Try to do the commands
                del jdict[str(ctx.guild.id)]["admins"][jdict[str(ctx.guild.id)]["admins"].index(admins)] # Delete the admin object
            except: # If not successful, it means that the user is not an admin
                raise commands.BadArgument("User not an admin before")
        json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
        json.write(str(jdict)) # Write the dictionary into the json file
        json.close() # Close the object to save resources
        await ctx.message.add_reaction("☑️") # React to message when succeed
    # Create a Reactrole embed ($reactrole <title> <description> <*Content>)
    #<*Content> = [emoji, channelping, emoji, channelping, emoji, channelping, ......]
    @commands.command()
    @commands.guild_only()
    async def reactrole(self, ctx, title = "", description = "", *content):
        guildid = ctx.guild.id
        authorid = ctx.author.id
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)] # See if guild id exists in the guild list
        except: # If not, then......
            jdict[str(guildid)] = {"mutedusers": [],"warn": {} , "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Add the guild template into the list
            json.close() # Close the object to save resources
            json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
            json.write(str(jdict)) # Write the dictionary into the json file
            json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)]["admins"].index(str(authorid)) # See if authorid exists in admin list
        except: # If not, then......
            raise commands.MissingPermissions(["Admin"]) # Raise an exception cuz why not
        if len(content) == 0 or (len(content) % 2) != 0: # If the length of the content is an odd number
            raise commands.BadArgument("Len(content) is an odd number") # Raise an exception
        if len(content) > 40: # If the length of the content is larger than 40
            raise commands.BadArgument("There are more than 40 arguments") # Raise an exception
        json = open("../data/auto.json","r") # Open and prepare to read the ~/data/auto.json
        rrole = ast.literal_eval(json.read()) # Read the json file and convert it to dictionary
        msg = await ctx.send(embed = discord.Embed( # Embed showing that the reactrole thing is configuring
            title="Configuring......" # title
        ))
        try: # Try to do the following command
            E = rrole[str(ctx.guild.id)] # See if the guild id exists in the rrole dictionary
        except: # If doesn't, then......
            rrole[str(ctx.guild.id)] = {} # Create a guild id object
        rrole[str(ctx.guild.id)][str(msg.id)] = {} # Create a message id object in the guild id object
        count = 0 # Count the number of reaction
        for con in content: # List all the content
            if (content.index(con) % 2) == 0: # It the content index is an Even number
                await msg.add_reaction(str(con)) # Add reaction
            else: # Or
                rrole[str(ctx.guild.id)][str(msg.id)][content[count]] = str(get(ctx.guild.roles, mention=con).id)
                # Append "emoji" :"roleid"
                count = count + 2
                # count once
        embdes = "" # Stands for the content of the react message
        for emoji in rrole[str(ctx.guild.id)][str(msg.id)]: # List all the emojis
            id = rrole[str(ctx.guild.id)][str(msg.id)][emoji] # Get the role id with the emoji
            emo = str(
                get(
                    ctx.guild.roles, id=int(id)
                    ).mention
                    ) # Get the ping of the role
            embdes = embdes + emoji + ": " + emo + "\n" # Combine then together
        embed = discord.Embed( # Embed object
            title = title, # title
            description = embdes + "\n" + description, # Content + Description
            color = discord.Color.blue() # Color
        )
        await msg.edit(embed = embed) # Edit the configuring embed
        json.close() # Close the file object to get the empty object
        json = open("../data/auto.json","w") # Open and ready to write ~/data/auto.json 
        json.write(str(rrole)) # Write the rrole dictionary into the file
        json.close() # Close the file object to save resources
    # Warn a user as an admin ($warn <@Member> <Reason>)
    @commands.command()
    @commands.guild_only()
    async def warn(self ,ctx, user: discord.Member, *,reason):
        guildid = ctx.guild.id
        authorid = ctx.author.id
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)] # See if guild id exists in the guild list
        except: # If not, then......
            jdict[str(guildid)] = {"mutedusers": [], "warn": {}, "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Add the guild template into the list
            json.close() # Close the object to save resources
            json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
            json.write(str(jdict)) # Write the dictionary into the json file
            json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)]["admins"].index(str(authorid)) # See if authorid exists in admin list
        except: # If not, then......
            raise commands.MissingPermissions(["Admin"]) # Permission denied
        try:
            jdict[str(guildid)]["warn"][str(user.id)][0]
        except:
            jdict[str(guildid)]["warn"][str(user.id)] = []
        jdict[str(guildid)]["warn"][str(user.id)].append(reason)
        json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
        json.write(str(jdict)) # Write the dictionary into the json file
        json.close() # Close the object to save resources
        # Make the embed object
        embed = discord.Embed(
            title=user.name + " is WARNED",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.red(),
            description="Reason:\n" + reason + "\nFrom " + ctx.author.mention
            )
        # Send out the embed object to the current channel
        await ctx.send(embed=embed)
        # Make the embed object which will be sent to warning channel
        embed = discord.Embed(
            title=user.name + " is WARNED",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.red(),
            description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention
            )
        try: # Try to do
            # See if the channel exists in the json file in line 138
            await get(
                ctx.guild.channels,
                id=int(jdict[str(ctx.guild.id)]["warnchannel"])
                ).send(embed=embed)
        except: # If it cannot
            # Remind admin to set the warnchannel
            await ctx.send("You may use `$warnchannel <#channel>` to specify the channel you want to public the warning channels.")
        # Make the embed object
        embed = discord.Embed(
            title="You are warned",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.green(),
            description="Reason:" + reason + "\nFrom " + ctx.author.mention
            )
        await user.send(embed=embed) # DM user the warning message
    # Show the warn record ($warnrecord [@Member])
    @commands.command()
    @commands.guild_only()
    async def warnrecord(self, ctx):
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        dir = jdict[str(ctx.guild.id)]["warn"]
        con = ""
        for mem in dir:
            name = get(ctx.guild.members, id=int(mem)).display_name
            con = con + name + " :\n"
            for rec in dir[mem]:
                con = con + "> " + rec + "\n"
        if con == "":
            con = "No one is ever warned in this server"
        embed = discord.Embed(
            title="Warn records",
            color=discord.Color.red(),
            description="```\n" + con + "\n```",
        )
        await ctx.send(embed=embed)
    # Kick a user as an admin ($kick <@Member> <Reason>)
    @commands.command()
    @commands.guild_only()
    async def kick(self ,ctx, user: discord.Member, *, reason):
        guildid = ctx.guild.id
        authorid = ctx.author.id
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)] # See if guild id exists in the guild list
        except: # If not, then......
            jdict[str(guildid)] = {"mutedusers": [], "warn":{}, "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Add the guild template into the list
            json.close() # Close the object to save resources
            json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
            json.write(str(jdict)) # Write the dictionary into the json file
            json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)]["admins"].index(str(authorid)) # See if authorid exists in admin list
        except: # If not, then......
            raise commands.MissingPermissions(["Admin"]) # Permission denied
        await user.kick(reason=reason) # Kick the user out of the server
        # Make an embed object
        embed = discord.Embed(
            title=user.name + " is KICKED",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.red(),
            description="Reason:\n" + reason + "\nFrom " + ctx.author.mention)
        await ctx.send(embed=embed) # Send the embed object to the current channel
        # Make an embed object which will be sent to the current channel
        embed = discord.Embed(
            title=user.name + " is KICKED",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.red(),
            description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
        try: # Try to do
            # See if the channel exists in the json file in line 138
            await get(
                ctx.guild.channels,
                id=int(
                    jdict[str(ctx.guild.id)]["warnchannel"]
                    )
                ).send(embed=embed)
        except: # If it cannot
            # Remind admin to set the warnchannel
            await ctx.send(
                "You may use `$warnchannel <#channel>` to specify the channel you want to public the warning channels."
                )
        # Make the embed object
        embed = discord.Embed(
            title="You are kicked",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.green(),
            description="Reason:" + reason + "\nFrom " + ctx.author.mention
            )
        await user.send(embed=embed) # DM user the warning message
    # Ban a user as an admin ($kick <@Member> <Reason>)
    @commands.command()
    @commands.guild_only()
    async def ban(self , ctx, user: discord.Member, *, reason):
        guildid = ctx.guild.id
        authorid = ctx.author.id
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)] # See if guild id exists in the guild list
        except: # If not, then......
            jdict[str(guildid)] = {"mutedusers": [], "warn": {}, "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Add the guild template into the list
            json.close() # Close the object to save resources
            json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
            json.write(str(jdict)) # Write the dictionary into the json file
            json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)]["admins"].index(str(authorid)) # See if authorid exists in admin list
        except: # If not, then......
            raise commands.MissingPermissions(["Admin"]) # Permission denied
        await user.ban(reason=reason) # Ban the user
        # Make the embed
        embed = discord.Embed(
            title=user.name + " is BANNED",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.red(),
            description="Reason:\n" + reason + "\nFrom " + ctx.author.mention
            )
        await ctx.send(embed=embed) # Send the embed to the channel
        # Make the embed object again
        embed = discord.Embed(
            title=user.name + " is BANNED!",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.red(),
            description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention
            )
        try: # Try to do
            # See if the channel exists in the json file in line 191
            await get(
                ctx.guild.channels,
                id=int(
                    jdict[str(ctx.guild.id)]["warnchannel"]
                    )
                ).send(embed=embed)
        except: # If failed
            # Remind admin to set warnchannel
            await ctx.send("You may use `$warnchannel <#channel>` to specify the channel you want to public the warning channels.")
        # Make the embed object
        embed = discord.Embed(
            title="You are banned",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.green(),
            description="Reason:" + reason + "\nFrom " + ctx.author.mention
            )
        await user.send(embed=embed) # DM user the embed
    # Mute a user by removing all his roles ($mute <@Member> <Reason>)
    @commands.command()
    @commands.guild_only()
    async def mute(self, ctx, user: discord.Member, *, reason):
        guildid = ctx.guild.id
        authorid = ctx.author.id
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)] # See if guild id exists in the guild list
        except: # If not, then......
            jdict[str(guildid)] = {"mutedusers": [], "warn": {}, "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Add the guild template into the list
            json.close() # Close the object to save resources
            json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
            json.write(str(jdict)) # Write the dictionary into the json file
            json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)]["admins"].index(str(authorid)) # See if authorid exists in admin list
        except: # If not, then......
            raise commands.MissingPermissions(["Admin"]) # Permission denied
        for role in user.roles: # Get Member's all roles
            if role.name != "@everyone": # Don't remove the @everyone role
                await user.remove_roles(role) # Remove all his roles
        for deuser in jdict[str(ctx.guild.id)]["mutedusers"]: # List all the muted users
            if user.id == deuser: # If the member is already muted
                raise commands.BadArgument("User '" + user.display_name + "' is not muted!")
        jdict[str(ctx.guild.id)]["users"].append(user.id) # Add user id into the muted list
        json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
        json.write(str(jdict)) # Write the dictionary into the file
        json.close() # Close the object to save resources
        # Make the embed object
        embed = discord.Embed(
            title=user.name + " is MUTED",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.red(),
            description="Reason:\n" + reason + "\nFrom " + ctx.author.mention
            )
        await ctx.send(embed=embed) # Send the embed to the current ctx channel
        # Make the embed object
        embed = discord.Embed(
            title=user.name + " is MUTED!",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.red(),
            description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
        try: # Try to do
            await get( # Get the warning channel from the dictionary
                ctx.guild.channels,
                id=int(
                    jdict[str(ctx.guild.id)]["warnchannel"]
                    )
                ).send(embed=embed)
        except: # If it cannot
            # Remind the admin to set the warning channel
            await ctx.send("You may use `$warnchannel <#channel>` to specify the channel you want to public the warning channels.")
        embed = discord.Embed( # Make the embed object
            title="You are muted",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.green(),
            description="Reason:" + reason + "\nFrom " + ctx.author.mention
            )
        await user.send(embed=embed) # DM user the embed
    # Unmute the user ($ummute <@Member>)
    @commands.command()
    @commands.guild_only()
    async def unmute(self, ctx, user: discord.Member):
        guildid = ctx.guild.id
        authorid = ctx.author.id
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)] # See if guild id exists in the guild list
        except: # If not, then......
            jdict[str(guildid)] = {"mutedusers": [], "warn": {}, "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Add the guild template into the list
            json.close() # Close the object to save resources
            json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
            json.write(str(jdict)) # Write the dictionary into the json file
            json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)]["admins"].index(str(authorid)) # See if authorid exists in admin list
        except: # If not, then......
            raise commands.MissingPermissions(["admin"]) # Permission denied
        for deuser in jdict[str(ctx.guild.id)]["mutedusers"]: # List all the muted users
            if user.id == deuser: # If the user who is being unmuted os in the mutelist
                # Delete the object
                del jdict[str(ctx.guild.id)]["mutedusers"][jdict[str(ctx.guild.id)]["mutedusers"].index(user.id)]
                json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
                json.write(str(jdict)) # Write the dictionary into the file
                json.close() # Close the object to save resources
                try: # Try to do
                    torole = jdict[str(ctx.guild.id)]["autorole"] # Get autorole id
                    guild = user.guild # Get the guild where the user is
                    await user.add_roles(get(guild.roles, id=int(torole))) # Add the user back to autorole
                except: # If it cannot
                    # Send the warning message
                    await ctx.send("Cannot unmute. Please configure the autorole using `$autorole <@Role>`")   
                embed = discord.Embed( # Create the embed object
                    title=user.name + " is UNMUTED",
                    url="http://tntprizz.zapto.org/dc",
                    color=discord.Color.red(),
                    description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention
                    )
                await ctx.send(embed=embed) # Send out the embed object
                embed = discord.Embed( # Create the embed object
                    title=user.name + " is UNMUTED!",
                    url="http://tntprizz.zapto.org/dc",
                    color=discord.Color.red(),
                    description="Thanks for admin's Great Fat Compassion!\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention
                    )
                try: # Try to do
                    channel = await get( # Get the warningchannel and send out the embed object to the channel.
                        ctx.guild.channels,
                        id=int(jdict[str(ctx.guild.id)]["warnchannel"])
                        ).send(embed=embed)
                    await channel.send(embed=embed)
                except: # If it failed
                    # Warn Admin
                    await ctx.send("You may use `$warnchannel <#channel>` to specify the channel you want to public the warning channels.")
                embed = discord.Embed( # Create the embed object
                    title="You are unmuted",
                    url="http://tntprizz.zapto.org/dc",
                    color=discord.Color.green(),
                    description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention
                    )
                await user.send(embed=embed) # DM user the embed object
                return # Terminate the function
        raise commands.BadArgument("User '" + user.display_name + "' is not muted!") # Raise an exception
    # Unban a user using his USER ID ($unban <int:User id>)
    @commands.command()
    @commands.guild_only()
    async def unban(self, ctx, id):
        guildid = ctx.guild.id
        authorid = ctx.author.id
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)] # See if guild id exists in the guild list
        except: # If not, then......
            jdict[str(guildid)] = {"mutedusers": [], "warn": {}, "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Add the guild template into the list
            json.close() # Close the object to save resources
            json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
            json.write(str(jdict)) # Write the dictionary into the json file
            json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)]["admins"].index(str(authorid)) # See if authorid exists in admin list
        except: # If not, then......
            raise commands.MissingPermissions(["admin"]) # Permission denied
        user = await self.bot.fetch_user(id) # Get the user object
        await ctx.guild.unban(user) # Unban the user
        # Make the embed object
        embed = discord.Embed(
            title=user.name + " is UNBANNED",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.red(),
            description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention
            )
        await ctx.send(embed=embed) # Send the embed object to the ctx
        try: # Try to do
            channel = await get( # Get the warning channel
                ctx.guild.channels,
                id=int(jdict[str(ctx.guild.id)]["warnchannel"])
                ).send(embed=embed)
            await channel.send(embed=embed)
        except: # If it cannot
            # Announce the admin to configure the warning channel
            await ctx.send("You may use `$warnchannel <#channel>` to specify the channel you want to public the warning channels.")
        # Make the embed object
        embed = discord.Embed(
            title="You are unbanned",
            url="http://tntprizz.zapto.org/dc",
            color=discord.Color.green(),
            description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention
            )
        await user.send(embed=embed) # DM user the embed object
    # List all users in this server ($lsuser)
    @commands.command()
    async def lsuser(self, ctx):
        guildid = ctx.guild.id
        authorid = ctx.author.id
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)] # See if guild id exists in the guild list
        except: # If not, then......
            jdict[str(guildid)] = {"mutedusers": [], "warn": {}, "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Add the guild template into the list
            json.close() # Close the object to save resources
            json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
            json.write(str(jdict)) # Write the dictionary into the json file
            json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)]["admins"].index(str(authorid)) # See if authorid exists in admin list
        except: # If not, then......
            raise commands.MissingPermissions(["admin"]) # Permission denied
        listuser = "" # The string ready to be sent
        for user in ctx.guild.members: # List all the members in this server
            listuser = listuser + user.mention + " ," # Append them together
        await ctx.send( # Send the following: 
            embed = discord.Embed( # Create the embed object
                title="Users in this server:",
                color=discord.Color.blue(),
                description=listuser
        ))
    # List servers the bot joined ($lsserver)
    @commands.command()
    async def lsserver(self, ctx):
        guildid = ctx.guild.id
        authorid = ctx.author.id
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)] # See if guild id exists in the guild list
        except: # If not, then......
            jdict[str(guildid)] = {"mutedusers": [], "warn": {}, "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Add the guild template into the list
            json.close() # Close the object to save resources
            json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
            json.write(str(jdict)) # Write the dictionary into the json file
            json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)]["admins"].index(str(authorid)) # See if authorid exists in admin list
        except: # If not, then......
            raise commands.MissingPermissions(["admin"]) # Permission denied
        listserver = "" # The string ready to be sent
        for guild in self.bot.guilds: # List all the servers the bot joined
            listserver = listserver + guild.name + "\n" # Append them together
        await ctx.send( # Send the following
            embed = discord.Embed( # Create the embed object
                title="Server joined:",
                color=discord.Color.blue(),
                description=listserver
        ))
    # Configure the warning channel ($warnchannel <#Channel>)
    @commands.guild_only()
    @commands.command()
    async def warnchannel(self, ctx, cha):
        guildid = ctx.guild.id
        authorid = ctx.author.id
        json = open("../data/admin.json","r") # Open and prepare to read ~/data/admin.json
        jdict = ast.literal_eval(json.read()) # Read the json and convert it to dictionary
        json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)] # See if guild id exists in the guild list
        except: # If not, then......
            jdict[str(guildid)] = {"mutedusers": [], "warn": {}, "admins": [], "warnchannel": "", "autorole": "", "welcome": ""} # Add the guild template into the list
            json.close() # Close the object to save resources
            json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json
            json.write(str(jdict)) # Write the dictionary into the json file
            json.close() # Close the object to save resources
        try: # Try to do the following commands
            E = jdict[str(guildid)]["admins"].index(str(authorid)) # See if authorid exists in admin list
        except: # If not, then......
            raise commands.MissingPermissions(["admin"]) # Permission denied
        jdict[str(ctx.guild.id)]["warnchannel"] = str(get( # Get the warning channel id and overwrite it to the dictionary
            ctx.guild.channels,
            mention=cha
            ).id)
        json = open("../data/admin.json","w") # Open and prepare to write ~/data/admin.json 
        json.write(str(jdict)) # Write the dictionary into the file
        json.close() # Close the object to save resources
        await ctx.message.add_reaction("☑️") # React if succeed
# Do this when the cog is loaded
def setup(bot):
    # For Manual commands($man)
    bot.cmdlist["admin"] = {
        "intro": "Commands for Admin.",
        "warn": "`warn <@user> <*reason> [Admin]`\nWarn a user with the reason provided.",
        "kick": "`kick <@user> <*reason> [Admin]`\nKick a user with the reason provided.",
        "ban": "`ban <@user> <*reason> [Admin]`\nBan a user with the reason provided.",
        "unban": "`unban <userid> [Admin]`\nUnban a user with his id.",
        "mute": "`mute <@user> <*reason> [Admin]`\nMute a user with the reason provided.",
        "unmute": "`unmute <@user> [Admin]`\nUnmute the user.",
        "lsuser": "`lsuser [Admin]`\nList users in current server.",
        "lsserver": "`lsserver [Admin]`\nList server this bot joined.",
        "reactrole": "`reactrole <title> <content> <*reactors> [Admin]`\nMake a reaction embed.\n[*reactors] format: <emoji> <role ping>",
        "addadmin": "`addadmin <*users> [Administrator permission]`\nAdd users into the admin list.",
        "lsadmin": "`lsadmin`\nList users in the admin list.\nAliases: `adminls`",
        "rmadmin": "`rmadmin <*users> [Administrator permission]`\nRemove users from the admin list",
        "warnchannel": "`warnchannel <#channel> [Admin]`\nSet the channel where the warning messages be sent.",
        "prefix": "`prefix (prefix) [Admin]`\nSet the prefix of this server or show the prefix of this server.\n(put in bot.py cuz necessary)",
        "autorole": "`autorole <@role> [Administrator permission]`\nSet autorole for the server.",
        "welcomechannel": "`welcomechannel <#Channel> [Administrator permission]`\nSet the welcome channel for the server."
        }
    # Add the cog into the bot
    bot.add_cog(admin(bot))