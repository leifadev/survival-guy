from config import BOT
import discord
import discord.ext
from discord.ext import commands
from discord.utils import get


intents = discord.Intents.all()
initial_extensions = ['cogs.cogs']
token = BOT['TOKEN']
bot = commands.Bot(command_prefix=BOT['PREFIX'], intents=intents)

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
    if payload.message_id == 741437491944358060:
        if payload.emoji.name == '\N{WHITE HEAVY CHECK MARK}':
            guild = await bot.fetch_guild(payload.guild_id)
            if guild is not None:
                member = payload.member
                guild_member = discord.utils.get(guild.roles, name="Guild Member")
                pending = discord.utils.get(guild.roles, name="Rules Pending")
                await member.add_roles(guild_member)
                await member.remove_roles(pending)
                channel = bot.get_channel(payload.channel_id)
                user = bot.get_user(payload.user_id)
                message = await channel.fetch_message(payload.message_id)
                emoji = payload.emoji.name
                await message.remove_reaction(emoji, user)

@bot.command()
@commands.has_role("Admin")
async def help(ctx):
    rembed = discord.Embed(title="IP and Info", color=0xb92d5d)
    rembed.add_field(name="The IP to the server is yugen.us.to", value="Contact admins for any other concerns", inline=False)
    rembed.set_footer(text="Thank you!")
    await ctx.channel.send(embed=rembed)

@bot.command()
@commands.has_role("Admin")
async def hypixelembed(ctx):
    rembed = discord.Embed(title="React here to see your Hypixel stats", color=0xb92d5d)
    rembed.add_field(name="Click the checkmark and have fun!", value="Brought to you by the Hypixel Guild Bot", inline=False)
    await ctx.channel.send(embed=rembed)



# cog import

# if __name__ == '__main__':
#     for extension in initial_extensions:
#         bot.load_extension(extension)


bot.run(token)
