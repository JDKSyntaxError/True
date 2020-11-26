import discord
import os
import time
from typing import Optional
from pathlib import Path
from discord.ext import commands
from discord import Embed, Color
from discord.utils import get
import asyncio
from dpymenus import Page, PaginatedMenu

class UserInfo(commands.Cog):
    def  __init__(self, client):
        self.client = client
    
    @commands.command(name="userinfo", aliases=['whois', 'user'])
    @commands.has_permissions(ban_members=True)
    async def user_info(self, ctx, user : discord.Member):
        roles = [role for role in user.roles if role != ctx.guild.default_role]
        embed = Embed(color=discord.Color.gold())
        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name=f"**👨USERINFO [{user.mention}]**",
                        value=f"🆔: **{user.id}**\n\n💻USERNAME: {user.mention}\n\n🟠STATUS: **{str(user.status).title()}**\n\n⌚CREATED AT: **{user.created_at}**\n\n🚪JOINED AT: **{user.joined_at}**\n\n💢ROLES: {[role.mention for role in roles]}")
        
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(UserInfo(client))