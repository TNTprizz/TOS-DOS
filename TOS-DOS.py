# imports
import discord
from discord.ext import commands, tasks
from discord.utils import get
from random import choice, shuffle, randrange
from gpiozero import CPUTemperature
from mechanize import Browser
from youtube_search import YoutubeSearch
from pyyoutube import Api
import psutil
import os
import youtube_dl
from math import floor
import asyncio
import subprocess

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
#basic and global values.

ver = "202106071656-Σ$A1"
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', help_command=None, intents=intents)
status = ['E', 'with 1 user', 'games', 'TOS-DOS', 'music', 'cytus2', 'Myself', 'phigros', 'nothing', '$man all', '$ask', 'maths', 'Dancerail3','MEMZ','Cytus','$about','CentOS','kali-linux','PUBG','Ubuntu','java','python','WannaCry']
ans = ['No, of course', 'Definitely yes!', 'I don\'t know ar', '馬冬甚麼? I cannot hear', 'OK, but why?',
       'This question is totally meaningless','huh?']
secrets = ["I am smiling evily but I am not gay", "I am a cell", "I love my water bottle", "1+1=2", "I am launched forever", "I am not farting", "this is a fact", "E"]
api = Api(api_key="AIzaSyALFRDV_TOgkbiYvcxml47vMxSFt-ynkZQ")

#for music player
def next(vc,id):
    global playlist
    global sourcelist
    if int(len(playlist[id]["queue"])) == playlist[id]["order"]:
        if playlist[id]["loop"]:
            playlist[id]["order"] = 0
        else:
            playlist[id] = {"order":0, "queue":[], "loop":False, "np":""}
            return
    playlist[id]["np"] = playlist[id]["queue"][playlist[id]["order"]]
    vc.play(discord.FFmpegPCMAudio(executable="/bin/ffmpeg", source="music/" + sourcelist[playlist[id]["np"]]), after=lambda e:next(vc,id))
    playlist[id]["order"] = playlist[id]["order"] + 1
    
#music player
@bot.command(aliases=["m","song","M"])
async def music(ctx, arg: str = "none", *input):
    if not len(input) == 0:
        url = " ".join(input)
    else:
        url = "none"
    serverid = ctx.message.guild.id
    global playlist
    global sourcelist
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
            con = con + str(i) + ". `" + result[i]["title"] + "` - " + result[i]["duration"] + "\n\n"
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
        playlist[serverid]["queue"].append(br.title())
        try:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            playlist[serverid] = {"order":0, "queue":[], "loop":False, "np":""}
        except: pass
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_client = ctx.message.guild.voice_client
        await ctx.send("Downloading files, please wait patiently.")
        async with ctx.typing():
            source = await YTDLSource.from_url(url, loop=bot.loop)
            os.system("mv *.m4a ./music/ 2>/dev/null")
            os.system("mv *.webm ./music/ 2>/dev/null")
            os.system("mv *.mp3 ./music/ 2>/dev/null")
            os.system("mv *.part ./music/ 2>/dev/null")
        sourcelist[br.title()] = source
        if voice_client.is_playing() or voice_client.is_paused():
            pass
        else:
            next(voice_channel,serverid)
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
                source = await YTDLSource.from_url(vurl, loop=bot.loop)
                os.system("mv *.m4a ./music/ 2>/dev/null")
                os.system("mv *.webm ./music/ 2>/dev/null")
                os.system("mv *.mp3 ./music/ 2>/dev/null")
                os.system("mv *.part ./music/ 2>/dev/null")
            br.open(vurl)
            playlist[serverid]["queue"].append(br.title())
            sourcelist[br.title()] = source
            playlist[serverid]["np"] = playlist[serverid]["queue"][playlist[serverid]["order"]]
            voice_channel.play(discord.FFmpegPCMAudio(executable="/bin/ffmpeg", source="./music/" + sourcelist[playlist[serverid]["np"]]), after=lambda e:next(voice_channel,serverid))
            playlist[serverid]["order"] = playlist[serverid]["order"] + 1
            i = 1
        async with ctx.typing():
            while not i == len(plist):
                try:
                    vid = plist[i].to_dict()["snippet"]["resourceId"]["videoId"]
                    vurl = "https://www.youtube.com/watch?v=" + vid
                    source = await YTDLSource.from_url(vurl, loop=bot.loop)
                    os.system("mv *.m4a ./music/ 2>/dev/null")
                    os.system("mv *.webm ./music/ 2>/dev/null")
                    os.system("mv *.mp3 ./music/ 2>/dev/null")
                    os.system("mv *.part ./music/ 2>/dev/null")
                    br.open(vurl)
                    playlist[serverid]["queue"].append(br.title())
                    sourcelist[br.title()] = source
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
                source = await YTDLSource.from_url(url, loop=bot.loop)
                os.system("mv *.m4a ./music/ 2>/dev/null")
                os.system("mv *.webm ./music/ 2>/dev/null")
                os.system("mv *.mp3 ./music/ 2>/dev/null")
                os.system("mv *.part ./music/ 2>/dev/null")
            br.open(url)
            playlist[serverid]["queue"].append(br.title())
            sourcelist[br.title()] = source
            if voice_client.is_playing() or voice_client.is_paused():
                pass
            else:
                next(voice_channel,serverid)
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


