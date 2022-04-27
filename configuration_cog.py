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
    set_channel_group = app_commands.Group(name="set_channel", description="Set channel commands", guild_ids=[846538497087111169])

    @set_channel_group.command(description="Change the welcome channel ID.")
    async def welcome(self, interaction: discord.Interaction, channel: discord.channel.TextChannel):
        with open("json/config.json", "r") as read_file:
            config = json.load(read_file)

        config["channels"]["welcome"] = channel.id

        with open("json/config.json", "w") as write_file:
            json.dump(config, write_file, indent=2)

        await interaction.response.send_message(f"{channel.mention} set as the welcome channel.\nUse >reload_all to commit changes.", ephemeral=False)

    @set_channel_group.command(description="Change the immigration channel ID.")
    async def immigration(self, interaction: discord.Interaction, channel: discord.channel.TextChannel):
        with open("json/config.json", "r") as read_file:
            config = json.load(read_file)

        config["channels"]["welcome"] = channel.id

        with open("json/config.json", "w") as write_file:
            json.dump(config, write_file, indent=2)

        await interaction.response.send_message(f"{channel.mention} set as the immigration channel.\nUse >reload_all to commit changes.", ephemeral=False)

    @set_channel_group.command(description="Change the emmigration channel ID.")
    async def emmigration(self, interaction: discord.Interaction, channel: discord.channel.TextChannel):
        with open("json/config.json", "r") as read_file:
            config = json.load(read_file)

        config["channels"]["welcome"] = channel.id

        with open("json/config.json", "w") as write_file:
            json.dump(config, write_file, indent=2)

        await interaction.response.send_message(f"{channel.mention} set as the emmigration channel.\nUse >reload_all to commit changes.", ephemeral=False)

    @set_channel_group.command(description="Change the watchlist alerts channel ID.")
    async def watchlist_alerts(self, interaction: discord.Interaction, channel: discord.channel.TextChannel):
        with open("json/config.json", "r") as read_file:
            config = json.load(read_file)

        config["channels"]["welcome"] = channel.id

        with open("json/config.json", "w") as write_file:
            json.dump(config, write_file, indent=2)

        await interaction.response.send_message(f"{channel.mention} set as the watchlist alerts channel.\nUse >reload_all to commit changes.", ephemeral=False)

    @set_channel_group.command(description="Change the community comments channel ID.")
    async def community_comments(self, interaction: discord.Interaction, channel: discord.channel.TextChannel):
        with open("json/config.json", "r") as read_file:
            config = json.load(read_file)

        config["channels"]["welcome"] = channel.id

        with open("json/config.json", "w") as write_file:
            json.dump(config, write_file, indent=2)

        await interaction.response.send_message(f"{channel.mention} set as the community comments channel.\nUse >reload_all to commit changes.", ephemeral=False)

    # Adds a new word to watched_words.json in lowercase. Requires the listener cog to be reloaded to commit changes
    @watchlist_group.command(description="Add a word to the watchlist.")
    async def add(self, interaction: discord.Interaction, word: str):
        with open("json/config.json", "r") as read_file:
            config = json.load(read_file)
        if word in config["watchlist"]:
            await interaction.response.send_message("Word is already on the watchlist.", ephemeral=True)
        else:
            config["watchlist"].append(word.lower())

            with open("json/config.json", "w") as write_file:
                json.dump(config, write_file, indent=2)

            await interaction.response.send_message("Word added to the watchlist.\nUse >reload listener to commit changes.", ephemeral=True)

    # Removes a word from watched_words.json. Requires the listener cog to be reloaded to commit changes
    @watchlist_group.command(description="Remove a word from the watchlist.")
    async def remove(self, interaction: discord.Interaction, word: str):
        with open("json/config.json", "r") as read_file:
            config = json.load(read_file)

        if word.lower() in config["watchlist"]:    
            config["watchlist"].remove(word.lower())
                
            with open("json/config.json", "w") as write_file:
                json.dump(config, write_file, indent=2)

            await interaction.response.send_message("Word removed from the watchlist.\nUse >reload listener to commit changes.", ephemeral=True)
        else:
            await interaction.response.send_message("Word not found on the watchlist", ephemeral=True)

    # Prints the watchlist
    @watchlist_group.command(description="Show the watchlist.")
    async def show(self, interaction: discord.Interaction):
        with open("json/config.json", "r") as read_file:
            config = json.load(read_file)

        # .format is used as f-string formatting does not allow for backslashes
        # .join joins all of the items in the list into a string separated by "\n"
        await interaction.response.send_message("```Use >reload listener to ensure this is up to date.\n\n{}```".format("\n".join(config["watchlist"])), ephemeral=True)

async def setup(bot):
    await bot.add_cog(configuration(bot))
