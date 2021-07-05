# Imports
from gpiozero import CPUTemperature
import psutil
from discord.ext import commands
import discord
import asyncio
import ast
import time
import yaml

# A new class called bash is ready to import as a cog
class bash(commands.Cog): # Show that it is a discord Cog object
    def __init__(self, bot): # Import the bot
        self.bot = bot # Self.bot -> bot   
    # Send out the sourcecode link ($sourcecode)
    @commands.command()
    async def sourcecode(self, ctx):
        # Send out the sourcecode embed
        await ctx.send(
            embed = discord.Embed(
                title="source code link:",
                url="https://github.com/TNTprizz/TOS-DOS",
                description="[Github](https://github.com/TNTprizz/TOS-DOS)\nUpdate unevenly",
                color=discord.Color.blue()
            )
        )
    # Send out author's data and status ($aboutme)
    @commands.guild_only()
    @commands.command(aliases=["profile"])
    async def aboutme(self, ctx):
        mention = [] # Create mention object(see line 46)
        user = ctx.author # user = author
        try: # Try to do
            act = user.activities[0].name # Fetch user activities
        except Exception: # If it cannot
            act = "Unknown or not defined." # Action cannot be defined
        status = str(user.status) # Status can be fetched using the user object
        if status == "dnd": # If user's status is "dnd"
            status = "Do not disturb" # Change it to "Do not disturb"
        elif status == "idle": # If user's status is "idle"
            status = "AFK" # Change it to "AFK"
        if str(act) == None: # If act is nothing
            act = "No activity." # Set it to "no activity"
        for role in user.roles: # List all the roles of the user
            if role.name != "@everyone": # If it is not @everyone
                mention.append(role.mention) # Append the mention
            else: # It it is @everyone
                mention.append("@everyone") # Append the name
        b = ", ".join(mention) # Join them all using ", "
        trole = user.top_role.mention # Get the user top role
        if user.top_role == None: # If the user don't have a role
            trole = "No role" # Set it to "no role"
        # Create an embed object
        embed = discord.Embed(
            title=user.name + "'s profile",
            url="http://tntprizz.zapto.org/dc",
            description="",
            color=discord.Color.blue()
            )
        embed.set_thumbnail( # Set the thhumbnail to the user's avatar
            url=user.avatar_url
            )
        embed.add_field( # Add user's display name as a field of the embed
            name="User display name",
            value=user.display_name
            )
        embed.add_field( # Mention the user as a field of the embed
            name="User mention",value=user.mention
            )
        embed.add_field( # Get the user id as a field of the embed
            name="User ID",
            value=user.id
            )
        embed.add_field( # Get the user activity as mentioned in line 33 as a field of the embed
            name="User activity",
            value=act
            )
        embed.add_field( # Get the user status as mentioned in line 36
            name="User status",
            value=status
            )
        embed.add_field( # Get user's top role as mentioned in line 49
            name="User top role",
            value=trole,
            inline=False
            )
        embed.add_field( # Get user's roles list as mentioned in line 48
            name="User roles",
            value=b
            )
        # Export the embed
        await ctx.send(embed=embed)
    # About someone or the bot itseif ($about <@Member>)
    @commands.command()
    async def about(self, ctx, user = "bot"):
        cputemp = CPUTemperature() # Get cpu temperature object
        temp = str(cputemp.temperature) # Get the temperature and convert it to string
        usage = str(psutil.cpu_percent(interval=0.3)) # Get the CPU usage and convert it to string
        memory = psutil.virtual_memory().percent # Get the RAM amount and convert it to percentage
        used = round(memory / 100 * 7629, 3) # Get the used RAM amount using simple calculation
        if user == "bot": # If nothing is inserted
            embed = discord.Embed( # Create the embed object
                title="about TOS-DOS:",
                url="http://TNTprizz.zapto.org/dc",
                description="about open sourced TOS-DOS",
                color=discord.Color.gold()
            )
            embed.add_field( # Add field about the author (thats me)
                name="author",
                value="<@469038475371479041>",
                inline=True
            )
            embed.add_field( # Add field about the bot itself
                name="name",
                value="<@827778239606554635>",
                inline=True
            )
            embed.add_field( # Add field about the version of the bot
                name="version",
                value=self.bot.ver,
                inline=True
            )
            embed.add_field( # Add field about the stage of the bot
                name="stage",
                value="Cogs",
                inline=True
            )
            embed.add_field( # Add field about the status of the bot
                name="status",
                value="running",
                inline=True
            )
            embed.add_field( # Add field about the sourcecode of the bot
                name="source",
                value="[Github](https://github.com/TNTprizz/TOS-DOS)",
                inline=True
            )
            embed.add_field( # Add field about the CPU of my rapsberry pi
                name="CPU:",
                value="```\nTemperature: " + temp + "°C\n" + "Usage: " + usage + "%\n```"
            )
            embed.add_field( # Add field about the RAM of my raspberry pi
                name="RAM:",
                value="```\nUsed: " + str(used) + "/7629.395 MiB\n" + "Percent: " + str(memory) + "%\n```"
            )
            # Export the embed object
            await ctx.send(embed=embed)
        else: # If argument is inserted
            converter = discord.ext.commands.MemberConverter() # Create a thing that can convert input to server member
            user = await converter.convert(ctx, user) # Convert the input into the server member
            # Same as command ($aboutme) but different user, not gonna explain
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
                else:
                    mention.append("@everyone")
            b = ", ".join(mention)
            trole = user.top_role
            if user.top_role == None:
                trole = "No role"
            embed = discord.Embed(
                title=user.name + "'s profile",
                url="http://tntprizz.zapto.org/dc",
                description="",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(
                url=user.avatar_url
            )
            embed.add_field(
                name="User display name",
                value=user.display_name
            )
            embed.add_field(
                name="User mention",
                value=user.mention
            )
            embed.add_field(
                name="User ID",
                value=user.id
            )
            embed.add_field(
                name="User activity",
                value=act
                )
            embed.add_field(
                name="User status",
                value=status
                )
            embed.add_field(
                name="User top roles",
                value=trole,
                inline=False
            )
            embed.add_field(
                name="User roles",
                value=b
            )
            await ctx.send(embed=embed)
    # DM user the arguments ($secho <#Member> <Message>)
    @commands.command()
    async def secho(self, ctx, user: discord.User,* , args: str):
        await user.send(args) # DM user the message
        await ctx.message.add_reaction("☑️") # React to message if succeed
    # Print out the version of the bot ($version)
    @commands.command()
    async def version(self, ctx):
        await ctx.send("Version: " + self.bot.ver) # Print out the version of the bot
    # Export an embed table ($embed <title> <content>)
    @commands.command(pass_context=True)
    async def embed(self, ctx, title: str, con: str):
        embed = discord.Embed( # Create an embed object with title and content
            title=title,
            url="http://tntprizz.zapto.org/dc",
            description=con,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed) # Export the embed object
    # Export an embed table but delete the author message ($dembed <title> <content>)
    @commands.command()
    async def dembed(self, ctx, title: str, con: str):
        embed = discord.Embed( # Create an embed object with title and content
            title=title,
            url="http://tntprizz.zapto.org/dc",
            description=con,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed) # Export the embed object
        await ctx.message.delete() # Delete the author message
    # Ping the bot and print out the bot latency ($ping)
    @commands.command()
    async def ping(self, ctx):
        thoery = round(self.bot.latency * 1000) # Get the theoretical bot latency
        temp = time.time() # Get the time tick
        msg = await ctx.send(embed = discord.Embed( # Send out a test embed object
            title="Detected latency of sending message......",
            color=discord.Color.purple()
        ))
        sendtime = (time.time() - temp) * 1000 # Record the latency
        temp = time.time() # Get the time tick
        await msg.edit(embed = discord.Embed( # Edit the test embed object
            title="Detected latency of editing message......",
            color=discord.Color.purple()
        ))
        edittime = (time.time() - temp) * 1000 # Record the latency
        temp = time.time() # Get the time tick
        await msg.delete() # Delete the test message
        deltime = (time.time() - temp) * 1000 # Record the latency
        embed = discord.Embed( # Make the imformation embed
            title="Pong!",
            color=discord.Color.dark_orange(),
            description="```\nTheoretical bot latency: " + str(thoery) + " ms\nLatency of bot sending message: " + str(round(sendtime)) + " ms\nLatency of bot editing message: " + str(round(edittime)) + " ms\nLatency of bot deleting message: " + str(round(deltime)) + " ms\n```"
        )
        await ctx.send(embed=embed) # Export the embed
    @commands.command()
    async def sett(self, ctx):
        with open("../config.yml","r") as f:
            configfile = f.read()
        configfile = configfile.replace(self.bot.config["token"], "[ FORBIDDEN ]")
        await ctx.send("```asciidoc\n" + configfile + "```")
    @commands.command()
    async def rlsett(self, ctx):
        if not ctx.author.id in self.bot.config["sudoers"]:
            raise commands.NotOwner("You are not sudoers!")
        with open("../config.yml","r") as f:
            self.bot.config = yaml.safe_load(f)
        await ctx.message.add_reaction("☑️")
    # Repeat what you said ($echo <content>)
    @commands.command()
    async def echo(self, ctx,* ,echoed: str):
        await ctx.send(echoed) # Simply send the argument.
    # Get a list of author's role ($whoamirole)
    @commands.command(aliases = ["rolecheck", "checkrole"])
    async def whoamirole(self, ctx):
        # Same as line 162 to 171, not going to explain
        mention = []
        user = ctx.author
        for role in user.roles:
            if role.name != "@everyone":
                mention.append(role.mention)
        b = ", ".join(mention)
        embed = discord.Embed(
            title="Info:",
            description=f"Info of: {user.mention}",
            color=discord.Color.orange()
            )
        embed.add_field(
            name="Top role:",
            value=user.top_role
            )
        embed.add_field(
            name="Roles:",
            value=b
            )
        await ctx.send(embed=embed)
    # Delete the author message after 2 seconds ($temp )
    @commands.command()
    async def temp(self, ctx):
        # Wait for 2 seconds
        await asyncio.sleep(2)
        await ctx.message.delete() # Delete the author message
    # Delete the message after repeating what you said
    @commands.command()
    async def decho(self, ctx, *, echoed):
        await ctx.send(echoed) # Repeat what you said
        await ctx.message.delete() # Delete the author message
    # Show the image using the link ($echoimage <url>)
    @commands.command(aliases=["image"])
    async def echoimage(self, ctx, *url: str):
        embed = discord.Embed( # Create the embed message
            title="  ",
            color=discord.Color.blue())
        embed.set_image(url=url) # Set the image using the url
        await ctx.send(embed=embed) # Export the embed
        await ctx.message.delete() # Delete the user message cuz essential
    # Purge the messages ($purge <limit>)
    @commands.command()
    async def purge(self, ctx, limit:int = 0):
        # See if the author is in the admin list or not
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": [], "warnchannel": ""}
        try:
            E = jdict[str(ctx.guild.id)]["admins"].index(str(ctx.author.id))
        except:
            raise commands.MissingPermissions(["admin"]) # Permission denied
        await ctx.channel.purge(limit=limit + 1) # Purge the messages
    # Edit the message the bot itself sent ($eembed <messageid> <title> <content>)
    @commands.command()
    async def eembed(self ,ctx, messageid: int, title: str, content: str):
        # see if the author is in the admin list or not
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": [], "warnchannel": ""}
        try:
            E = jdict[str(ctx.guild.id)]["admins"].index(str(ctx.author.id))
        except:
            raise commands.MissingPermissions(["admin"]) # Permission denied
        try:
            msg = await ctx.fetch_message(messageid) # Get the message using the message id
            await msg.edit(embed=discord.Embed( # Replace the message with the new embed
                title=title,
                url="http://tntprizz.zapto.org/dc",
                description=content,
                color=discord.Color.blue()
                ))
            await ctx.message.delete() # Delete the user message
        except:
            raise commands.MessageNotFound(str(messageid)) # Message not found exception
    # Add reaction to a message ($areact <messageid> <emoji>)
    @commands.command()
    async def areact(self, ctx, messageid: int, emoji):
        # Check if the author is in the admin list or not
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": [], "warnchannel": ""}
        try:
            E = jdict[str(ctx.guild.id)]["admins"].index(str(ctx.author.id))
        except:
            raise commands.MissingPermissions(["admin"]) # Perission denied
        try:
            await ctx.message.delete() # Delete the author message
            msg = await ctx.fetch_message(messageid) # Fetch the message using the message id
            await msg.add_reaction(emoji) # Add reaction into the message
        except:
            raise commands.MessageNotFound(str(messageid)) # raise Message not found exception
    # Replace the message content with the text ($eecho <messageid> <content>)
    @commands.command()
    async def eecho(self, ctx, messageid: int, *, content):
        # Check if the user is in the admin list or not
        json = open("../data/admin.json","r")
        jdict = ast.literal_eval(json.read())
        json.close()
        try:
            E = jdict[str(ctx.guild.id)]
        except:
            jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": [], "warnchannel": ""}
        try:
            E = jdict[str(ctx.guild.id)]["admins"].index(str(ctx.author.id))
        except:
            raise commands.MissingPermissions(["admin"]) # Permission denied
        try:
            msg = await ctx.fetch_message(messageid) # Fetch the message using the id
            await msg.edit(content=content) # Replace the message with the text
            await ctx.message.delete() # Delete the author message
        except:
            raise commands.MessageNotFound(str(messageid)) # Message not found exception
# Do these when the cog is loaded
def setup(bot):
    # For manual commands($man)
    bot.cmdlist["bash"] = {
        "intro": "Basically some basic commands.",
        "version": "`version`\nPrint out the version of this bot.",
        "sourcecode": "`sourcecode`\nPrint out the source code.",
        "aboutme": "`aboutme`\nPrint out the profile of the author.",
        "about": "`about <@user>`\nPrint out the profile of the mentioned user.",
        "embed": "`embed <title> <content>`\nExport an embed table with the given title and content",
        "dembed": "`dembed <title> <content>`\nExport an embed table with the given title and content but delete the command message.",
        "eembed": "`eembed <messageid> <title> <content> [Administrator]`\nOverwrite the message with message id with the embed table.",
        "echo": "`echo <content>`\nPrint out the content.",
        "decho": "`decho <content>`\nPrint out the content but delete the command message.",
        "eecho": "`eecho <messageid> <title> <content> [Administrator]`\nOverwrite the message with message id with the embed table.",
        "secho": "`secho <@user> <content>`\nSend a DM to the specified user.",
        "echoimage": "`echoimage <url>`\nExport an embed table with the image.",
        "ping": "`ping`\nPrint out `pong` and return the latency of the bot.",
        "whoamirole": "`whoamid`\nExport all your roles.",
        "temp": "`temp`\nDelete the command message after 2 seconds.",
        "purge": "`purge <number of message> [Administrator]`\nPurge numbers of message.",
        "areact": "`areact <messageid> <emoji>`\nMake the bot react the message using id with the emoji.",
        "sett": "`sett`\nShow the content of config.yml.",
        "rlsett": "`rlsett (sudoers)`\n"
        }
    # Add the cog into the bot
    bot.add_cog(bash(bot))