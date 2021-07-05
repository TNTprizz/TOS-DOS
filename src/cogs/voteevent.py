# Imports
import discord
from discord.ext import commands
# A class called voteevent is ready to be imported as a cog
class voteevent(commands.Cog): # Showing that this is a discord cog
    def __init__(self, bot): # Import the bot
        self.bot = bot # self.bot -> bot
        bot.votelist = {} # Declare the votelist
        bot.multivotelist = {} # Declare the multivotelist
    # Listener which will detect every reaction add
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        bot = self.bot # Get the bot shortcut
        votelist = bot.votelist # Get the vote list
        multivotelist = bot.multivotelist # Get the multivotelist
        emoji = payload.emoji.name # Get the emoji which user reacted
        # Get the message where user reacted
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        try: # If the message is the voteevent, then append the vote option
            if emoji == "✅":
                votelist[int(message.id)][0] = votelist[int(message.id)][0] + 1
            elif emoji == "❎":
                votelist[int(message.id)][1] = votelist[int(message.id)][1] + 1
        except:
            pass
        try: # If the message is the voteevent, then append the vote option
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
        multivotelist = self.bot.multivotelist # Get the multivotelist
        votelist = self.bot.votelist # Get the vote list
        emoji = payload.emoji.name # Get the unreacted emoji name
        # Get the message where the unreact event occur
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        try: # If the message is the voteevent, then deduct the vote option
            if emoji == "✅":
                votelist[int(message.id)][0] = votelist[int(message.id)][0] - 1
            elif emoji == "❎":
                votelist[int(message.id)][1] = votelist[int(message.id)][1] - 1
        except:
            pass
        try: # If the message is the voteevent, then deduct the vote option
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
    # Raise a True-False vote event ($tfvote <content>)
    @commands.command()
    async def tfvote(self, ctx, *, content):
        await ctx.message.delete() # Delete the user message
        msg = await ctx.send(embed = discord.Embed(title="Voting event started!")) # Create and send an embed object
        self.bot.votelist[msg.id] = [-1,-1] # Create a votelist
        await msg.add_reaction("✅") # React to message
        await msg.add_reaction("❎") # Same as above
        await msg.edit( # Edit the message
            embed = discord.Embed(
                title="Voting event started!",
                description=content + "\n\nMessage ID: " + str(msg.id),
                color=discord.Color.blue()
            )
        )
    # End a vote event ($endvote <message id>)
    @commands.command()
    async def endvote(self, ctx, messageid: int):
        bot = self.bot # Get the bot object
        try:
            F = bot.votelist[messageid] # Get the vote list 
            msg = await ctx.fetch_message(messageid) # Fetch the message using message id
            for r in msg.reactions: # Get all the reaction
                await msg.clear_reaction(r.emoji) # Clear all the reaction
            embed = discord.Embed( # Make the embed object
                title="Vote ended!",
                url="http://TNTprizz.zapto.org/dc",
                color=discord.Color.blue(),
                # Append the content together
                description="✅: " + str(F[0]) + "\n❎: " + str(F[1]) + "\n\nJump to message: [↗️](" + msg.jump_url + ")\nMessage ID: " + str(messageid))
            await ctx.send(embed = embed) # Export the embed object
            del bot.votelist[messageid] # Delete the votelist object
            return # Terminate the function
        except:
            try:
                # Construct the argument list
                arglist = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
                messageid = int(messageid) # Convert the message id to integer
                bot.multivotelist[messageid] # Get the multivote object
                msg = await ctx.fetch_message(messageid) # Fetch message using the message id
                for r in msg.reactions: # Get all the reactions
                    await msg.clear_reaction(r.emoji) # Remove them all
                i = 0 # Counter
                con = "" # Content string
                while i != len(bot.multivotelist[messageid]["number"]): # Do this for the length of multivote list times
                    # Append the options together
                    con = con + arglist[i] + ":" + str(bot.multivotelist[messageid]["options"][i]) + " : " + str(bot.multivotelist[messageid]["number"][i]) + "\n"
                    i = i + 1 # Count once
                embed = discord.Embed( # Make the embed object
                    title="Multivote ended!",
                    url="http://TNTprizz.zapto.org/dc",
                    color=discord.Color.blue(),
                    description=con + "\nJump to message: [↗️](" + msg.jump_url + ")\nMessage ID: " + str(messageid)
                )
                await ctx.send(embed = embed) # Export the embed object
                del bot.multivotelist[messageid] # Delete the multivote list
                return
            except: # If it is an invalid message id
                raise commands.BadArgument("'" + str(messageid) + "' is not an invaild message id") # Raise error
    # Raise a multivote event ($multivote <content> <*args>)
    @commands.command(aliases=["mvote"])
    async def multivote(self ,ctx, content: str,*args):
        if len(args) > 10: # If the number of arguments are more than 10
            raise commands.TooManyArguments("More than 10 arguments") # Raise error
        msg = await ctx.send(embed=discord.Embed(title="Loading......")) # Send out an embed object
        arglist = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"] # Construct the arg list
        i = 0 # Count
        con = "" # Content
        self.bot.multivotelist[int(msg.id)] = {"number":[],"options":[]} # Make a multivotelist
        while i != len(args): # Do for the length of the arguments
            await msg.add_reaction(arglist[i]) # Add reaction
            self.bot.multivotelist[int(msg.id)]["number"].append(-1) # Append the value
            self.bot.multivotelist[int(msg.id)]["options"].append(args[i]) # Append the arguments
            i = i + 1 # Count once
        i = 0 # Count again
        while i != len(args): # Do for the length og the arguments
            con = con + arglist[i] + ":" + args[i] + "\n" # Append the options together
            i = i + 1 # Count once
        embed = discord.Embed( # Make the embed object
            title=content,
            url="http://TNTprizz.zapto.org/dc",
            color=discord.Color.blue(),
            description=con + "Message ID:" + str(msg.id)
        )
        await msg.edit(embed = embed) # Export the embed object
# Do when the cog is loaded
def setup(bot):
    bot.cmdlist["voteevent"] = { # Manual list
        "intro": "Commands for voting event.",
        "tfvote": "`vote <content>`\nRaise a voting event on the message with the id provided.",
        "multivote": "`multivote <title> <*args>`\nRaise a multivoting event with the embed.(max. 10)\nAliases: `mvote`",
        "endvote": "`endvote <messageid>`\nEnd a voting event with the message id."
        }
    bot.add_cog(voteevent(bot)) # Add cog into the bot
    