# ~ is the directory where the launch.py is
# This will not be mentioned anymore in the rest of the files.

# Imports
import discord
from discord.ext import commands
import os
import sys
import ast
# The default prefix:
default_prefixes = ['$']
# For changing prefix
async def determine_prefix(bot, message):
    guild = message.guild # Get the guild so that cannot change prefix in DMChannel
    if guild: # If it is not the DMChannel
        return bot.custom_prefixes.get(guild.id, default_prefixes) # Get prefix from the bot.custom_prefixes variable
    else: # If it is a DMChannel
        return default_prefixes # Return the default prefix

intents = discord.Intents().all() # Intents
# Create the bot object.  Prefix changer            replace with $man  intents
bot = commands.Bot(command_prefix=determine_prefix, help_command=None, intents=intents)
bot.ver = "202106181849-Σ21Cog$" # The version of the bot

def restart_program(): # Restart the whole bot
  python = sys.executable # pyhton = the file it is running
  os.execl(python, python, * sys.argv) # Restart the bot
# Restart command ($restart)
@bot.command()
async def restart(ctx): # Define the function
  if ctx.author.id != 469038475371479041: # If user is not @T̸͍͠N̵͓̚T̴̤͘p̷̣̌ř̵̝ì̴͈z̴̗͐z̷̰̒#9487
    raise commands.NotOwner("You are not the owner of this bot")
  await ctx.send("Restarting... Allow up to 5 seconds") # Show the program restarting message.
  print("Caught restart command, restarting......") # Output to terminal
  restart_program() # See line 22
# Import the cogs when the bot is ready (N/A)
@bot.event
async def on_ready(): # Define the function
  for filename in os.listdir('./cogs'): # List all the files in ~/src/cogs
    if filename.endswith('.py'): # If file is a python file
      print("Loaded cog " + filename[:-3] + " from file: " + filename) # Output to terminal
      bot.load_extension(f'cogs.{filename[:-3]}') # Import the Cogs
  bot.playlist = {} # Init for sigma
  bot.songdes = {} # Init for sigma
  print("Bot online!") # Output to terminal if the whole thing is completed
# Prefix command ($prefix [prefix])
@bot.command()
@commands.guild_only() # Cannot execute in DMChannel
async def prefix(ctx, *, prefixes=""): # Define the function
  json = open("../data/admin.json","r") # Open and read ~/data/admin.json
  jdict = ast.literal_eval(json.read()) # Convert from string to dictionary
  json.close() # Close the object to save resources
  try: # Try the following command
    E = jdict[str(ctx.guild.id)] # Check if the guild id exists in the guild list
  except: # If not, then......
   jdict[str(ctx.guild.id)] = {"mutedusers": [], "admins": [], "warnchannel": ""} # Create a new guild field
  try: # Try the following command
    E = jdict[str(ctx.guild.id)]["admins"].index(str(ctx.author.id)) # Check if the author is in the admin list or not
  except: # If not, then......
    raise commands.MissingPermissions(["admin"])
  if prefixes != "": # If prefix field is not empty.
    bot.custom_prefixes[ctx.guild.id] = prefixes.split() or default_prefixes # Store the prefix into the dictionary to make it work 
    await ctx.send("Prefix set to " + prefixes.split()[0]) # Tell the user command execute successfully
    json = open("../data/prefix.json","w") # Open and prepare to write ~/data/prefix.json
    json.write(str(bot.custom_prefixes)) # Write the dictionary to the json file
    json.close() # Close the object to save resources
  else: # If prefix field is empty
    try: # Try the following command
      bot.custom_prefixes[ctx.guild.id] # See if the prefix is stored in the dictionary
    except: # If not, then......
      bot.custom_prefixes[ctx.guild.id] = ["$"] # Give it a new value
    await ctx.send("Prefix of this server: `" + str(bot.custom_prefixes[ctx.guild.id]) + "`") # Show the current prefix of this server

print('No santax exception, running') # tell user that there is no santax error in this file.

bot.cmdlist = {} # For the manual system
# Format:
# {"Example cog":{
#   "Command": "Explaination",
#   "Command": "Explaination",
#   ......
#   },"Example cog":{
#   "Command": "Explaination",
#   "Command": "Explaination",
#   ......
#   }, ......
# }
json = open("../data/prefix.json","r") # Open and prepare to read ~/data/prefix.json
bot.custom_prefixes = ast.literal_eval(json.read()) # Convert it to dictionary and store the value to bot.custom_prefixes
# Format:
# {"guild.id": "prefix",
# "guild.id": "prefix",
# ......
# }
json.close() # Close the object to save resources
token = open("../E.key","r+") # Open and prepare to read ~/E.key
bot.run(token.read()) # Run the bot with the content of ~/E.key
# P.S. You need to touch the ~/E.key and store your bot token in it. Don't ask me anymore!
token.close()
# Close the object to save resources