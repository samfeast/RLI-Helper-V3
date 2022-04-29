import discord
from discord.ext import commands
from discord import app_commands
import json

with open("json/config.json", "r") as read_file:
    config = json.load(read_file)


class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Ping the moderation cog.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def ping_moderation(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!", ephemeral=True)

    @app_commands.command(description="Ping the moderation cog.")
    @app_commands.guilds(discord.Object(id=846538497087111169))
    async def mute(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        duration: str,
        reason: str,
    ):
        try:
            await user.add_roles(
                self.bot.get_guild(846538497087111169).get_role(
                    config["roles"]["muted"]
                )
            )
            embed = discord.Embed(colour=0x72FF72)
            embed.set_author(name=f"{user.name}#{user.discriminator} was muted")
            embed.set_thumbnail(url=user.avatar)
            embed.set_footer(
                text=f"muted by {interaction.user.name}#{interaction.user.discriminator}",
                icon_url=interaction.user.avatar,
            )
            embed.add_field(name="Duration", value=duration)
            embed.add_field(name="Reason", value=reason)

            await interaction.response.send_message(embed=embed, ephemeral=False)
        except discord.Forbidden:
            await interaction.response.send_message(
                "Unable to mute user. Make sure the muted role is below the bot role in the hierarchy.",
                ephemeral=True,
            )


async def setup(bot):
    await bot.add_cog(moderation(bot))
