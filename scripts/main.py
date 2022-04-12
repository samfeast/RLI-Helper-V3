import discord
from discord.ext import commands
from discord import app_commands
import asyncio
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

async def main():
    async with bot:
        cogs = [f[:-3] for f in listdir() if "cog" == f[-6:-3]]
        print("Cogs:")
        for cog in cogs:
            try:
                await bot.load_extension("listener_cog")
                print(f"\t{cog}")
            except:
                print(f"Failed to load cog: {cog[:-4]}")
                print(f"{type(Exception).__name__}: {Exception}")
        await bot.start(TOKEN)

asyncio.run(main())