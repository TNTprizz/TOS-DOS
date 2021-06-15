import os
token = open("../E.key","r+")
print("using token:" + token.read())
token.close()
print("Launching the bot, it shoud be online in less than 7 seconds.")
os.chdir("./src")
os.system("python3 bot.py")