#change present per 1 minute.
@tasks.loop(minutes=1)
async def chpre():
    await bot.change_presence(activity=discord.Game(name=choice(status)))
#clear temp data per 24 hours.
@tasks.loop(hours=24)
async def clear():
    temprecord = open("temprecord", "w")
    temprecord.close()
#inits and debug values when bot opened
@bot.event
async def on_ready():
    os.system("rm -rf ./music/*.m4a")
    os.system("rm -rf ./music/*.webm")
    os.system("rm -rf ./music/*.mp3")
    os.system("rm -rf ./music/*.part")
    global playlist
    playlist = {}
    global exitcode
    exitcode = 0
    global server
    server = None
    global sourcelist
    sourcelist = {}
    global votelist
    votelist = {}
    global multivotelist
    multivotelist = {}
    global votehuman
    votehuman = []
    chpre.start()
    clear.start()
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    print("version: " + ver)
#exceptions
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="E! You typed in a wrong command!!!",
                              url="http://tntprizz.zapto.org/dc",
                              description="Use `$man all` for a list of commands.",
                              color=discord.Color.red())
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="E! You missed some arguments!",
                              url="http://tntprizz.zapto.org/dc",
                              description="You may run `$man <command>` for further help.",
                              color=discord.Color.red())
    elif isinstance(error, commands.TooManyArguments):
        embed = discord.Embed(title="E! You typed in too many arguments!!",
                              url="http://tntprizz.zapto.org/dc",
                              description="You may use `''` to state one argument with blankspace\n"
                                          "or run `$man <command>` for further help.",
                              color=discord.Color.red())
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title="E! You typed in bad argument!",
                              url="http://tntprizz.zapto.org/dc",
                              description="You should use the correct arguement\n"
                                          "or run `$man <command>` for further help.",
                              color=discord.Color.red())
    elif isinstance(error, KeyError):
        embed = discord.Embed(title="E! I am not in the voice channel!!!",
                              url="http://tntprizz.zapto.org/dc",
                              description="You should let the bot join voice channel first!\n"
                                          "run `$man music` for further help.",
                              color=discord.Color.red())
    else:
        embed = discord.Embed(title="E! Something went wrong!",
                              url="http://tntprizz.zapto.org/dc",
                              description="try use `$man <command>` for help.",
                              color=discord.Color.red())
    embed.add_field(name="Debug:",value=str(error))
    await ctx.send(embed=embed)
#for voting events
@bot.event
async def on_raw_reaction_add(payload):
    global votelist
    global multivotelist
    emoji = payload.emoji.name
    user = payload.member
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    try:
        E = votelist[int(message.id)][2].index(user.id)
    except KeyError:
        pass
    except ValueError:
        if emoji == "✅":
            votelist[int(message.id)][0] = votelist[int(message.id)][0] + 1
        elif emoji == "❎":
            votelist[int(message.id)][1] = votelist[int(message.id)][1] + 1
        votelist[int(message.id)][2].append(user.id)
        return
    try:
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
    if str(message.id) == "851739300882022420":
        channel = message.channel
        guild = channel.guild
        if emoji == "🔴":
            await user.add_roles(get(guild.roles, id=851712411428847656))
        elif emoji == "🟠":
            await user.add_roles(get(guild.roles, id=851712474096336897))
        elif emoji == "🟡":
            await user.add_roles(get(guild.roles, id=851712584481505320))
        elif emoji == "🟢":
            await user.add_roles(get(guild.roles, id=851712725125693441))
        elif emoji == "🔵":
            await user.add_roles(get(guild.roles, id=851712701632610357))
        elif emoji == "🟣":
            await user.add_roles(get(guild.roles, id=851712642602893342))
        elif emoji == "🟤":
            await user.add_roles(get(guild.roles, id=851723029959802890))
        elif emoji == "⚪":
            await user.add_roles(get(guild.roles, id=851723170226503720))
        elif emoji == "⚫":
            await user.add_roles(get(guild.roles, id=851723283236782110))
        elif emoji == "🌎":
            await user.add_roles(get(guild.roles, id=851723379646922753))
        else:
            pass
    elif str(message.id) == "851744658659868702":
        channel = message.channel
        guild = channel.guild
        if emoji == "💻":
            await user.add_roles(get(guild.roles, id=851719683446669352))
        elif emoji == "🕺":
            await user.add_roles(get(guild.roles, id=851719744763854879))
        elif emoji == "♂️":
            await user.add_roles(get(guild.roles, id=851743689919037460))
        else:
            pass
