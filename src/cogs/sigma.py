# Imports
import sys
import discord
from discord.ext import commands
from discord.utils import get
from random import shuffle
from youtube_search import YoutubeSearch
import pytube
import pafy
import youtube_dl
import time
from io import StringIO
import asyncio
from contextlib import redirect_stderr, redirect_stdout
from math import floor

# FFmpeg options that it will reconnect if timeout
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# YoutubeDL options
ydl_opts = {'format': 'bestaudio'}

# A small function which convert seconds to a time format
def timeconvert(sec:int):
    hour = floor(sec / 3600)
    if hour <= 9:
        hour = "0" + str(hour)
    hour = str(hour)
    min = floor(floor(sec % 3600) / 60)
    if min <= 9:
        min = "0" + str(min)
    min = str(min)
    sec = sec % 3600 % 60
    if sec <= 9:
        sec = "0" + str(sec)
    sec = str(sec)
    return str(hour + ":" + min + ":" + sec) # Return a string

# Next function which will be done when the music ends
def next(vc,guild,bot):
    if len(bot.playlist[guild.id]["queue"]) <= bot.playlist[guild.id]["order"]: # If it reach the end of the queue
        if bot.playlist[guild.id]["loop"]: # If loop is true
            bot.playlist[guild.id]["order"] = 0 # Back to the first track
        else: # If not looping
            bot.playlist[guild] = {"order" : 0, "np" : "", "queue" : [], "loop": False, "startime": None} # Reset the playlist
            return # Terminate the whole thing
    voice = get(vc, guild=guild) # Get the voice channel the user is in
    output = StringIO() # Prepare to resirect output
    err = StringIO()
    with redirect_stdout(output):
        with redirect_stderr(output): # Redirect output to output variable
            with youtube_dl.YoutubeDL(ydl_opts) as ydl: # Open YoutubeDL as ydl
                # Download the bytes of the song
                info = ydl.extract_info(bot.playlist[guild.id]["queue"][bot.playlist[guild.id]["order"]], download=False)
    # Get the time tick when music start
    bot.playlist[guild.id]["startime"] = floor(time.time())
    # Play the audio using FFmpeg
    with redirect_stderr(err):
        with redirect_stdout(output):
            voice.play(discord.FFmpegPCMAudio(info["url"],**ffmpeg_options), after=lambda e:next(vc, guild, bot))
    # Set now playing to the currently playing song
    bot.playlist[guild.id]["np"] = bot.playlist[guild.id]["queue"][bot.playlist[guild.id]["order"]]
    bot.playlist[guild.id]["order"] = bot.playlist[guild.id]["order"] + 1 # Order += 1

