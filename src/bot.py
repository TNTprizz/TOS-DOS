# ~ is the directory where the launch.py is
# This will not be mentioned anymore in the rest of the files.

# Imports
import discord
from discord.ext import commands
import os
import sys
import ast
import yaml
import time

with open("../config.yml") as f:
  config = yaml.safe_load(f)

# The default prefix:
default_prefixes = [config["default_prefix"]]
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
bot.config = config

def nowtime():
  return time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())

def restart_program(): # Restart the whole bot
  python = sys.executable # pyhton = the file it is running
  os.execl(python, python, * sys.argv) # Restart the bot
# Restart command ($restart)
@bot.command()
async def restart(ctx): # Define the function
  if not ctx.author.id in bot.config["sudoers"]: # If user is not @T̸͍͠N̵͓̚T̴̤͘p̷̣̌ř̵̝ì̴͈z̴̗͐z̷̰̒#9487
    raise commands.NotOwner("You are not the owner of this bot")
  await ctx.send("Restarting... Allow up to 5 seconds") # Show the program restarting message.
  print(nowtime() + "\033[1;37;45m Sys   \033[1;34;40m Caught restart command, restarting......\033[1;37;40m") # Output to terminal
  restart_program() # See line 22
# Import the cogs when the bot is ready (N/A)
@bot.event
async def on_ready(): # Define the function
  for filename in os.listdir('./cogs'): # List all the files in ~/src/cogs
    if filename.endswith('.py'): # If file is a python file
      try:
        bot.load_extension(f'cogs.{filename[:-3]}') # Import the Cogs
        print(nowtime() + "\033[1;37;43m Sys   \033[1;32;40m Loaded cog " + filename[:-3] + " from file: " + filename + "\033[1;37;40m") # Output to terminal
      except Exception:
        print(nowtime() + "\033[1;37;41m Error \033[1;31;40m Cannot load cog " + filename[:-3] + " from file: " + filename + ", ignoring\033[1;37;40m")
  bot.playlist = {} # Init for sigma
  bot.songdes = {} # Init for sigma
  print(nowtime() + "\033[1;37;43m Msg   \033[1;36;40m TOS-DOS is watching you!\033[1;37;40m") # Output to terminal if the whole thing is completed
@bot.event
async def on_message(message):
  if message.content.startswith('$') and not message.content == "$":
    print(nowtime() + "\033[1;37;46m Cmd   \033[1;33;40m Execute command \033[1;32;40m" + message.content + "\033[1;33;40m from \033[1;35;40m" + message.author.display_name + "\033[1;37;40m")
    await bot.process_commands(message)
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

print(nowtime() + "\033[1;37;44m Base  \033[1;33;40m Connecting to Discord API\033[1;37;40m") # tell user that there is no santax error in this file.

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
bot.run(bot.config["token"]) # Run the bot with the content of ~/E.key
# P.S. You need to touch the ~/E.key and store your bot token in it. Don't ask me anymore!