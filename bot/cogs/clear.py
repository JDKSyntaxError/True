import discord
import os
import time
from pathlib import Path
from discord.ext import commands
from discord import Embed, Color
from discord.utils import get
import asyncio
from dpymenus import Page, PaginatedMenu

class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="clear")
    async def clear(self, ctx, amount=1000000):
        await ctx.channel.purge(limit=amount)

        await ctx.send(f"**True cleared {ctx.channel}**")
        time.sleep(5)
        await ctx.channel.purge(limit=1)

def setup(client):
    client.add_cog(Clear(client))