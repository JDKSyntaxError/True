import discord
import os
import time
import asyncio
from typing import Optional
from pathlib import Path
from discord.ext import commands
from discord import Embed, Color
from discord.utils import get
from dpymenus import Page, PaginatedMenu

class TicketSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="ticket")
    async def ticket(self, ctx):
        Mute = get(ctx.guild.roles, name="❌mute")
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }

        ticket_role = await ctx.guild.create_role(name=f"❗ticket-{ctx.author}")
        ticket_r = get(ctx.guild.roles, name=f"{ticket_role}")
        ticket_channel = await ctx.guild.create_text_channel(f'❗ticket-{ctx.author}', overwrites=overwrites)
        await ctx.author.add_roles(ticket_r)

        embed = Embed(color=discord.Color.gold())
        embed.set_author(name=ctx.author,
                        icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="🔺TICKET SYSTEM",
                        value=f"{ctx.author.mention} you ticket has been created: {ticket_channel}")
        
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def close(self, ctx, member : discord.Member, ticket_r):
        role = get(ctx.guild.roles, name=ticket_r)
        await member.remove_roles(role)
        await ctx.channel.delete(reason="Ticket closed")
        await role.delete()
    

def setup(client):
    client.add_cog(TicketSystem(client))