# Imports
import os
token = open("E.key","r+") # Open and prepare to read ~/E.key
print("using token:" + token.read()) # Output the token
token.close() # Close the object to save resources
print("Launching the bot, it shoud be online in less than 7 seconds.") # Output
os.chdir("./src") # Change directory to ~/src/ to launch the bot
os.system("python3 bot.py") # Launch ~/src/bot.py with python3