import discord
from discord.ext import commands
from discord import app_commands
from os import listdir
import config

PREFIX = ">"
TOKEN = config.TOKEN
GUILD_ID = "846538497087111169"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
tree = bot.tree

cogs = [f[:-3] for f in listdir() if "cog" == f[-6:-3]]
print("Cogs:")
for cog in cogs:
    try:
        bot.load_extension(cog)
        print(f"\t{cog}")
    except Exception as e:
        print(f"Failed to load cog: {cog[:-4]}")
        print(f"{type(e).__name__}: {e}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} [{bot.user.id}]")
    print("Servers:")
    for guild in bot.guilds:
        print(f"\t{guild.name}")

@bot.command()
async def synclocal(ctx):
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    await ctx.send("Slash commands synced.")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! (from a prefix command)")

@tree.command(description="Ping the main script using a slash command.", guild=discord.Object(id=GUILD_ID))
async def ding(interaction:discord.Interaction):
    await interaction.response.send_message("Dong! (from a slash command)", ephemeral=True)

bot.run(TOKEN)