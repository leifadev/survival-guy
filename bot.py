from config import BOT
import discord
import discord.ext
from discord.ext import commands
from discord.utils import get
import time

intents = discord.Intents.all()
initial_extensions = ['cogs.cogs']
token = BOT['TOKEN']
bot = commands.Bot(command_prefix=BOT['PREFIX'], intents=intents, help_command=None)


class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)


# Rich Presence
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Netflix"))


@bot.event
async def on_member_join(member):
    role = get(member.guild.roles, name='Member')
    await member.add_roles(role)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 804096688670769223:
        if payload.emoji.name == '\N{WHITE HEAVY CHECK MARK}':
            guild = await bot.fetch_guild(payload.guild_id)
            if guild is not None:
                member = payload.member
                guild_member = discord.utils.get(guild.roles, name="Hypixel Stats")
                await member.add_roles(guild_member)
                channel = bot.get_channel(payload.channel_id)
                user = bot.get_user(payload.user_id)
                message = await channel.fetch_message(payload.message_id)
                emoji = payload.emoji.name
                await message.remove_reaction(emoji, user)
    if payload.message_id == 804096688670769223:
        if payload.emoji.name == '\N{CROSS MARK}':
            guild = await bot.fetch_guild(payload.guild_id)
            if guild is not None:
                member = payload.member
                guild_member = discord.utils.get(guild.roles, name="Hypixel Stats")
                await member.remove_roles(guild_member)
                channel = bot.get_channel(payload.channel_id)
                user = bot.get_user(payload.user_id)
                message = await channel.fetch_message(payload.message_id)
                emoji = payload.emoji.name
                await message.remove_reaction(emoji, user)


@bot.command()
async def kawaii(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(file=discord.File('pics/02.gif'))


@bot.command()
async def help(ctx):
    rembed = discord.Embed(title="IP and Info", color=0x3a88fe)
    rembed.add_field(name="The IP to the server is yugen.us.to", value="Contact admins for any other concerns",
                     inline=False)
    rembed.set_footer(text="Thank you!")
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(embed=rembed)
    time.sleep(0.5)
    await ctx.channel.send(
        "**Also check the bots help page for all the commands!** https://github.com/leifadev/survival-guy/wiki")


@bot.command()
@commands.has_role("Admin")
async def hypixelembed(ctx):
    hembed = discord.Embed(title="React here to see your Hypixel stats", color=0x77bb41)
    hembed.add_field(name="Click the checkmark and have fun!", value="Brought to you by the Hypixel Guild Bot",
                     inline=False)
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(embed=hembed)


@bot.command()
async def sourcecode(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.channel.send("**The code for the bot is public to everyone on github**:")
    await ctx.channel.send("https://github.com/leifadev/survival-guy/")


## VOICE STUFF

@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def calmdown(ctx):
    try:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        voice = get(bot.voice_clients)
        voice.play(discord.FFmpegPCMAudio('sounds/calmdownjamal.wav'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 20.0
        time.sleep(4.5)
        await voice.disconnect()
    except:
        await ctx.author.send("You have to be in a voice channel to use this!")

@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def pierre(ctx):
    try:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        voice = get(bot.voice_clients)
        voice.play(discord.FFmpegPCMAudio('sounds/pierre.wav'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 10.0
        time.sleep(4.5)
        await voice.disconnect()
    except:
        await ctx.author.send("You have to be in a voice channel to use this!")
        await ctx.channel.purge(limit=1)
        
@bot.command()
@commands.has_role("Admin")
async def eclear(ctx, amount):
    try:
    	await ctx.channel.purge(limit=int(amount))
    except:
        await ctx.channel.send("Please specify a valid number!")
        
@bot.command()
async def hawaii(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(file=discord.File('pics/hawaii.jpeg'))
    
print("Startup successful!")

bot.run(token)
