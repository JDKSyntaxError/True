import discord
import os
import time
from pathlib import Path
from discord.ext import commands
from discord import Embed, Color
from discord.utils import get
import asyncio
from dpymenus import Page, PaginatedMenu
    

class GuildJoin(commands.Cog):
    def __init__(self, client):
        self.client = client    
    
    async def find_channel(self, guild):
        for c in guild.text_channels:
            if not c.permissions_for(guild.me).send_messages:
                continue
            return c
        return None

    @commands.Cog.listener()
    async def on_guild_join(self, guild, find_channel):
        channel = await find_channel(guild)
        if channel is None:
            return
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="✅ True BOT Is Now Online",
                        value="True is Working into your server.\n\n💢BOT Prefix: **t!**\n🔴**If you need help with the bot, type _t!help_**\n\n💎Best Moderation for your server.\n✅Ban\n✅Kick\n✅Users Info\n\nNo More:\n❌Link Spamming\n❌Hackers\n❌Fake Accounts \n\nTrue has been designed for greater use by the server staff.\n\nIf you want to know something about True, use the command **t!how_to**.")
        embed.set_footer(
            text=f"Made by Sal Code\nGitHub: https://bit.ly/32us8mR\nYouTube: https://bit.ly/2CqHjmn\nTwitter: https://bit.ly/399ucC0\nInstagram: https://bit.ly/2CkayYa\nDiscord: https://bit.ly/32UqhHF\nPatreon: https://bit.ly/3eJEJF0\nTimeStamp: {time.ctime()}")

        await channel.send(embed=embed)
        Verified = await guild.create_role(name="✔Verified", color=discord.Color.green())
        Mute = await guild.create_role(name="❌mute", color=discord.Color.orange())

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }

        login = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }

        logout = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }

        await guild.create_text_channel("✅verify", overwrites=overwrites)
        await guild.create_text_channel("💢log-in", overwrites=login)
        await guild.create_text_channel("💢log-out", overwrites=logout)

def setup(client):
    client.add_cog(GuildJoin(client))