# A new class called sigma is ready to be imported as a cog
class sigma(commands.Cog): # Show that it is a discord cog object
    def __init__(self, bot): # Import the bot
        self.bot = bot # self.bot = bot
    # Join a voice channel ($join)
    @commands.guild_only()
    @commands.command(aliases=["connect"])
    async def join(self, ctx):
        await ctx.author.voice.channel.connect() # Connect to the voice channel where the user is
        # Set up a playlist object
        self.bot.playlist[ctx.guild.id] = {"order" : 0, "np" : "", "queue" : [], "loop": False, "startime": None}
        await ctx.message.add_reaction("☑️") # React if success
    # Leave a voice channel ($leave)
    @commands.guild_only()
    @commands.command(aliases=["dc","disconnect","disco"])
    async def leave(self, ctx):
        await ctx.voice_client.disconnect() # Disconnect from the voice channel
        # Reset a playlist object
        self.bot.playlist[ctx.guild.id] = {"order" : 0, "np" : "", "queue" : [], "loop": False, "startime": None}
        await ctx.message.add_reaction("☑️") # React if success
    # Loop the queue ($loopqueue)
    @commands.guild_only()
    @commands.command(aliases=["lq", "loop"])
    async def loopqueue(self, ctx):
        if self.bot.playlist[ctx.guild.id]["loop"]: # If loop is true
            self.bot.playlist[ctx.guild.id]["loop"] = False # loop = false
        else: # If not loop is true
            self.bot.playlist[ctx.guild.id]["loop"] = True # loop = true
        await ctx.message.add_reaction("🔁") # React if success
    # Show the queue ($queue)
    @commands.guild_only()
    @commands.command(aliases=["q"])
    async def queue(self, ctx, page = "NG"):
        if not len(self.bot.playlist[ctx.guild.id]["queue"]) == 0: # If the length of the queue is not 0
            try: # Try to do
                order1 = int(page) # If page value is valid
                order1 = order1 * 10 # Set the page value
            except: # If the page value is not valid
                # Set the page to where the track playing now is
                order1 = floor(int(self.bot.playlist[ctx.guild.id]["order"] - 1) / 10) * 10 + 10
            E = self.bot.playlist[ctx.guild.id]["queue"][int(order1 - 10):int(order1)] # Get the list of the range of the page
            con = "" # Declare a string object
            ro = order1 - 10
            for link in E: # List out all the links
                # Append the title and the duration together
                if ro == self.bot.playlist[ctx.guild.id]["order"] - 1:
                    con = con + "= " + str(ro) + ". " + self.bot.songdes[link]["title"] + " - " + timeconvert(floor(time.time() - self.bot.playlist[ctx.guild.id]["startime"])) + "/" + timeconvert(self.bot.songdes[link]["duration"]) + "\n"
                elif ro > self.bot.playlist[ctx.guild.id]["order"] - 1:
                    con = con + "* " + str(ro) + ". " + self.bot.songdes[link]["title"] + " - " + timeconvert(self.bot.songdes[link]["duration"]) + "\n"
                else:
                    con = con + "- " + str(ro) + ". " + self.bot.songdes[link]["title"] + " - " + timeconvert(self.bot.songdes[link]["duration"]) + "\n"
                ro = ro + 1
            # Add some decoration
            con = "\n[ Queue ]\n" + con + ""
        else: # If the length of the queue is 0
            con = "" # Needed cuz needed
            order1 = 10 # Needed cuz needed
        duration = 0 # Declare an integer
        for dir in self.bot.playlist[ctx.guild.id]["queue"]: # Get the whole duration of the playlist
            duration = int(duration) + int(floor(self.bot.songdes[dir]["duration"]))
        # Append the values together
        await ctx.send("```asciidoc\n" + con + "\nTotal duration: " + timeconvert(duration) + "\n" + "current page:" + str(order1 / 10) +"\nPosition:" + str(self.bot.playlist[ctx.guild.id]["order"] - 1) + "/" + str(len(self.bot.playlist[ctx.guild.id]["queue"])) + "\nloop:" + str(self.bot.playlist[ctx.guild.id]["loop"]) + "```")
    # Shuffle the queue ($shuffle)
    @commands.guild_only()
    @commands.command()
    async def shuffle(self, ctx):
        # Get the unplayed part of the queue
        cp = self.bot.playlist[ctx.guild.id]["queue"][int(self.bot.playlist[ctx.guild.id]["order"]):]
        shuffle(cp) # Shuffle the unplayed part of the queue
        # Append them together again
        self.bot.playlist[ctx.guild.id]["queue"][int(self.bot.playlist[ctx.guild.id]["order"]):] = cp
        await ctx.message.add_reaction("🔀") # React when succeed
    # Play a youtube audio or a playlist ($play <url>)
    @commands.guild_only()
    @commands.command()
    async def play(self, ctx, *,url:str):
        try: # Try to connect to the voice channel where the user is
            await ctx.author.voice.channel.connect()
            # Reset the playlist
            self.bot.playlist[ctx.guild.id] = {"order" : 0, "np" : "", "queue" : [], "loop": False, "startime": None}
        except: pass
        # If not connected in a voice channel
        if not get(ctx.bot.voice_clients, guild=ctx.guild).is_connected():
            raise Exception("Not connected to a voice channel") # Raise exception
        msg = await ctx.send(embed=discord.Embed( # Create a temperatory added embed
            title="Processing, please wait."
        ))
        try:
            plist = pytube.Playlist(url) # Get the playlist of the url
            timez = 0 # Declare an integer to count
        except:
            vid = pytube.YouTube(url) # Get the video of the url
            self.bot.playlist[ctx.guild.id]["queue"].append(url) # Append the url into the queue
            vid = pafy.new(url)
            self.bot.songdes[url] = {"title" : vid.title, "duration": int(vid.duration), "thumb": vid.thumb} # Get the title and the duration of the track
            voice_client = ctx.message.guild.voice_client # Get the voice client
            if not voice_client.is_playing() and not voice_client.is_paused(): # If the bot isn't playing anything
                next(self.bot.voice_clients, ctx.guild, self.bot) # Toggle the next function to start play music
            embed = discord.Embed( # Make the embed object
                title="Added track into queue",
                color=discord.Color.gold(),
                description="Added `" + vid.title + "` Into queue." # Tell user that the process is completed
            )
            # Set the thumbnail to the avatar of the video
            embed.set_thumbnail(url=vid.thumb)
        else:
            for URL in plist: # List all the link in the playlist
                vid = pafy.new(URL) # Get the video object
                self.bot.songdes[URL] = {"title" : vid.title, "duration": int(vid.length), "thumb": vid.thumb} # Get the title and the duration of the track
                self.bot.playlist[ctx.guild.id]["queue"].append(URL) # Append the links into the queue
                await msg.edit(embed=discord.Embed( # Edit the embed to prevent timeout error
                    title="Procesing, please wait.\nDownloaded:" + str(timez) # (And force it to response to commands)
                ))
                
                if not ctx.message.guild.voice_client.is_playing() and not ctx.message.guild.voice_client.is_paused(): # If the bot isn't playing anything
                    next(self.bot.voice_clients, ctx.guild, self.bot) # Toggle the next function to start play music
                timez = timez + 1 # timez =+ 1
            embed = discord.Embed( # Create an embed object
                title="Added playlist into queue",
                color=discord.Color.gold(), # Tell user that the process is completed
                description="Added " + str(len(plist)) + " tracks into queue\nName of playlist: `" + plist.title + "`"
            )
            # Set the thumbnail to the avatar of the first video
            embed.set_thumbnail(url=self.bot.songdes[self.bot.playlist[ctx.guild.id]["queue"][0]]["thumb"])
        await msg.edit(embed=embed) # Export the embed table
        await ctx.message.add_reaction("☑️") # React if success
    # Show what is playing now ($nowplaying)
    @commands.guild_only()
    @commands.command(aliases=["np","nowplay","playingnow"])
    async def nowplaying(self, ctx):
        voice_client = ctx.message.guild.voice_client # Get the voice client
        if not voice_client.is_playing() and not voice_client.is_paused():
            raise Exception("Nothing playing now.")
        try: # Try to get the video url and youtube video object
            url = self.bot.playlist[ctx.guild.id]["queue"][self.bot.playlist[ctx.guild.id]["order"] - 1]
            des = self.bot.songdes[url]
            thumb = des["thumb"]
        except: # If it cannot
            raise Exception("The bot is not playing anything at the moment.") # Raise error
        ctime = floor(time.time()) # Get current time tick
        etime = floor(ctime - self.bot.playlist[ctx.guild.id]["startime"]) # Get the eliapsed time
        try:
            etime = floor(self.bot.playlist[ctx.guild.id]["pausetime"] - self.bot.playlist[ctx.guild.id]["startime"])
        except: pass
        barnum = int(round((etime / des["duration"]) * 40)) # Get the percentage
        i = 0 # Declare an integer
        bar = "" # Declare a string
        while i != 40: # Run for 41 times to get the progress bar
            if barnum < i:
                bar = bar + "-"
            elif barnum > i:
                bar = bar + "="
            else:
                bar = bar + ">"
            i = i + 1
        embed = discord.Embed( # Make an embed object
            title="Now Playing",
            color=discord.Color.gold(),
            description="[**" + des["title"] + "**](" + url + ")\n" + timeconvert(etime) + " / " + timeconvert(des["duration"]) + "\n`" + bar + "`"
        )
        # Set thumbnail to the avatar of the video
        embed.set_thumbnail(url=thumb)
        await ctx.send(embed = embed) # Export the embed object
    # Search for songs($search <arguments>)
    @commands.guild_only()
    @commands.command()
    async def search(self, ctx, *, stuffs: str):
        try: # Try to do
            await ctx.author.voice.channel.connect() # Connect to the voice channel where the user is
            # Reset the playlist
            self.bot.playlist[ctx.guild.id] = {"order" : 0, "np" : "", "queue" : [], "loop": False, "startime": None}
        except: pass
        # If not connected to voice channel
        if not get(ctx.bot.voice_clients, guild=ctx.guild).is_connected():
            raise Exception("Not connected to a voice channel") # Raise exception
        def check(m): # Define the check function
            return m.author == ctx.message.author
        result = YoutubeSearch(stuffs,max_results=10).to_dict() # Search the stuffs and export the results to dictionary
        con = "" # Declare a string
        i = 0 # Declare an integer
        for res in result: # List all the result 
            con = con + str(i) + ". `" + str(res["title"]) + "` - " + str(res["duration"]) + "\n\n" # Append the results
            i = i + 1 # Count + 1
        embed = discord.Embed( # Create an embed object
            title="Search results of " + stuffs,
            url="http://tntprizz.zapto.org/dc",
            description=con,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed) # Export the embed object
        await ctx.send("Please select your option.") # Prompt user to insert an integer
        try: # Try to get the message
            resp = await self.bot.wait_for('message', check=check, timeout=20)
            opt = int(resp.content) # Get the number user seleted
        except TimeoutError: # If user cannot insert the number on time
            raise Exception("You cannot insert an integer within 20 seconds! Cancel operation") # Raise exception
        except ValueError: # If user don't insert an integer
            raise ValueError("This is not an integer! Cancel operation") # Raise exception
        if opt >= 10: # If option is larger than 9
            raise ValueError("You should insert an integer within 0 to 9! Cancel operation") # Raise exception
        url = "https://www.youtube.com/" + result[opt]["url_suffix"] # Get the video url
        vid = pafy.new(url) # Get the video object
        self.bot.songdes[url] = {"title" : vid.title, "duration": int(vid.length), "thumb": vid.thumb} # Get the title and the duration of the track
        self.bot.playlist[ctx.guild.id]["queue"].append(URL) # Append the links into the queue
        embed = discord.Embed( # Make an embed object
            title="Added track into queue",
            color=discord.Color.gold(),
            description="Added " + vid.title + " Into queue."
        )
        embed.set_thumbnail(url=vid.thumb) # Set thumbnail to video thumbnail
        voice_client = ctx.message.guild.voice_client # Get the voice client object
        if not voice_client.is_playing() and not voice_client.is_paused(): # If the voice client isn't playing
            next(self.bot.voice_clients, ctx.guild, self.bot) # Start playing song
        await ctx.send(embed=embed) # Export the embed object
        await ctx.message.add_reaction("☑️") # React if success
    # Remove the track using the number of the song ($rmtrack <tracknum>)
    @commands.guild_only()
    @commands.command(aliases = ["rm", "deltrack"])
    async def rmtrack(self, ctx, tracknum : int):
        if tracknum < 0 or tracknum > len(self.bot.playlist[ctx.guild.id]["queue"]): # Check if the number inserted is valid
            raise Exception("Invalid track number") # Raise exception
        # Check if the tracknum is before the order or after the order
        if self.bot.playlist[ctx.guild.id]["order"] - 1 == tracknum:
            ctx.message.guild.voice_client.stop()
        if self.bot.playlist[ctx.guild.id]["order"] - 1 < tracknum:
            del self.bot.playlist[ctx.guild.id]["queue"][tracknum] # Delete the track
        else:
            self.bot.playlist[ctx.guild.id]["order"] = self.bot.playlist[ctx.guild.id]["order"] - 1 # Set order to -1
            del self.bot.playlist[ctx.guild.id]["queue"][tracknum] # Only delete the track
        await ctx.message.add_reaction("☑️") # React if success
    # Skip to track ($skiptotrack <tracknum>)
    @commands.guild_only()
    @commands.command(aliases=["gototrack","jumptotrack","stt"])
    async def skiptotrack(self, ctx, tracknum: int):
        if tracknum < 0 or tracknum > len(self.bot.playlist[ctx.guild.id]["queue"]): # Check if the number inserted is valid
            raise Exception("Invalid track number") # Raise exception
        self.bot.playlist[ctx.guild.id]["order"] = tracknum # Set order to tracknum
        ctx.message.guild.voice_client.stop() # Stop the track to execute the next function
        await ctx.message.add_reaction("☑️") # React if success
    # Pause the currently playing track ($pause)
    @commands.guild_only()
    @commands.command()
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client # Get the voice client
        self.bot.playlist[ctx.guild.id]["pausetime"] = time.time() # Get the time tick when the track paused
        voice_client.pause() # Pause the music
        await ctx.message.add_reaction("⏸") # React if success
    # Resume the paused track ($resume)
    @commands.guild_only()
    @commands.command()
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client # Get the voice client
        # Correcting the $nowplaying elipsed time
        self.bot.playlist[ctx.guild.id]["startime"] = self.bot.playlist[ctx.guild.id]["startime"] + (floor(time.time()) - floor(self.bot.playlist[ctx.guild.id]["pausetime"]))
        del self.bot.playlist[ctx.guild.id]["pausetime"] # Delete the time tick when the track paused
        voice_client.resume() # Resume the music
        await ctx.message.add_reaction("▶️") # React if success
    # Stop the whole playlist ($stop)
    @commands.guild_only()
    @commands.command(aliases=["clear","cq"])
    async def stop(self, ctx):
        self.bot.playlist[ctx.guild.id] = {"order":0, "queue":[], "loop":False, "np":""} # Reset the playlist dictionary
        voice_client = ctx.message.guild.voice_client # Get the voice client
        voice_client.stop() # Stop the music
        await ctx.message.add_reaction("⏹️") # React if success
    # Go to the last track(s) ($last [tracks])
    @commands.guild_only()
    @commands.command(aliases=["back"])
    async def last(self, ctx, tracks: int = 1):
        voice_client = ctx.message.guild.voice_client # Get the voice client
        if self.bot.playlist[ctx.guild.id]["order"] - tracks - 1 < 0: # If the order become smaller than 0
            raise IndexError("Cannot accept order value smaller than 0") # Raise exception
        # Set order to the modified order
        self.bot.playlist[ctx.guild.id]["order"] = self.bot.playlist[ctx.guild.id]["order"] - tracks - 1
        voice_client.stop() # Stop the player to let it execute the next function
        await ctx.message.add_reaction("⏮️") # React if success
    # Skip the track(s) ($skip [tracks])
    @commands.guild_only()
    @commands.command(aliases=["next"])
    async def skip(self, ctx, tracks: int = 1):
        voice_client = ctx.message.guild.voice_client # Get the voice client
        # If the order become larger then the length of the queue
        if self.bot.playlist[ctx.guild.id]["order"] + tracks - 1 == len(self.bot.playlist[ctx.guild.id]["queue"]):
            raise IndexError("Cannot accept order value bigger than the length of the queue") # Raise exception
        # Set order to the modified order
        self.bot.playlist[ctx.guild.id]["order"] = self.bot.playlist[ctx.guild.id]["order"] + tracks - 1
        voice_client.stop() # Stop the player to let it execute the next function
        await ctx.message.add_reaction("⏭️") # React if success
    
