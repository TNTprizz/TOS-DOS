#imports
import discord
from discord.ext import commands
from random import shuffle
from mechanize import Browser
from youtube_search import YoutubeSearch
from pyyoutube import Api
import os
import youtube_dl
from math import floor
import asyncio
import ast

#youtube_dl config:
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.url = ""
        

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename
#end youtube_dl config
api = Api(api_key="AIzaSyALFRDV_TOgkbiYvcxml47vMxSFt-ynkZQ")

def next(vc,id,bot):
    playlist = bot.playlist
    sourcejson = open("../music/sourcelist.json","r")
    sourcelist = ast.literal_eval(sourcejson.read())
    sourcejson.close()
    if int(len(playlist[id]["queue"])) == playlist[id]["order"]:
        if playlist[id]["loop"]:
            playlist[id]["order"] = 0
        else:
            playlist[id] = {"order":0, "queue":[], "loop":False, "np":""}
            return
    playlist[id]["np"] = playlist[id]["queue"][playlist[id]["order"]]
    vc.play(discord.FFmpegPCMAudio(executable="/bin/ffmpeg", source="../music/" + sourcelist[playlist[id]["np"]]), after=lambda e:next(vc,id))
    playlist[id]["order"] = playlist[id]["order"] + 1

class sigma(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.command(aliases=["m","song","M"])
    async def music(self , ctx, arg: str = "none", *input):
        bot = self.bot
        if not len(input) == 0:
            url = " ".join(input)
        else:
            url = "none"
        serverid = str(ctx.message.guild.id)
        playlist = bot.playlist
        sourcejson = open("../music/sourcelist.json","r")
        sourcelist = ast.literal_eval(sourcejson.read())
        sourcejson.close()
        br = Browser()
        con = ""
        if arg == "connect" or arg == "join":
            if not ctx.message.author.voice:
                await ctx.message.add_reaction("❌")
                return
            else:
                try:
                    channel = ctx.message.author.voice.channel
                    await channel.connect()
                    playlist[serverid] = {"order":0, "queue":[], "loop":False, "np":""}
                    await ctx.message.add_reaction("☑️")
                except:
                    await ctx.message.add_reaction("❌")
        elif arg == "disconnect" or arg == "disco":
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_connected():
                await voice_client.disconnect()
                playlist[serverid] = {"order":0, "queue":[], "loop":False, "np":""}
                await ctx.message.add_reaction("☑️")
            else:
                await ctx.message.add_reaction("❌")
        elif arg == "loop":
            try:
                E = playlist[serverid]
            except KeyError:
                await ctx.message.add_reaction("❌")
                return
            if playlist[serverid]["loop"]:
                playlist[serverid]["loop"] = False
            else:
                playlist[serverid]["loop"] = True
            await ctx.message.add_reaction("🔁")
        elif arg == "search" or arg == "s":
            if url == "none":
                await ctx.message.add_reaction("❌")
                return
            def check(m):
                return m.author == ctx.message.author
            result = YoutubeSearch(url,max_results=10).to_dict()
            i = 0
            while not i == 10:
                con = con + str(i) + ". `" + str(result[i]["title"]) + "` - " + str(result[i]["duration"]) + "\n\n"
                i = i + 1
            embed = discord.Embed(title="Search results of " + url, url="http://tntprizz.zapto.org/dc", description=con, color=discord.Color.blue())
            await ctx.send(embed=embed)
            await ctx.send("Please select your option.")
            try:
                resp = await bot.wait_for('message', check=check, timeout=20)
                opt = int(resp.content)
            except:
                await ctx.message.add_reaction("❌")
                return
            if opt >= 10:
                await ctx.send("You should insert an integer which is 0-9!")
                await ctx.message.add_reaction("❌")
                return
            url = "https://www.youtube.com/" + result[opt]["url_suffix"]
            br.open(url)
            try:
                channel = ctx.message.author.voice.channel
                await channel.connect()
                playlist[serverid] = {"order":0, "queue":[], "loop":False, "np":""}
            except: pass
            playlist[serverid]["queue"].append(br.title())
            server = ctx.message.guild
            voice_channel = server.voice_client
            voice_client = ctx.message.guild.voice_client
            await ctx.send("Downloading files, please wait patiently.")
            async with ctx.typing():
                br.open(url)
                try:
                    E = sourcelist[br.title()]
                except KeyError:
                    source = await YTDLSource.from_url(url, loop=bot.loop)
                    sourcelist[br.title()] = source
                    sourcejson = open("../music/sourcelist.json","w")
                    sourcejson.write(str(sourcelist))
                    sourcejson.close()
                os.system("mv *.m4a ../music/ 2>/dev/null")
                os.system("mv *.webm ../music/ 2>/dev/null")
                os.system("mv *.mp3 ../music/ 2>/dev/null")
                os.system("mv *.part ../music/ 2>/dev/null")
            if voice_client.is_playing() or voice_client.is_paused():
                pass
            else:
                next(voice_channel,serverid,bot)
            await ctx.message.add_reaction("☑️")
        elif arg == "listqueue" or arg == "lq":
            try:
                E = playlist[serverid]
            except KeyError:
                await ctx.message.add_reaction("❌")
                return
            if playlist[serverid]["np"] == "":
                nowp = "Nothing playing now"
            else:
                nowp = playlist[serverid]["np"]
            if not len(playlist[serverid]["queue"]) == 0:
                try:
                    order1 = int(url)
                    order1 = order1 * 10
                except:
                    order1 = floor(int(playlist[serverid]["order"] - 1) / 10) * 10 + 10
                E = playlist[serverid]["queue"][int(order1 - 10):int(order1)]
                con = "\n".join(E)
                con = "\n== Contents ==\n" + con + ""
            else:
                con = ""
                order1 = 10
            await ctx.send("```asciidoc\n== Now playing ==\n" + nowp + con + "\n\n" + "current page:" + str(order1 / 10) +"\nPosition:" + str(playlist[serverid]["order"]) + "/" + str(len(playlist[serverid]["queue"])) + "\nloop:" + str(playlist[serverid]["loop"]) + "```")
        elif arg == "apl" or arg == "addplaylist":
            if url == "none":
                await ctx.message.add_reaction("❌")
                return
            try:
                channel = ctx.message.author.voice.channel
                await channel.connect()
                playlist[serverid] = {"order":0, "queue":[], "loop":False, "np":""}
            except: pass
            server = ctx.message.guild
            voice_channel = server.voice_client
            voice_client = ctx.message.guild.voice_client
            listid = url.split("list=")[1].split("&")[0]
            plist = api.get_playlist_items(playlist_id=listid, count=None).items
            vid = plist[0].to_dict()["snippet"]["resourceId"]["videoId"]
            vurl = "https://www.youtube.com/watch?v=" + vid
            await ctx.send("adding list into queue, please wait very patiently.")
            if voice_client.is_playing() or voice_client.is_paused():
                i = 0
            else:
                async with ctx.typing():
                    br.open(vurl)
                    try:
                        E = sourcelist[br.title()]
                    except KeyError:
                        source = await YTDLSource.from_url(vurl, loop=bot.loop)
                        sourcelist[br.title()] = source
                        sourcejson = open("../music/sourcelist.json","w")
                        sourcejson.write(str(sourcelist))
                        sourcejson.close()
                    os.system("mv *.m4a ../music/ 2>/dev/null")
                    os.system("mv *.webm ../music/ 2>/dev/null")
                    os.system("mv *.mp3 ../music/ 2>/dev/null")
                playlist[serverid]["queue"].append(br.title())
                playlist[serverid]["np"] = playlist[serverid]["queue"][playlist[serverid]["order"]]
                voice_channel.play(discord.FFmpegPCMAudio(executable="/bin/ffmpeg", source="../music/" + sourcelist[playlist[serverid]["np"]]), after=lambda e:next(voice_channel,serverid,bot))
                playlist[serverid]["order"] = playlist[serverid]["order"] + 1
                i = 1
            async with ctx.typing():
                while not i == len(plist):
                    try:
                        vid = plist[i].to_dict()["snippet"]["resourceId"]["videoId"]
                        vurl = "https://www.youtube.com/watch?v=" + vid
                        br.open(vurl)
                        try:
                            E = sourcelist[br.title()]
                        except KeyError:
                            source = await YTDLSource.from_url(vurl, loop=bot.loop)
                            sourcelist[br.title()] = source
                            sourcejson = open("../music/sourcelist.json","w")
                            sourcejson.write(str(sourcelist))
                            sourcejson.close()
                        os.system("mv *.m4a ../music/ 2>/dev/null")
                        os.system("mv *.webm ../music/ 2>/dev/null")
                        os.system("mv *.mp3 ../music/ 2>/dev/null")
                        playlist[serverid]["queue"].append(br.title())
                    except:
                        await ctx.send("Something went wrong, ignoring......")
                    i = i + 1
            await ctx.message.add_reaction("☑️")
        elif arg == "queue" or arg == "q" or arg == "play" or arg == "p":
            if url == "none":
                await ctx.message.add_reaction("❌")
                return
            try:
                channel = ctx.message.author.voice.channel
                await channel.connect()
                playlist[serverid] = {"order":0, "queue":[], "loop":False, "np":""}
            except: pass
            try:
                server = ctx.message.guild
                voice_channel = server.voice_client
                voice_client = ctx.message.guild.voice_client
                await ctx.send("Downloading files, please wait patiently.")
                async with ctx.typing():
                    br.open(url)
                    try:
                        E = sourcelist[br.title()]
                    except KeyError:
                        source = await YTDLSource.from_url(url, loop=bot.loop)
                        sourcelist[br.title()] = source
                        sourcejson = open("../music/sourcelist.json","w")
                        sourcejson.write(str(sourcelist))
                        sourcejson.close()
                    os.system("mv *.m4a ../music/ 2>/dev/null")
                    os.system("mv *.webm ../music/ 2>/dev/null")
                    os.system("mv *.mp3 ../music/ 2>/dev/null")
                playlist[serverid]["queue"].append(br.title())
                if voice_client.is_playing() or voice_client.is_paused():
                    pass
                else:
                    next(voice_channel,serverid,bot)
                await ctx.message.add_reaction("☑️")
            except Exception():
                del playlist[serverid]["queue"][len(playlist[serverid]["queue"])]
                await ctx.send("This is an invaild url. Please use Youtube link.")
                await ctx.message.add_reaction("❌")
        elif arg == "shuffle":
            try:
                E = playlist[serverid]
            except KeyError:
                await ctx.message.add_reaction("❌")
                return
            cp = playlist[serverid]["queue"][int(playlist[serverid]["order"]):]
            shuffle(cp)
            playlist[serverid]["queue"][int(playlist[serverid]["order"]):] = cp
            await ctx.message.add_reaction("🔀")
        elif arg == "pause":
            try:
                E = playlist[serverid]
            except KeyError:
                await ctx.message.add_reaction("❌")
                return
            try:
                voice_client = ctx.message.guild.voice_client
                if voice_client.is_playing():
                    await ctx.message.add_reaction("⏯")
                    await voice_client.pause()
                else:
                    await ctx.send("The bot is not playing anything at the moment.")
            except: pass
        elif arg == "resume":
            try:
                E = playlist[serverid]
            except KeyError:
                await ctx.message.add_reaction("❌")
                return
            try:
                voice_client = ctx.message.guild.voice_client
                if voice_client.is_paused():
                    await ctx.message.add_reaction("⏯")
                    await voice_client.resume()
                else:
                    await ctx.send("The bot was not playing anything before this. Use play command")
            except: pass
        elif arg == "skip":
            try:
                E = playlist[serverid]
            except KeyError:
                await ctx.message.add_reaction("❌")
                return
            try:
                voice_client = ctx.message.guild.voice_client
                if voice_client.is_playing():
                    await ctx.message.add_reaction("⏭️")
                    await voice_client.stop()
                else:
                    await ctx.send("The bot is not playing anything at the moment.")
            except:
                pass
        elif arg == "stop":
            try:
                E = playlist[serverid]
            except KeyError:
                await ctx.message.add_reaction("❌")
                return
            playlist[serverid] = {"order":0, "queue":[], "loop":False, "np":""}
            try:
                voice_client = ctx.message.guild.voice_client
                if voice_client.is_playing():
                    await ctx.message.add_reaction("⏹️")
                    await voice_client.stop()
                    playlist[serverid] = {"order":0, "queue":[], "loop":False, "np":""}
                else:
                    await ctx.message.add_reaction("❌")
            except: pass
        else:
            await ctx.message.add_reaction("❌")
        sourcejson = open("../music/sourcelist.json","w")
        sourcejson.write(str(sourcelist))
        sourcejson.close()


def setup(bot):
    bot.cmdlist["sigma"] = {
        "intro": "Commands for playing musics.",
        "music": "`$music <command> (*input)`\nPlays music. Here are the usages:\n"
        "`$music join`:Join the music channel where the user is;\n"
        "`$music leave`:Leave the music channel where the bot is;\n"
        "`$music loop`:Toggle the loop funcion;\n"
        "`$music shuffle`:Shuffle the queue;\n"
        "`$music search <*args>`:Search music from youtube;\n"
        "`$music listqueue (page)`:List the music queue;\n"
        "`$music addplaylist <url>`:Add the playlist into the queue.\n"
        "`$music play <url>`:Add the song into the queue.\n"
        "`$music pause`:Pause the current track.\n"
        "`$music resume`:Resume the current track.\n"
        "`$music skip`:Skip the current track.\n"
        "`$music stop`:Stop the current track and clear the whole queue.\n"
        "aliases: `m` `song` `M`"
        }
    bot.playlist = {}
    bot.add_cog(sigma(bot))
    