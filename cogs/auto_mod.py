import discord
from discord.ext import commands
from discord import Embed, Color
from discord.utils import get
from datetime import datetime

class AutoMod(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message):
        muted = get(message.guild.roles, name="❌mute")

        with open("files/list.txt", "r") as f:
            bad_words = [words.strip(",") for words in f.read().split(",")]

            for word in bad_words:
                if message.content.count(word.strip(",")) > 0:
                    await message.channel.purge(limit=1)
                    embed = Embed(color=discord.Color.red())
                    embed.add_field(name="🔺BAD WORD HAS BEEN SAYD",
                                    value=f"A bad word has been sayd:\n**Author**: {message.author.mention}\n**Word**: {word}\n**Channel**: {message.channel}\n**Time**: {datetime.utcnow()}")
                    
                    await message.channel.send(embed=embed)
                    await message.author.add_roles(muted)

def setup(client):
    client.add_cog(AutoMod(client))
