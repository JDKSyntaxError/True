import discord
import os
import time
from pathlib import Path
from discord.ext import commands
from discord import Embed, Color
from discord.utils import get
import asyncio
from dpymenus import Page, PaginatedMenu

class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def helpstaff(self, ctx):
        await ctx.author.create_dm()
        embed = Embed(color=discord.Color.red())
        embed.add_field(name="📒True Help Window - ⚠For Staff Only",
                        value="`ban` `kick` `mute`\n`unmute` `sudo` `warn`\n`tell` `sets` `whois`\n`close` `change[1-2-3-4]` `reset`")

        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.author.dm_channel.send(embed=embed)


    @commands.command()
    async def help(self, ctx):
        await ctx.author.create_dm()
        embed = Embed(color=discord.Color.green())
        embed.add_field(name="📒True Help Window",
                        value="🟠Commands: If you want to see **True** commands: **t!cmd**\n🚩If you need support, use the **t!ticket** command. I will create a new channel called **ticket-yourname**. In that channel you can chat with the staff & discuss about your problem.\n⛔If you find any bug/problem, you can report it at [Our Form](https://forms.gle/sH97ZjbR7opgU9ic6). Thanks for your contribution.\n🌎Visit [Our WebSite](https://truebot.ml)\n🔥[Vote US](https://discord.ly/true)")
        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.author.dm_channel.send(embed=embed)


    @commands.command()
    async def bugreport(self, ctx, *, bug):
        e9 = Embed(color=discord.Color.red())
        e9.add_field(name=f'🔻**BUG REPORT MESSAGE FROM {ctx.author.mention}**🔻',
                    value=f'WE THANK YOU FOR YOUR COLLABORATION {ctx.author.mention}! WE WILL TAKE ACCOUNT OF YOUR REPORT AND FIX THE BUG REPORTED TO US.\nREPORTED BUG: **{bug}**')
        e9.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e9)


    @commands.command()
    async def usereport(self, ctx, user: discord.Member, *, reason):
        e10 = Embed(color=discord.Color.red())
        e10.add_field(name=f'🔻**USER REPORT MESSAGE FROM {ctx.author.mention}**🔻',
                    value=f'The following user will be reported: {user.mention}')
        e10.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e10)


    @commands.command()
    async def cmd(self, ctx):
        await ctx.author.create_dm()
        embed = Embed(color=discord.Color.teal())
        embed.add_field(name="📒True Commands",
                        value=f"`helpstaff` `help` `verify`\n `whois` `ban` `kick`\n `mute` `unmute` `clear`\n`change1` `change2` `change3`\n`change4` `reset` `ticket`\n`close` `sudo` `bugreport`\n`usereport` `warn`\n`tell` `sets` `show_settings`")
        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.author.dm_channel.send(embed=embed)
    
    @commands.command()
    async def how_to(self, ctx):
        true = self.client.get_user(758205623401447476)

        initial = Page(color=discord.Color.red())
        initial.add_field(name="📚Official Documentation",
                            value="This command is only a short mode od our documentation.\nTo visit the full documentation, please [Visit Here](https://salazar34.github.io/True)")
        
        initial.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        first_page = Page(color=discord.Color.blue())      
        first_page.add_field(name="📒How to set up True for your guild",
                            value="By default, True has a set of automatic settings that, when entering the server, are set as default. The first step consists of generating three chats: One for verification and two to manage the inputs and outputs in the server. The second and final phase consists of the creation of two roles, always related to verification and staff. If you want to change the settings, you can do so by accessing the following commands:\n**change1**\n**change2**\n**change3**\n**change4**. If you would like to learn more about the documentation of the following commands, see **show_settings**.")
        
        first_page.set_footer(text=f"PAGE 1/5\nTimestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        second_page = Page(color=discord.Color.green())
        second_page.add_field(name="📒User Verification",
                            value=f"Each time a user enters the server, they will have to perform a verification. By performing the verification, the user will have access to all the channels of the server. In case you want to remove the verification system, run the command **t!change1**. The verification system works like a Captcha System. The user has to wirte the correct combination of characters to pass the verification. If the user pass, than {true.mention} will give him/her the **✔Verified** role.")
        
        second_page.set_footer(text=f"PAGE 2/5\nTimestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        third_page = Page(color=discord.Color.orange())
        third_page.add_field(name="📒Log-in / Log Out",
                            value="Another of True’s default settings is the creation of two chats dedicated to the inputs and outputs in the server. These chats are especially dedicated to the Server Staff. In case you want to delete the above, use the **t!change2**.")
        
        third_page.set_footer(text=f"PAGE 3/5\nTimestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        fourth_page = Page(color=discord.Color.purple())
        fourth_page.add_field(name="📒Staff Commands",
                            value=f"To see all the Staff's commands, use the command **t!helpstaff**. {true.mention} will create a DM chat with you & send you all the Staff's dedicated commands. Note that to use the moderation commands, you need to get special permissions on the server, for exmaple: Ban users, namage messages, Administrator etc...")
        
        fourth_page.set_footer(text=f"PAGE 4/5\nTimestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        fifth_page = Page(color=discord.Color.magenta())
        fifth_page.add_field(name="📒Users commands",
                            value=f"To see all the User's commands, use the command **t!cmd**. {true.mention} will send you all the user commands.")
        
        fifth_page.set_footer(text=f"PAGE 5/5\nTimestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        menu = PaginatedMenu(ctx)
        menu.add_pages(
            [initial, first_page, second_page, third_page, fourth_page, fifth_page])
        await menu.open()


def setup(client):
    client.add_cog(HelpCommand(client))