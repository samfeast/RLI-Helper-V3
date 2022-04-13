from ast import Str
import discord
from discord.ext import commands
from discord import app_commands
import json

class configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Ping the configuration cog.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def ping_configuration(self, interaction:discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

    watchlist_group = app_commands.Group(name="watchlist", description="Watchlist commands", guild_ids=[846538497087111169])

    # Adds a new word to watched_words.json in lowercase. Requires the listener cog to be reloaded to commit changes
    @watchlist_group.command(description="Add a word to the watchlist.")
    async def add(self, interaction: discord.Interaction, word: str):
        with open("json/watched_words.json", "r") as read_file:
            watchlist = json.load(read_file)
        if word in watchlist["list"]:
            await interaction.response.send_message("Word is already on the watchlist.", ephemeral=True)
        else:
            watchlist["list"].append(word.lower())

            with open("json/watched_words.json", "w") as write_file:
                json.dump(watchlist, write_file, indent=2)

            await interaction.response.send_message("Word added to the watchlist.\nUse >reload listener to commit changes.", ephemeral=True)

    # Removes a word from watched_words.json. Requires the listener cog to be reloaded to commit changes
    @watchlist_group.command(description="Remove a word from the watchlist.")
    async def remove(self, interaction: discord.Interaction, word: str):
        with open("json/watched_words.json", "r") as read_file:
            watchlist = json.load(read_file)

        if word.lower() in watchlist["list"]:    
            watchlist["list"].remove(word.lower())
                
            with open("json/watched_words.json", "w") as write_file:
                json.dump(watchlist, write_file, indent=2)

            await interaction.response.send_message("Word removed from the watchlist.\nUse >reload listener to commit changes.", ephemeral=True)
        else:
            await interaction.response.send_message("Word not found on the watchlist", ephemeral=True)

    # Prints the watchlist
    @watchlist_group.command(description="Show the watchlist.")
    async def show(self, interaction: discord.Interaction):
        with open("json/watched_words.json", "r") as read_file:
            watchlist = json.load(read_file)

        # .format is used as f-string formatting does not allow for backslashes
        # .join joins all of the items in the list into a string separated by "\n"
        await interaction.response.send_message("```Use >reload listener to ensure this is up to date.\n\n{}```".format("\n".join(watchlist["list"])), ephemeral=True)

async def setup(bot):
    await bot.add_cog(configuration(bot))
