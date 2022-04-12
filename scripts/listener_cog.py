from os import write
import discord
from discord.ext import commands
import json

#with open("banned_words.json", "r") as read_file:
#    banned_word_list = json.load(read_file)

banned_word_list = {"banned_words": ["test"]}

class commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bading(self, ctx):
        embed=discord.Embed(title="Badong", color=0x0cdce2)
        embed.set_footer(text="Inspired by cog")
        await ctx.send(embed=embed)

    @commands.command()
    async def add_banned_word(self, ctx, word):
        
        with open("banned_words.json", "r") as read_file:
            banned_words = json.load(read_file)

        banned_words["banned_words"].append(word.lower())

        with open("banned_words.json", "w") as write_file:
            json.dump(banned_words, write_file, indent=2)

        await ctx.send(f'"{word}" has been added to the banned word list.\nUse >reload listener_cog to commit changes.')
    
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        mod_channel = self.bot.get_channel(856899721170518016)

        try:
            _ = message.channel.name
            channel = f"<#{message.channel.id}>"

        except AttributeError:
            await mod_channel.send(f"```{message.author.name} said: \n\n{message.content}```")
            channel = None
        
        message_check = message.content.lower()

        for i in banned_word_list["banned_words"]:
            if i in message_check and channel != None:
                if len(message.content) < 250:
                    embed=discord.Embed(title=":octagonal_sign: **Naughty Word Detected** :octagonal_sign:", description=f"{message.author.mention} in {channel}", color=0xff0000)
                    embed.add_field(name=f'"{message.content}"', value="‎")
                    embed.set_footer(text="Powered by RLI", icon_url=f'https://cdn.discordapp.com/emojis/607596209254694913.png?v=1')
                    await mod_channel.send(embed=embed)
                else:
                    await mod_channel.send(f":octagonal_sign: **NAUGHTY WORD DETECTED** :octagonal_sign:\n\n{message.author.mention} in <#{channel}>:\n```{message.content}```")

async def setup(bot):
    await bot.add_cog(commands(bot))
