import discord
from discord.ext import commands
from discord import app_commands
import json
from datetime import datetime, timezone

# Imports config
with open("json/config.json", "r") as read_file:
    config = json.load(read_file)

WATCHLIST = config["watchlist"]

WELCOME_CHANNEL_ID = config["channels"]["welcome"]
IMMIGRATION_CHANNEL_ID = config["channels"]["immigration"]
EMMIGRATION_CHANNEL_ID = config["channels"]["emmigration"]
WATCHLIST_ALERTS_CHANNEL_ID = config["channels"]["watchlist_alerts"]
COMMUNITY_COMMENTS_CHANNEL_ID = config["channels"]["community_comments"]
DEFAULT_ROLE_ID = config["roles"]["default"]


class listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Ping the listener cog.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def ping_listener(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

    # Scans all messages the bot can see to see if it contains any of the words on the watchlist
    @commands.Cog.listener()
    async def on_message(self, message):

        # Does nothing if the bot was the user to send the message (prevents a loop)
        if message.author == self.bot.user:
            return

        # The channel that messages get sent to when a word on the watchlist is found
        watchlist_alerts_channel = self.bot.get_channel(WATCHLIST_ALERTS_CHANNEL_ID)
        community_comments_channel = self.bot.get_channel(COMMUNITY_COMMENTS_CHANNEL_ID)

        # message.channel.name throws an error if the message is a direct message to the bot
        try:
            _ = message.channel.name
            channel = message.channel.id

        # If it is a direct message, it is sent directly to the staff channel
        except AttributeError:
            await community_comments_channel.send(
                f"```{message.author.name} said: \n\n{message.content}```"
            )
            channel = None

        message_check = message.content.lower()

        # Checks to see if any of the watched words are included in the (lowercase) message
        # Also triggers with prefixes and suffixes (If "foo" is on the watchlist, "foo", "afoo", "foob", and "afoob" will trigger the bot)
        for word in WATCHLIST:
            # Doesn't send message to staff channel if it was in direct messages (they've already been sent)
            if word in message_check and channel != None:
                # Formats differently depending on message length (Discord embeds have an ~250 character limit)
                if len(message.content) < 250:
                    embed = discord.Embed(
                        title="Message Alert",
                        description=f"{message.author.mention} in <#{channel}>",
                        color=0xFFBB00,
                    )
                    embed.add_field(
                        name=f'"{message.content}"',
                        value=f"[Message Link]({message.jump_url})",
                    )
                    embed.set_footer(
                        text="",
                        icon_url=f"https://cdn.discordapp.com/emojis/607596209254694913.png?v=1",
                    )
                    await watchlist_alerts_channel.send(embed=embed)
                else:
                    # If the message is close to the character limit, it is shortened to ensure it is always sent to the staff channel
                    if len(message.content) > 1700:
                        message_content = message.content[0:1700] + (
                            "(Rest of message unavailable)"
                        )
                    else:
                        message_content = message.content

                    await watchlist_alerts_channel.send(
                        f"**Message Alert**\t||\tWord:   {word}\n\n{message.author.mention} in <#{channel}>\nLink: {message.jump_url}\n\n```{message_content}```"
                    )

    # Sends a message to an emmigration channel when a user leaves the server
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        emmigration_channel = self.bot.get_channel(EMMIGRATION_CHANNEL_ID)

        # Calculates the difference between the current time and the time the user joined
        delta = datetime.now(timezone.utc) - member.joined_at

        if delta.days == 1:
            await emmigration_channel.send(
                f"{member.mention} has left the server (Last joined {delta.days} day ago)"
            )
        else:
            await emmigration_channel.send(
                f"{member.mention} has left the server (Last joined {delta.days} days ago)"
            )

    # When a member joins the server, they receive a default role, a direct message, and a message in the welcome channel
    @commands.Cog.listener()
    async def on_member_join(self, member):
        default_role = discord.utils.get(member.guild.roles, id=DEFAULT_ROLE_ID)
        await discord.Member.add_roles(member, default_role)

        welcome_channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        immigration_channel = self.bot.get_channel(IMMIGRATION_CHANNEL_ID)

        await welcome_channel.send("Welcome to **RL Ireland**")

        delta = datetime.now(timezone.utc) - member.created_at

        if delta.days == 1:
            await immigration_channel.send(
                f"{member.mention} has joined the server (Account created {delta.days} day ago)"
            )
        else:
            await immigration_channel.send(
                f"{member.mention} has joined the server (Account created {delta.days} days ago)"
            )
        await member.send("Hey! Welcome to RL Ireland")


async def setup(bot):
    await bot.add_cog(listener(bot))
