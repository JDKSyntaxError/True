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
                        value="🟠Commands: If you want to see **True** commands: **t!cmd**\n✅Verify: When a New member join the server, to be sure that it's not a fake account or a bot, it will be necessary to perform a verification. To do this, you will need to type the command **t!verify** in the appropriate text channel.\n👑**Staff commands**\n🚩**t!ban**: Use this command to ban a user from the guild. Syntax: ```python\nt!ban @username reason\n```\n🚩**t!kick**: USe this command to kick a user from the guild. Syntax: ```python\nt!kick @username reason\n```\n🚩**t!sudo**: Use this command to alert a user that his/her behavior. Syntax: ```python\nt!sudo @username reason\n```\n\n🚩**t!close**: The staff must use the following command to cancel and close a user-generated ticket.\n🚩**t!mute**: Use this command to mute a member in the guild. Syntax: ```python\nt!mute @username time(EX. 120 10) reason\n```.\nTime in the mute command is in minutes.\n🚩**t!unmute**: Use this command to unmute a member in the guild Syntax: ```python\nt!unmute @username\n```.")

        embed.set_footer(text="Made by Sal Code\nGitHub: https://bit.ly/32us8mR\nYouTube: https://bit.ly/2CqHjmn\nTwitter: https://bit.ly/399ucC0\nInstagram: https://bit.ly/2CkayYa\nDiscord: https://bit.ly/32UqhHF\nPatreon: https://bit.ly/3eJEJF0\n")

        await ctx.author.dm_channel.send(embed=embed)


    @commands.command()
    async def help(self, ctx):
        await ctx.author.create_dm()
        embed = Embed(color=discord.Color.green())
        embed.add_field(name="📒True Help Window",
                        value="🟠Commands: If you want to see **True** commands: **t!cmd**\n🚩If you need support, use the **t!ticket** command. I will create a new channel called **ticket-yourname**. In that channel you can chat with the staff & discuss about your problem.\n⛔If you find any bug/problem, you can report it at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
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
                        value=f"1️⃣: **t!help**: If you need help, I can help you to solve your issues!\n2️⃣: **t!ticket**: If you need support from the staff, you can use this command to generate a ticket. A channel with thw name **❗ticket-yourusername** will be created into the server. Only you and the staff can access to this channel.\n3️⃣: **t!usereport**: If you think a user has a wrong behavior, you can report that user by using this command; Syntax: ```python\nt!usereport @user reason\n```\n4️⃣: **t!bugreport**: If you find a bug into the server, you can report it at the staff by using this command; Syntax: ```python\nt!bugreport bug\n```\n5️⃣: **t!verify**: If you're new in the server you need to verify your self.\n6️⃣: **t!how_to**: To see a detailed documentation about True.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.author.dm_channel.send(embed=embed)
    
    @commands.command()
    async def how_to(self, ctx):
        true = self.client.get_user(758205623401447476)
        first_page = Page(color=discord.Color.blue())
        first_page.add_field(name="📒How to set up True for your guild",
                            value="By default, True has a set of automatic settings that, when entering the server, are set as default. The first step consists of generating three chats: One for verification and two to manage the inputs and outputs in the server. The second and final phase consists of the creation of two roles, always related to verification and staff. If you want to change the settings, you can do so by accessing the following commands:\n**change1**\n**change2**\n**bot_change3**\n**change4**. If you would like to learn more about the documentation of the following commands, see **settings**.")
        
        first_page.set_footer(text=f"PAGE 1/5\nTimestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        second_page = Page(color=discord.Color.green())
        second_page.add_field(name="📒User Verification",
                            value=f"Each time a user enters the server, they will have to perform a verification. By performing the verification, the user will have access to all the channels of the server. In case you want to remove the verification system, run the command **t!change1**. The verification system works like a Captcha System. The user has to wirte the correct combination of characters to pass the verification. If the user pass, than {true.mention} will give him/her the **✔Verified** role.")
        
        second_page.set_footer(text=f"PAGE 2/5\nTimestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        third_page = Page(color=discord.Color.orange())
        third_page.add_field(name="📒Log-in / Log Out",
                            value="Another of True’s default settings is the creation of two chats dedicated to the inputs and outputs in the server. These chats are especially dedicated to the Server Staff. In case you want to delete the above, use the **t command! bot_change2**.")
        
        third_page.set_footer(text=f"PAGE 3/5\nTimestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        fourth_page = Page(color=discord.Color.purple())
        fourth_page.add_field(name="📒Staff Commands",
                            value=f"To see all the Staff's commands, use the command **t!helpstaff**. {true.mention} will create a DM chat with you & send you all the Staff's dedicated commands. Note that to use the moderation commands, you need to get special permissions on the server, for exmaple: Ban users, namage messages, Administrator etc...")
        
        fourth_page.set_footer(text=f"PAGE 4/5\nTimestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        fifth_page = Page(color=discord.Color.magenta())
        fifth_page.add_field(name="📒Users commands",
                            value=f"To see all the User's commands, use the command **t!cmd**. {true.mention} will send you all the user commands.")
        
        fifth_page.set_footer(text=f"PAGE 5/5**\nTimestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        menu = PaginatedMenu(ctx)
        menu.add_pages(
            [first_page, second_page, third_page, fourth_page, fifth_page])
        await menu.open()


def setup(client):
    client.add_cog(HelpCommand(client))