@bot.event
async def on_raw_reaction_remove(payload):
    global multivotelist
    emoji = payload.emoji.name
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    channel = message.channel
    guild = channel.guild
    user = get(guild.members, id=payload.user_id)
    try:
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
    if str(message.id) == "851739300882022420":
        if emoji == "🔴":
            await user.remove_roles(get(guild.roles, id=851712411428847656))
        elif emoji == "🟠":
            await user.remove_roles(get(guild.roles, id=851712474096336897))
        elif emoji == "🟡":
            await user.remove_roles(get(guild.roles, id=851712584481505320))
        elif emoji == "🟢":
            await user.remove_roles(get(guild.roles, id=851712725125693441))
        elif emoji == "🔵":
            await user.remove_roles(get(guild.roles, id=851712701632610357))
        elif emoji == "🟣":
            await user.remove_roles(get(guild.roles, id=851712642602893342))
        elif emoji == "🟤":
            await user.remove_roles(get(guild.roles, id=851723029959802890))
        elif emoji == "⚪":
            await user.remove_roles(get(guild.roles, id=851723170226503720))
        elif emoji == "⚫":
            await user.remove_roles(get(guild.roles, id=851723283236782110))
        elif emoji == "🌎":
            await user.remove_roles(get(guild.roles, id=851723379646922753))
        else:
            pass
    if str(message.id) == "851744658659868702":
        if emoji == "💻":
            await user.remove_roles(get(guild.roles, id=851719683446669352))
        elif emoji == "🕺":
            await user.remove_roles(get(guild.roles, id=851719744763854879))
        elif emoji == "♂️":
            await user.remove_roles(get(guild.roles, id=851743689919037460))
        else:
            pass
@bot.event
async def on_member_join(user):
    if user.guild.id != 800679086955167775:
        return
    guild = user.guild
    await user.add_roles(get(guild.roles, id=800681780834992129))
    message = await bot.get_channel(800679087541583944).fetch_message(827789950606901309)
    channel = message.channel
    embed = discord.Embed(title="Welcome new user!",url="http://TNTprizz.zapto.org/dc",color=discord.Color.blue(),description="Welcome " + user.mention + " !\nHope you enjoy staying in this server!")
    await channel.send(embed=embed)
    await channel.send(file=discord.File('welcome.gif'))
@bot.command()
async def vote(ctx, messageid: int):
    global votelist
    await ctx.message.delete()
    msg = await ctx.fetch_message(messageid)
    await msg.add_reaction("✅")
    await msg.add_reaction("❎")
    votelist[messageid] = [0,-1,[]]
@bot.command()
async def endvote(ctx, messageid: int):
    try:
        global votelist
        F = votelist[messageid]
        msg = await ctx.fetch_message(messageid)
        embed = discord.Embed(title="Vote ended!",url="http://TNTprizz.zapto.org/dc",color=discord.Color.blue(),description="✅: " + str(F[0]) + "\n❎: " + str(F[1]) + "\nMessage id:" + str(messageid))
        await msg.reply(embed = embed)
        del votelist[messageid]
        return
    except:
        try:
            arglist = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            global multivotelist
            messageid = int(messageid)
            F = multivotelist[messageid]
            msg = await ctx.fetch_message(messageid)
            await msg.edit(embed=discord.Embed(title="Multivoting event ended!",url="http://TNTprizz.zapto.org/dc",color=discord.Color.blue(),description="This event is expired, better luck next time!"))
            i = 0
            con = ""
            while i != len(multivotelist[messageid]["number"]):
                con = con + arglist[i] + ":" + str(multivotelist[messageid]["options"][i]) + " : " + str(multivotelist[messageid]["number"][i]) + "\n"
                i = i + 1
            embed = discord.Embed(title="Multivote ended!",url="http://TNTprizz.zapto.org/dc",color=discord.Color.blue(),description=con + "\nMessage id:" + str(messageid))
            await msg.reply(embed = embed)
            del multivotelist[messageid]
            return
        except:
            await ctx.message.add_reaction("❌")
@bot.command()
async def multivote(ctx, content: str,*args):
    msg = await ctx.send(embed=discord.Embed(title="Loading......",url="http://TNTprizz.zapto.org/dc"))
    if len(args) > 10:
        await ctx.message.add_reaction("❌")
        return
    arglist = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    i = 0
    con = ""
    global multivotelist
    multivotelist[int(msg.id)] = {"number":[],"options":[]}
    while i != len(args):
        await msg.add_reaction(arglist[i])
        multivotelist[int(msg.id)]["number"].append(-1)
        multivotelist[int(msg.id)]["options"].append(args[i])
        i = i + 1
    i = 0
    while i != len(args):
        con = con + arglist[i] + ":" + args[i] + "\n"
        i = i + 1
    embed = discord.Embed(title=content,url="http://TNTprizz.zapto.org/dc",color=discord.Color.blue(),description=con + "Message ID:" + str(msg.id))
    await msg.edit(embed = embed)
#this is still beta
@bot.command()
async def test(ctx):
    await ctx.send("You serious? This is not beta bash.")