def setup(bot):
    bot.cmdlist["sigma"] = { # Import the manual list
        "intro": "Music player version 2",
        "join": "`join`\nConnect to the music channel the author is in\nAliases: `connect`",
        "leave": "`leave`\nDisconnect from the music channel\nAliases: `dc` `disco` `disconnect`",
        "loopqueue": "`loopqueue`\nToggle the loop boolean which will loop the queue\nAliases: `lq`",
        "shuffle": "`shuffle`\nShuffle the queue",
        "play": "`play <Youtube URL>`\nPlay the Youtube audio",
        "queue": "`queue [page]`\nShow out the queue\nAliases: `q`",
        "nowplaying": "`nowplaying`\nShow the currently playing track\nAliases: `np` `playingnow` `nowplay`",
        "search": "`search <args>`\nSearch the arguments from youtube and play the seleted audio",
        "pause": "`pause`\nPause the current track",
        "resume": "`resume`\nResume the paused track",
        "stop": "`stop`\nStop playing the whole queue\nAliases: `clear` `cq`",
        "skip": "`skip [tracks]`\nSkip the track(s)\nAliases: `next`",
        "last": "`last [tracks]`\nGo backward for a number of track(s)\nAliases: `back`",
        "rmtrack": "`rmtrack <tracknum>`\nRemove the track using the number\nAliases: `rm` `deltrack`",
        "skiptotrack": "`skiptotrack <tracknum>`\nSkip to the track using the number\nAliases: `gototrack` `jumptotrack` `stt`"
        }
    bot.add_cog(sigma(bot)) # Add cog into the bot
    