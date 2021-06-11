#imports
import discord
from discord.ext import commands
from discord.utils import get

class auto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, user):
        if user.guild.id != 800679086955167775:
            return
        guild = user.guild
        await user.add_roles(get(guild.roles, id=800681780834992129))
        message = await self.bot.get_channel(800679087541583944).fetch_message(827789950606901309)
        channel = message.channel
        embed = discord.Embed(title="Welcome new user!",url="http://TNTprizz.zapto.org/dc",color=discord.Color.blue(),description="Welcome " + user.mention + " !\nHope you enjoy staying in this server!")
        await channel.send(embed=embed)
        await channel.send(file=discord.File('../welcome.gif'))
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji = payload.emoji.name
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        channel = message.channel
        guild = channel.guild
        user = get(guild.members, id=payload.user_id)
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
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji.name
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        channel = message.channel
        guild = channel.guild
        user = get(guild.members, id=payload.user_id)
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
def setup(bot):
    bot.add_cog(auto(bot))