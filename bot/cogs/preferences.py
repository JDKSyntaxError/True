import discord
import os
import time
import json
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
    async def show_settings(self, ctx):
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="🤖BOT GUILD SETTINGS",
                        value="Use this command if you want to change the BOT settings in your server. There some options avaible.\n1️⃣: If you don't want the user verification in your server, just type **change1**.\n2️⃣: If you don't want the Staff Log, just type: **change2**\n3️⃣: If you want only the verification, just type **change3**. **Note: \n4️⃣If you want the Staff Log, just type **change4**")
        embed.set_footer(
            text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

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
        embed.set_footer(
            text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

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
        embed.set_footer(
            text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

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
        embed.set_footer(
            text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

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
        embed.set_footer(
            text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

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
        embed.set_footer(
            text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="settings", aliases=['current_settings', 'sets'])
    @commands.has_permissions(ban_members=True)
    async def settings_command(self, ctx):
        if get(ctx.guild.channels, name="✅verify") and get(ctx.guild.channels, name="💢log-in") and get(ctx.guild.channels, name="💢log-in"):
            embed = Embed(color=discord.Color.green())
            embed.set_footer(
                text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name=f"🔧{str(ctx.guild.name).upper()} CURRENT SETTINGS",
                            value=f"In this page, {ctx.author.mention} you can see the current settings in your guild. If you need to change something, please use **t!show_settings** or the **t!how_to** commands to see how to change the current settings.")

            embed.add_field(name="⭕VERIFICATION SYSTEM SETTINGS",
                            value="**✅**\nThe verification system is activate and it's correctly working.")

            embed.add_field(name="⭕MOD LOG SYSTEM",
                            value="**✅**\nThe moderation log system is activate and it's correctly working.")

            embed.add_field(name="🐦PROTECTION AND EFFICIENCY BALANCE",
                            value="The guild has the **100%** of protection rate. All the systems are activate and are correctly working. 💪")

            await ctx.send(embed=embed)

        elif get(ctx.guild.channels, name="✅verify") and not get(ctx.guild.channels, name="💢log-in") and not get(ctx.guild.channels, name="💢log-in"):
            embed = Embed(color=discord.Color.green())
            embed.set_footer(
                text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name=f"🔧{str(ctx.guild.name).upper()} CURRENT SETTINGS",
                            value=f"In this page, {ctx.author.mention} you can see the current settings in your guild. If you need to change something, please use **t!show_settings** or the **t!how_to** commands to see how to change the current settings.")

            embed.add_field(name="⭕VERIFICATION SYSTEM SETTINGS",
                            value="**✅**\nThe verification system is activate and it's correctly working.")

            embed.add_field(name="⭕MOD LOG SYSTEM",
                            value="**❌**\nThe moderation log system is activate and it's correctly working.")

            embed.add_field(name="🐦PROTECTION AND EFFICIENCY BALANCE",
                            value="The guild has the **50%** of protection rate. The log system isn't activate yet. We recommend you to activate the log system to get the maximum control and protection in your guild.")

            await ctx.send(embed=embed)

        elif not get(ctx.guild.channels, name="✅verify") and get(ctx.guild.channels, name="💢log-in") and get(ctx.guild.channels, name="💢log-in"):
            embed = Embed(color=discord.Color.green())
            embed.set_footer(
                text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name=f"🔧{str(ctx.guild.name).upper()} CURRENT SETTINGS",
                            value=f"In this page, {ctx.author.mention} you can see the current settings in your guild. If you need to change something, please use **t!show_settings** or the **t!how_to** commands to see how to change the current settings.")

            embed.add_field(name="⭕VERIFICATION SYSTEM SETTINGS",
                            value="**❌**\nThe verification system is activate and it's correctly working.")

            embed.add_field(name="⭕MOD LOG SYSTEM",
                            value="**✅**\nThe moderation log system is activate and it's correctly working.")

            embed.add_field(name="🐦PROTECTION AND EFFICIENCY BALANCE",
                            value="The guild has the **50%** of protection rate. The Captcha verification system isn't activate yet. We recommend you to activate the verification system to get the maximum control and protection in your guild.")

            await ctx.send(embed=embed)

        elif not get(ctx.guild.channels, name="✅verify") and not get(ctx.guild.channels, name="💢log-in") and not get(ctx.guild.channels, name="💢log-in"):
            embed = Embed(color=discord.Color.green())
            embed.set_footer(
                text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name=f"🔧{str(ctx.guild.name).upper()} CURRENT SETTINGS",
                            value=f"In this page, {ctx.author.mention} you can see the current settings in your guild. If you need to change something, please use **t!show_settings** or the **t!how_to** commands to see how to change the current settings.")

            embed.add_field(name="⭕VERIFICATION SYSTEM SETTINGS",
                            value="**❌**\nThe verification system isn't activate.")

            embed.add_field(name="⭕MOD LOG SYSTEM",
                            value="**❌**\nThe moderation log system isn't activate.")

            embed.add_field(name="🐦PROTECTION AND EFFICIENCY BALANCE",
                            value="The guild has the **0%** of protection rate. The Captcha verification system and log system aren't activate yet. We recommend you to activate the all of them to get the maximum control and protection in your guild.")

            await ctx.send(embed=embed)

    
    @settings_command.error
    async def settings_command_error(self, exc, ctx):
        if isinstance(exc, commands.MissingPermissions):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="❗**SETTINGS** COMMAND ERROR",
                            value=f"We're sorry {ctx.author.mention}. You don't have necessary permissions to use this command.")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Preferences(client))