@bot.command()
@commands.has_role('Administrator')
async def warn(ctx, user: discord.User,*reason):
    message = await bot.get_channel(851784439204675584).fetch_message(851784867066282057)
    channel = message.channel
    reason = " ".join(reason)
    embed = discord.Embed(title=user.name + " is WARNED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nFrom " + ctx.author.mention)
    await ctx.send(embed=embed)
    embed = discord.Embed(title="You are warned",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Reason:" + reason + "\nFrom " + ctx.author.mention)
    await user.send(embed=embed)
    embed = discord.Embed(title=user.name + " is WARNED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
    await channel.send(embed=embed)
@bot.command()
@commands.has_role("Administrator")
async def kick(ctx, user: discord.Member, *reason):
    message = await bot.get_channel(851784439204675584).fetch_message(851784867066282057)
    channel = message.channel
    reason = " ".join(reason)
    await user.kick(reason=reason)
    embed = discord.Embed(title=user.name + " is KICKED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nFrom " + ctx.author.mention)
    await ctx.send(embed=embed)
    embed = discord.Embed(title="You are kicked",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Reason:" + reason + "\nFrom " + ctx.author.mention)
    await user.send(embed=embed)
    embed = discord.Embed(title=user.name + " is KICKED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
    await channel.send(embed=embed)
@bot.command()
@commands.has_role("Administrator")
async def ban(ctx, user: discord.Member, *reason):
    message = await bot.get_channel(851784439204675584).fetch_message(851784867066282057)
    channel = message.channel
    reason = " ".join(reason)
    await user.ban(reason=reason)
    embed = discord.Embed(title=user.name + " is BANNED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nFrom " + ctx.author.mention)
    await ctx.send(embed=embed)
    embed = discord.Embed(title="You are banned",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Reason:" + reason + "\nFrom " + ctx.author.mention)
    await user.send(embed=embed)
    embed = discord.Embed(title=user.name + " is BANNED!",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Reason:\n" + reason + "\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
    await channel.send(embed=embed)
@bot.command()
@commands.has_role("Administrator")
async def unban(ctx, id):
    message = await bot.get_channel(851784439204675584).fetch_message(851784867066282057)
    channel = message.channel
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    embed = discord.Embed(title=user.name + " is UNBANNED",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention)
    await ctx.send(embed=embed)
    embed = discord.Embed(title="You are unbanned",url="http://tntprizz.zapto.org/dc",color=discord.Color.green(),description="Thanks for admin's Great Fat Compassion!" + "\nFrom " + ctx.author.mention)
    await user.send(embed=embed)
    embed = discord.Embed(title=user.name + " is BANNED!",url="http://tntprizz.zapto.org/dc",color=discord.Color.red(),description="Thanks for admin's Great Fat Compassion!\nchannel:" + ctx.message.channel.mention + "\nFrom " + ctx.author.mention)
    await channel.send(embed=embed)
@bot.command()
@commands.has_role("Administrator")
async def purge(ctx,limit:int):
    await ctx.channel.purge(limit=limit)
#embed echoimage
@bot.command(aliases=["image"])
async def echoimage(ctx, *url: str):
    if ctx.channel.id == 800679826611765258:
        return
    elif ctx.channel.id == 829292031049990195:
        return
    else:
        embed = discord.Embed(title="  ",
                             url="http://tntprizz.zapto.org/dc",
                              color=discord.Color.blue())
        url1 = " ".join(url)
        embed.set_image(url=url1)
        await ctx.send(embed=embed)
        await ctx.message.delete()
@bot.command()
@commands.has_role("Administrator")
async def eembed(ctx, messageid: int, title: str, content: str):
    try:
        msg = await ctx.fetch_message(messageid)
        await msg.edit(embed=discord.Embed(title=title,url="http://tntprizz.zapto.org/dc",description=content,color=discord.Color.blue()))
        await ctx.message.delete()
    except:
        await ctx.message.add_reaction("❌")
@bot.command()
@commands.has_role("Administrator")
async def areact(ctx, messageid: int, emoji):
    try:
        await ctx.message.delete()
        msg = await ctx.fetch_message(messageid)
        await msg.add_reaction(emoji)
    except:
        await ctx.message.add_reaction("❌")
@bot.command()
@commands.has_role("Administrator")
async def eecho(ctx, messageid: int, *content):
    try:
        content = " ".join(content)
        msg = await ctx.fetch_message(messageid)
        await msg.edit(content=content)
        await ctx.message.delete()
    except:
        await ctx.message.add_reaction("❌")
#rock paper scissors
@bot.command()
async def rps(ctx, F: str = "rock"):
    E = ["rock","paper","scissors"]
    ch = choice(E)
    if ch == F:
        result = "Draw!"
    else:
        if F == "rock":
            if ch == "paper":
                result = "I won!"
            else:
                result = "You won!"
        elif F == "paper":
            if ch == "scissors":
                result = "I won!"
            else:
                result = "You won!"
        elif F == "scissors":
            if ch == "rock":
                result = "I won!"
            else:
                result = "You won!"
        else:
            result = "use `rock` `paper` `scissors` as your option."
    embed = discord.Embed(title=result,url="http://tntprizz.zapto.org/dc",description="You: " + F + "\nMe: " + ch,color=discord.Color.blue())
    await ctx.send(embed=embed)
#send out the sourcecode
@bot.command(pass_content=True)
async def sourcecode(ctx):
    await ctx.send(embed = discord.Embed(title="source code link:",
                                url="https://github.com/TNTprizz/TOS-DOS",
                                description="[Github](https://github.com/TNTprizz/TOS-DOS)\nUpdate unevenly",
                                color=discord.Color.blue()))
#start TNTprizz server
@bot.command(aliases=["startsmp","smpstart","startserver","server"])
async def tntserverstart(ctx):
    global exitcode
    global server
    try:
        exitcode = server.poll()
    except: pass
    if exitcode == 0:
        server = subprocess.Popen(["bash","/var/www/html/dmg/discord/papermc/start.sh"],cwd="/var/www/html/dmg/discord/papermc/")
        print("\a")
        exitcode = 1
        await ctx.send("Server is starting, please wait until server started message appears at <#838308356745330728>")
    else:
        await ctx.send("Server has started. You cannot start the server which is started.")
@bot.command()
async def serverlog(ctx):
    await ctx.send("update when server start again.")
    await ctx.send(file=discord.File('/var/www/html/dmg/discord/papermc/minecraft.log'))
#send out your profile
@bot.command(aliases=["profile"])
async def aboutme(ctx):
    mention = []
    user = ctx.author
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
    try:
        for role in user.roles:
            if role.name != "@everyone":
                mention.append(role.mention)
        b = ", ".join(mention)
        trole = user.top_role
        if user.top_role == None:
            trole = "no role"
    except Exception():
        b = "no role."
        trole = "no role."
    embed = discord.Embed(title=user.name + "'s profile",
                        url="http://tntprizz.zapto.org/dc",
                        description="",
                        color=discord.Color.blue())
    embed.set_thumbnail(url=user.avatar_url) # this thanks @two slices of cucumber that gives me the user icon method.
    embed.add_field(name="User display name",value=user.display_name)
    embed.add_field(name="User mention",value=user.mention)
    embed.add_field(name="User ID",value=user.id)
    embed.add_field(name="User activity",value=act)
    embed.add_field(name="User status",value=status)
    try:
        embed.add_field(name="User top role", value=trole,inline=False)
        embed.add_field(name="User roles",value=b)
    except:
        embed.add_field(name="User roles", value="You have no role! What a shame.", inline=False)
    await ctx.send(embed=embed)
#print someone's profile
@bot.command()
async def about(ctx, user = "bot"):
    cputemp = CPUTemperature()
    temp = str(cputemp.temperature)
    usage = str(psutil.cpu_percent(interval=0.3))
    memory = psutil.virtual_memory().percent
    used = round(memory / 100 * 7629, 3)
    if user == "bot":
        embed = discord.Embed(title="about TOS-DOS:",
                        url="http://TNTprizz.zapto.org/dc",
                        description="about open sourced TOS-DOS",
                        color=discord.Color.gold())
        embed.add_field(name="author",value="TNTprizz80315#6093",inline=True)
        embed.add_field(name="name",value="TOS-DOS(TNTprizz operating server - Don't operate system)",inline=True)
        embed.add_field(name="version",value=ver,inline=True)
        embed.add_field(name="stage",value="Σ(SIGMA)",inline=True)
        embed.add_field(name="status",value="running",inline=True)
        embed.add_field(name="source",value="run `$sourcecode` to get the link", inline=True)
        embed.add_field(name="CPU:",value="Temperature: " + temp + "°C\n" + "Usage: " + usage + "%")
        embed.add_field(name="RAM:",value="Used: " + str(used) + "/7629.395 MiB\n" + "Percent: " + str(memory) + "%")
        await ctx.send(embed=embed)
    else:
        converter = discord.ext.commands.MemberConverter()
        user = await converter.convert(ctx, user)
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
        b = ", ".join(mention)
        embed = discord.Embed(title=user.name + "'s profile",
                            url="http://tntprizz.zapto.org/dc",
                            description="",
                            color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar_url) # this thanks @two slices of cucumber that gives me the user icon method.
        embed.add_field(name="User display name",value=user.display_name)
        embed.add_field(name="User mention",value=user.mention)
        embed.add_field(name="User ID",value=user.id)
        embed.add_field(name="User activity",value=act)
        embed.add_field(name="User status",value=status)
        try:
            embed.add_field(name="User top roles", value=user.top_role,inline=False)
            embed.add_field(name="User roles",value=b)
        except:
            embed.add_field(name="User roles", value="This user has no role! What a shame.", inline=False)
        await ctx.send(embed=embed)
#random question answerer
@bot.command(pass_context=True)
async def ask(ctx):
    await ctx.send(choice(ans))
#hacking
@bot.command()
async def hack(ctx, user: discord.User):
    msg = await ctx.send("hacking " + user.display_name + "......")
    await asyncio.sleep(1)
    await msg.edit(content="Fetching ip address......")
    await asyncio.sleep(1)
    await msg.edit(content="Ip address fetched! Output: `142.250." + str(randrange(999)) + ".78:" + str(randrange(9999)) + "`")
    await asyncio.sleep(1)
    await msg.edit(content="Getting email address and password......")
    await asyncio.sleep(1)
    await msg.edit(content="Succeed!!!!\nemail:`" + user.display_name + "@pepe.copper`\npassword:||`abcd1234`||")
    await asyncio.sleep(1)
    await msg.edit(content="prepare to ddos his computer......")
    await asyncio.sleep(1)
    await msg.edit(content="ddos commpleted!")
    await asyncio.sleep(1)
    await msg.edit(content="send command:`sudo rm -rf /*`")
    await asyncio.sleep(1)
    await msg.edit(content="Sending missle to his house......")
    await asyncio.sleep(4)
    await msg.edit(content="Completed!")
    await asyncio.sleep(1)
    await msg.edit(content="Selling his data to the Communist Party......")
    await asyncio.sleep(1)
    await msg.edit(content="Done!")
    await asyncio.sleep(1)
    await msg.edit(content="Stealing all his bitcoin......")
    await asyncio.sleep(1)
    await msg.edit(content="Now he has 0 and you have 100000")
    await asyncio.sleep(1)
    await msg.edit(content="Getting all of the Phallic Object from " + user.display_name)
    await asyncio.sleep(1)
    await msg.edit(content="Getting all his money from " + user.display_name + " ignoring the passive mode.")
    await asyncio.sleep(1)
    await msg.edit(content="Installing CentOS on his phone")
    await asyncio.sleep(1)
    await msg.edit(content="Send `MEMZ` `WannaCry` `Petya` into his computer")
    await asyncio.sleep(1)
    await msg.edit(content="replacing bash with rbash")
    await asyncio.sleep(1)
    await msg.edit(content="command:`$ echo logout >> .bashrc`")
    await asyncio.sleep(2)
    await msg.edit(content="Calling Windowsboy to hack him.")
    await asyncio.sleep(1)
    await msg.edit(content="Tracking Windowsboy's ip address")
    await asyncio.sleep(1)
    await msg.edit(content="Sending the sourcecode into Windowsboy's computer")
    await asyncio.sleep(1)
    await msg.edit(content="Now the whole world know that Windowsboy done that.")
    await asyncio.sleep(3)
    await msg.edit(content="Process completed with exit code 0.")
#kill someone(virtually)
@bot.command()
async def kill(ctx, user: discord.User):
    await ctx.send(str(user.name + choice([" was blown up by a creeper", " fell from a high place", " was killed by a wither", " has done nothing but he still died", " failed his exam", " falied his clutch", " was blown up by [Internal Game Design]", " was slain by air", " was betrayed by his dogs", " failed his water MLG"])))
#say hi
@bot.command(pass_context=True)
async def hello(ctx):
    await ctx.send(choice(["HI! :)", "Hoi! ;)", "E", "Why you wake me up QAQ"]))

@bot.command()
async def secho(ctx, user: discord.User, args: str):
    await user.send(args)
    await ctx.send("secho executed successfully.")
#export an embed table
@bot.command(pass_context=True)
async def embed(ctx, title: str, con: str):
    embed = discord.Embed(title=title,
                          url="http://tntprizz.zapto.org/dc",
                          description=con,
                          color=discord.Color.blue())
    await ctx.send(embed=embed)
#export an embed table securely
@bot.command()
async def dembed(ctx, title: str, con: str):
    name = ctx.message.author.name
    embed = discord.Embed(title=title,
                          url="http://tntprizz.zapto.org/dc",
                          description=con,
                          color=discord.Color.blue())
    record = open("temprecord", "a+")
    record.write(name + ": " + title + " ; " + con + "\n")
    record.close()
    await ctx.send(embed=embed)
    await ctx.message.delete()
#assign role
@bot.command(pass_context=True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(role.name + " is assigned to user " + user.display_name)
#remove role
@bot.command(pass_context=True)
async def rmrole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(role.name + " is removed from user " + user.display_name)
#detect latency
@bot.command()
async def ping(ctx):
    await ctx.send('**$pong**')
    await ctx.send('latency = ' + str(round(bot.latency * 1000)) + 'ms')
#detect latency
@bot.command()
async def pong(ctx):
    await ctx.send('**$ping**')
    await ctx.send('latency = ' + str(round(bot.latency * 1000)) + 'ms')
#say something what you say
@bot.command()
async def echo(ctx, echoed: str):
    await ctx.send(echoed)
#check your role
@bot.command(aliases = ["rolecheck", "checkrole"])
async def whoamirole(ctx):
    mention = []
    user = ctx.author
    for role in user.roles:
        if role.name != "@everyone":
            mention.append(role.mention)
    b = ", ".join(mention)
    embed = discord.Embed(title="Info:", description=f"Info of: {user.mention}", color=discord.Color.orange())
    embed.add_field(name="Top role:", value=user.top_role)
    embed.add_field(name="Roles:", value=b)
    await ctx.send(embed=embed)
#check who you are
@bot.command(pass_content=True)
async def whoami(ctx):
    await ctx.send(ctx.message.author.mention)
#check whats your id
@bot.command(pass_content=True)
async def whoamid(ctx):
    await ctx.send(ctx.message.author.id)
#print out a secret
@bot.command()
async def secret(ctx):
    await ctx.send(choice(secrets))
#filp a coin
@bot.command()
async def coinfilp(ctx):
    await ctx.send(choice(["front","back"]))
#bash
@bot.command()
async def cd(ctx):
    await ctx.send("rbash: cd : restricted")
#temp show contents
@bot.command()
async def temp(ctx, *con: str):
    name = ctx.message.author.name
    record = open("temprecord", "a+")
    record.write(name + str(con) + "\n")
    await asyncio.sleep(2)
    await ctx.message.delete()
    record.close()
#echo but delete the massage
@bot.command()
async def decho(ctx, echoed):
    name = ctx.message.author.name
    record = open("temprecord", "a+")
    record.write(name + ": " + echoed + "\n")
    record.close()
    await ctx.send(echoed)
    await ctx.message.delete()
#show the version
@bot.command()
async def version(ctx):
    await ctx.send("Version: " + ver)
#show the credit
@bot.command(aliases = ["credits"])
async def credit(ctx):
    embed = discord.Embed(title="Credits",
                          url="https://www.youtube.com/watch?v=EOTAWLaDa58",
                          description="TOS-DOS created by <@469038475371479041>\n"
                                      "list of members:\n"
                                      "coding:<@469038475371479041>\n"
                                      "surf internet:<@469038475371479041>\n"
                                      "go to toilet:<@469038475371479041>\n"
                                      "Eeeing:<@469038475371479041>\n"
                                      "Advisor:<@666186125026525194>, <@664644679232520233>, <@653086042752286730>\n",
                          color=discord.Color.blue())
    embed.set_thumbnail(url="http://tntprizz.zapto.org/dc/bps(square).jpeg")
    await ctx.send(embed=embed)
#show the real credit
@bot.command()
async def creditz(ctx):
    embed = discord.Embed(title="Creditz",
                          url="https://www.youtube.com/watch?v=EOTAWLaDa58",
                          description="I coded a bot but you don't\n"
                                      "(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ\n"
                                      "(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ\n"
                                      "(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ\n"
                                      "(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ\n"
                                      "(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ(σﾟ∀ﾟ)σ\n"
                                      "--by TNTprizz who own TOS-DOS",
                          color=discord.Color.red())
    embed.set_thumbnail(url="http://tntprizz.zapto.org/dc/bps(square).jpeg")
    await ctx.send(embed=embed)
#same as help.
@bot.command(aliases = ["?", "manual", "help"])
async def man(ctx, cmd: str = "all"):
    embed = discord.Embed(title="manual",
                          url="http://TNTprizz.zapto.org/dc/",
                          description="Hello! " + ctx.author.display_name + "\nHere is the manual:",
                          color=discord.Color.blue())
    embed.set_thumbnail(url="http://tntprizz.zapto.org/dc/bps(square).jpeg")
    if cmd == "all":
        embed.add_field(name="Bash:", value="`echo` `decho` `whoami` `whoamid` `whoamirole` `embed` `dembed` `sourcecode` `version` `about` `aboutme`",
                        inline=False)
        embed.add_field(name="Something E:", value="`ping` `pong` `E` `credit(z)` `ask` `kill` `temp` `rps` `coinfilp` `hack`", inline=False)
        embed.add_field(name="Minecraft:", value="`startserver` `serverlog`", inline=False)
        embed.add_field(name="Events:",value="`vote` `endvote` `multivote`", inline=False)
        embed.add_field(name="Superusers:", value="`rmrole` `addrole` `warn` `ban` `unban` `kick` `eembed` `eecho` `areact` `purge`", inline=False)
        embed.add_field(name="Music Σ(Sigma):", value="use `$man music` for help", inline=False)
        embed.add_field(name="Currently updating", value="please look forward for updates!", inline=False)
    elif cmd == "purge":
        embed.add_field(name="man purge:", value="`$areact <number of message>`\nPurge the given number of message.", inline=False)
    elif cmd == "eembed":
        embed.add_field(name="man eembed:", value="`$eembed <messageid> <title> <content>`\nEdit a message with the given embed.", inline=False)
    elif cmd == "eecho":
        embed.add_field(name="man eecho:", value="`$eecho <messageid> <content>`\nEdit a message with the given text.", inline=False)
    elif cmd == "areact":
        embed.add_field(name="man areact:", value="`$areact <messageid> <emoji>`\nAdd a reaction with the given emoji.", inline=False)
    elif cmd == "vote":
        embed.add_field(name="man vote:", value="`$vote <messageid>`\nCreate a voting event using the message id.", inline=False)
    elif cmd == "endvote":
        embed.add_field(name="man endvote:", value="`$endvote <messageid>`\nEnd a voting event using the message id.", inline=False)
    elif cmd == "multivote":
        embed.add_field(name="man multivote:", value="`$multivote <title> *<args(max 10)>`\nCreate a multivoting event", inline=False)
    elif cmd == "rps":
        embed.add_field(name="man rps:", value="`$rps <rps?>`\nPlay rock paper scissors with you", inline=False)
    elif cmd == "hack":
        embed.add_field(name="man hack:", value="`$rps <@user>`\nHack someone", inline=False)
    elif cmd == "man":
        embed.add_field(name="man man:", value="`$man <cmd>`\nprint out this help manual", inline=False)
    elif cmd == "music":
        embed.add_field(name="man music:",value="TOS-DOS is a music player!\n`$music <cmd> [url]`\n`$m connect`: Let TOS-DOS connect to a voice channel.\n"
        "`$m disconnect`: Let TOS-DOS disconnect from the voice channel.\n`$m play <url>`: play music with given url from youtube.\n`$m addplaylist <url>`: add playlist into queue.\n`$m pause`: pause the current track.\n"
        "`$m resume`: resume the paused track.\n`$m queue <url>`: add songs to queue or do same things with `$m play`.\n`$m search <args>`: search song from youtube.\n`$m listqueue <page>`: List out the song queue\n"
        "`$m skip`: skip the current track.\n`$m loop`: loop the queue for the specified time.(Suggested by Stupid Benz)\n`$m stop`: Stop and clear the whole queue.")
    elif cmd == "ask":
        embed.add_field(name="man ask:", value="`$ask [question]`\nanswer your questions randomly\n"
                                               "What do you expect? An AI?", inline=False)
    elif cmd == "kick":
        embed.add_field(name="man kick:", value="`$kick <@user> <reason>`\nKick the user with given reason.", inline=False)
    elif cmd == "ban":
        embed.add_field(name="man ban:", value="`$ban <@user> <reason>`\nBan the user with given reason.", inline=False)
    elif cmd == "unban":
        embed.add_field(name="man unban:", value="`$ban <user id>`\nUnban the user with given userid.", inline=False)
    elif cmd == "warn":
        embed.add_field(name="man warn:", value="`$warn <@user> <reason>`\nWarn the user with given reason.", inline=False)
    elif cmd == "echoimage":
        embed.add_field(name="man echoimage:", value="`$echoimage <url>`\nShow the image with given url.", inline=False)
    elif cmd == "temp":
        embed.add_field(name="man temp:", value="`$temp [temps]`\ntemperatory show your stuffs, and delete it after 2 seconds.", inline=False)
    elif cmd == "decho":
        embed.add_field(name="man decho:", value="`$decho <echoed>`\nsecurely print out the input and delete your command.", inline=False)
    elif cmd == "dembed":
        embed.add_field(name="man dembed:", value="`$dembed <title> <content>`\nsecurely export an embed table and delete your command.", inline=False)
    elif cmd == "startserver":
        embed.add_field(name="man startserver:", value="`$startserver`\nStart my minecraft server\nip:`TNTprizz.zapto.org`", inline=False)
    elif cmd == "serverlog":
        embed.add_field(name="man serverlog:", value="`$serverlog`\nShow the log of the minecraft server.", inline=False)
    elif cmd == "sourcecode":
        embed.add_field(name="man sourcecode:", value="`$sourcecode`\nshow the source code of TOS-DOS", inline=False)
    elif cmd == "ping":
        embed.add_field(name="man ping:", value="`$ping`\nprint out pong and show latency when triggered", inline=False)
    elif cmd == "kill":
        embed.add_field(name="man kill:", value="`$kill <user>`\nkill someone using 德\naka 以德服人", inline=False)
    elif cmd == "warnlist":
        embed.add_field(name="man warnlist:", value="`$warnlist`\nprint out the warn record, for more details, goto" +
                                                    "\n<#813277900564463616> for more details", inline=False)
    elif cmd == "E":
        embed.add_field(name="man E:", value="`$E`\nprint out Æ when triggered", inline=False)
    elif cmd == "pong":
        embed.add_field(name="man pong:", value="`$pong`\nprint out ping and show latency when triggered", inline=False)
    elif cmd == "ls":
        embed.add_field(name="man ls:", value="`$ls`\nlist out the directory of ~", inline=False)
    elif cmd == "echo":
        embed.add_field(name="man echo:", value="`$echo <something>`\nprint out the second field inserted\n(use '' for "
                                                "multiple words.)", inline=False)
    elif cmd == "cd":
        embed.add_field(name="man cd:", value="`$cd <directory>`\nchange directory\nRestricted cuz using rbash",
                        inline=False)
    elif cmd == "coinfilp":
        embed.add_field(name="man coinfilp:", value="`$coinfilp`\nfilp a coin", inline=False)
    elif cmd == "about":
        embed.add_field(name="man about:", value="`$about`\nexport an embed containing user imformation",inline=False)
    elif cmd == "version":
        embed.add_field(name="man version:", value="`$version`\nprint out the version of TOS-DOS when triggered", inline=False)
    elif cmd == "cat":
        embed.add_field(name="man cat:", value="`$cat <file>`\nprint out the content of the file", inline=False)
    elif cmd == "whoami":
        embed.add_field(name="man whoami:", value="`$whoami`\nprint out your name", inline=False)
    elif cmd == "whoamid":
        embed.add_field(name="man whoamid:", value="`$whoamid`\nprint out your user id", inline=False)
    elif cmd == "aboutme":
        embed.add_field(name="man aboutme:", value="`$aboutme`\nexport an embed table contains your profile.", inline=False)
    elif cmd == "embed":
        embed.add_field(name="man embed:", value="`$embed <title> <content>`\nexport an embed table with title and "
                                                 "content", inline=False)
    elif cmd == "whoamirole":
        embed.add_field(name="man whoamirole:", value="`$whoamirole`\nprint out your roles", inline=False)
    elif cmd == "rmrole":
        embed.add_field(name="man rmrole:", value="`$rmrole <@member> <rolename>`\nremove role from user", inline=False)
    elif cmd == "addrole":
        embed.add_field(name="man addrole:", value="`$addrole <@member> <rolename>`\nadd role to user", inline=False)
    elif cmd == "credit":
        embed.add_field(name="man credit:", value="`$credit`\nshow the credit", inline=False)
    elif cmd == "creditz":
        embed.add_field(name="man creditz:", value="`$creditz`\nshow the real credit(?)", inline=False)
    else:
        embed.add_field(name="Error:", value="no manual for this command,\n"
                                             "use `$man all` for a list of command.", inline=False)
    await ctx.send(embed=embed)

print('No santax exception, running')
token = open("E.key","r+")
bot.run(token.read())
token.close()
