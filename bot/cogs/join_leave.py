import discord
import os
import time
from pathlib import Path
from discord.ext import commands
from discord import Embed, Color
from discord.utils import get
import asyncio
from dpymenus import Page, PaginatedMenu

class JoinLeave(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        try:
            channel = get(ctx.guild.channels, name="💢log-in")
            member_count = len(ctx.guild.members)

            embed = Embed(color=discord.Color.green())
            embed.add_field(name="💢LOG IN MESSAGE",
                            value=f"{ctx.mention} has joined the server.\nTotal number of members: {member_count}")
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await channel.send(embed=embed)

        except:
            return None


    @commands.Cog.listener()
    async def on_member_remove(self, ctx):
        try:
            channel = get(ctx.guild.channels, name="💢log-out")
            member_count = len(ctx.guild.members)

            embed = Embed(color=discord.Color.red())
            embed.add_field(name="💢LOG OUT MESSAGE",
                            value=f"{ctx.mention} has left the server.\nTotal number of members: {member_count}")
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await channel.send(embed=embed)

        except:
            return None

def setup(client):
    client.add_cog(JoinLeave(client))