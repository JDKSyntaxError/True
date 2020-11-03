import discord
import os
import time
from pathlib import Path
from discord.ext import commands
from discord import Embed, Color
from discord.utils import get
import asyncio
from dpymenus import Page, PaginatedMenu

class Preferences(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def settings(self, ctx):
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="🤖BOT GUILD SETTINGS",
                        value="Use this command if you want to change the BOT settings in your server. There some options avaible.\n1️⃣: If you don't want the user verification in your server, just type **change1**.\n2️⃣: If you don't want the Staff Log, just type: **change2**\n3️⃣: If you want only the verification, just type **change3**. **Note: \n4️⃣If you want the Staff Log, just type change4**")
        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def change1(self, ctx):
        role = get(ctx.guild.roles, name="✔Verified")
        channel = get(ctx.guild.channels, name="✅verify")

        await channel.delete(reason="BOT Settings changed")
        await role.delete()

        embed = Embed(color=discord.Color.green())
        embed.add_field(name="🤖BOT Settings successfully changed",
                        value="The BOT settings have been successfully changed.\nCHANGE: **Deleting Verify system**")
        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def change2(self, ctx):
        login = get(ctx.guild.channels, name="💢log-in")
        logout = get(ctx.guild.channels, name="💢log-out")

        await login.delete(reason="BOT Settings changed")
        await logout.delete(reason="BOT Settings changed")

        embed = Embed(color=discord.Color.green())
        embed.add_field(name="🤖BOT Settings successfully changed",
                        value="The BOT settings have been successfully changed.\nCHANGE: **Deleting Staff Log system**")
        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def change3(self, ctx):
        Verified = await ctx.guild.create_role(name="✔Verified", color=discord.Color.green())

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True),

        }

        await ctx.guild.create_text_channel("✅verify", overwrites=overwrites)

        embed = Embed(color=discord.Color.green())
        embed.add_field(name="🤖BOT Settings successfully changed",
                        value="The BOT settings have been successfully changed.\nCHANGE: **Setting User Verification System**")
        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def change4(self, ctx):
        Verified = get(ctx.guild.roles, name="✔Verified")
        Mute = get(ctx.guild.roles, name="❌mute")

        login = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }

        logout = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }

        await ctx.guild.create_text_channel("💢log-in", overwrites=login)
        await ctx.guild.create_text_channel("💢log-out", overwrites=logout)

        embed = Embed(color=discord.Color.green())
        embed.add_field(name="🤖BOT Settings successfully changed",
                        value="The BOT settings have been successfully changed.\nCHANGE: **Staff Log System**")
        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def reset(self, ctx):
        Verified = await ctx.guild.create_role(name="✔Verified", color=discord.Color.green())
        await ctx.guild.create_role(name="❌mute", color=discord.Color.orange())
        Mute = get(ctx.guild.roles, name="❌mute")

        login = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }

        logout = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }

        await ctx.guild.create_text_channel("💢log-in", overwrites=login)
        await ctx.guild.create_text_channel("💢log-out", overwrites=logout)
        await ctx.guild.create_text_channel("✅verify", overwrites=overwrites)

        embed = Embed(color=discord.Color.green())
        embed.add_field(name="🤖BOT Settings reset",
                        value="All the BOT settings have been successfully restored.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
    

def setup(client):
    client.add_cog(Preferences(client))