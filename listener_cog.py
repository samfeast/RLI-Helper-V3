import discord
from discord.ext import commands
from discord import app_commands
import json

# Imports list of words to listen for
with open("json/watched_words.json", "r") as read_file:
    watched_word_list = json.load(read_file)

class commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Ping the listener cog using a slash command.")
    @app_commands.guilds(discord.Object(id="846538497087111169"))
    async def ping_listener(self, interaction:discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

    # Adds a new term to watched_words.json in lowercase. Requires the cog to be reloaded so that the script re-imports the list
    @commands.command()
    async def add_watched_word(self, ctx, word):
        
        with open("json/watched_words.json", "r") as read_file:
            watched_words = json.load(read_file)

        watched_words["list"].append(word.lower())

        with open("json/watched_words.json", "w") as write_file:
            json.dump(watched_words, write_file, indent=2)

        await ctx.send(f'"{word}" has been added to the banned word list.\nUse >reload listener to commit changes.')
    
    # Scans all messages the bot can see to see if it contains any of the words in the banned list
    @commands.Cog.listener()
    async def on_message(self, message):

        # Does nothing if the bot was the user to send the message (prevents a loop)
        if message.author == self.bot.user:
            return

        # The channel that messages get sent to when a watched word is found
        mod_channel = self.bot.get_channel(856899721170518016)

        # message.channel.name throws an error if the message is a direct message to the bot
        try:
            _ = message.channel.name
            channel = message.channel.id

        # If it is a direct message, it is sent directly to the staff channel
        except AttributeError:
            await mod_channel.send(f"```{message.author.name} said: \n\n{message.content}```")
            channel = None
        
        message_check = message.content.lower()

        # Checks to see if any of the watched words are included in the (lowercase) message
        # Also triggers with prefixes and suffixes (If "foo" is on the watchlist, "foo", "afoo", "foob", and "afoob" will trigger the bot)
        for word in watched_word_list["list"]:
            # Doesn't send message to staff channel if it was in direct messages (they've already been sent)
            if word in message_check and channel != None:
                # Formats differently depending on message length (Discord embeds have an ~250 character limit)
                if len(message.content) < 250:
                    embed=discord.Embed(title=":octagonal_sign: **Naughty Word Detected** :octagonal_sign:", description=f"{message.author.mention} in <#{channel}>", color=0xff0000)
                    embed.add_field(name=f'"{message.content}"', value="‎")
                    embed.set_footer(text="Powered by RLI", icon_url=f'https://cdn.discordapp.com/emojis/607596209254694913.png?v=1')
                    await mod_channel.send(embed=embed)
                else:
                    await mod_channel.send(f":octagonal_sign: **NAUGHTY WORD DETECTED** :octagonal_sign:\n\n{message.author.mention} in <#{channel}>:\n```{message.content}```")

async def setup(bot):
    await bot.add_cog(commands(bot))
