import discord
import os
import time
from discord.ext import commands
from discord import Embed, Color
from discord.utils import get
import asyncio
from dpymenus import Page, PaginatedMenu

client = commands.Bot(command_prefix="t!")
client.remove_command("help")

def read_token():
    with open(".env", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

# Events

@client.event
async def on_ready():
    print("True now online")
    while True:
        await client.change_presence(activity=discord.Game(f"Working in {len(client.guilds)} guilds"))
        await asyncio.sleep(600)

async def find_channel(guild):
    for c in guild.text_channels:
        if not c.permissions_for(guild.me).send_messages:
            continue
        return c
    return None


@client.event
async def on_guild_join(guild):
    channel = await find_channel(guild)
    if channel is None:
        return
    embed = Embed(color=discord.Color.orange())
    embed.add_field(name="✅ True BOT Is Now Online",
                    value="True is Working into your server.\n\n💢BOT Prefix: **t!**\n🔴**If you need help with the bot, type _t!help_**\n\n💎Best Moderation for your server.\n✅Ban\n✅Kick\n✅Users Info\n\nNo More:\n❌Link Spamming\n❌Hackers\n❌Fake Accounts \n\n[💠Vote for me](https://top.gg/758205623401447476)\nTrue has been designed for greater use by the server staff; Most commands need the **🐱‍💻Staff** role from the author of the message. not to avoid mistakes, we recommend assigning this role to all the staff members of the server.\n\nIf you want to know something about True, use the command **t!how_to**.")
    embed.set_footer(text=f"Made by Sal Code\nGitHub: https://bit.ly/32us8mR\nYouTube: https://bit.ly/2CqHjmn\nTwitter: https://bit.ly/399ucC0\nInstagram: https://bit.ly/2CkayYa\nDiscord: https://bit.ly/32UqhHF\nPatreon: https://bit.ly/3eJEJF0\nTimeStamp: {time.ctime()}")

    await channel.send(embed=embed)
    Staff = await guild.create_role(name="🐱‍💻Staff", color=discord.Color.red())
    Verified = await guild.create_role(name="✔Verified", color=discord.Color.green())
    Mute = await guild.create_role(name="❌mute", color=discord.Color.orange())

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        Verified: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True),
        Staff: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, manage_messages=True),
        Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
    }

    login = {
        guild.default_role : discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
        Verified : discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
        Staff: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, manage_messages=True),
        Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
    }

    logout = {
        guild.default_role : discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
        Verified : discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
        Staff: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, manage_messages=True),
        Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
    }

    await guild.create_text_channel("✅verify", overwrites=overwrites)
    await guild.create_text_channel("💢log-in", overwrites=login)
    await guild.create_text_channel("💢log-out", overwrites=logout)

#@client.event
#async def on_command_error(ctx, error):
    #staff = get(ctx.guild.roles, name="🐱‍💻Staff")
    #embed = Embed(color=discord.Color.red())
    #embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAD",
                    #value=f"We're sorry {ctx.author.mention}. The command you're trying to use doesn't exists. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
    #embed.set_footer(text=f"Timestamp: {time.ctime()}")
    
    #await ctx.send(embed=embed)

@client.event
async def on_member_join(ctx):
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

@client.event
async def on_member_remove(ctx):
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

# Commands

@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def helpstaff(ctx):
    try:
        await ctx.author.create_dm()
        embed = Embed(color=discord.Color.red())
        embed.add_field(name="📒True Help Window - ⚠For Staff Only",
                        value="🟠Commands: If you want to see **True** commands: **t!cmd**\n✅Verify: When a New member join the server, to be sure that it's not a fake account or a bot, it will be necessary to perform a verification. To do this, you will need to type the command **t!verify** in the appropriate text channel.\n👑**Staff commands**\n🚩**t!ban**: Use this command to ban a user from the guild. Syntax: ```python\nt!ban @username reason\n```\n🚩**t!kick**: USe this command to kick a user from the guild. Syntax: ```python\nt!kick @username reason\n```\n🚩**t!sudo**: Use this command to alert a user that his/her behavior. Syntax: ```python\nt!sudo @username reason\n```\n\n🚩**t!close**: The staff must use the following command to cancel and close a user-generated ticket.\n🚩**t!mute**: Use this command to mute a member in the guild. Syntax: ```python\nt!mute @username time(EX. 120 10) reason\n```.\nTime in the mute command is in minutes.\n🚩**t!unmute**: Use this command to unmute a member in the guild Syntax: ```python\nt!unmute @username\n```.")
            
        embed.set_footer(text="Made by Sal Code\nGitHub: https://bit.ly/32us8mR\nYouTube: https://bit.ly/2CqHjmn\nTwitter: https://bit.ly/399ucC0\nInstagram: https://bit.ly/2CkayYa\nDiscord: https://bit.ly/32UqhHF\nPatreon: https://bit.ly/3eJEJF0\n")

        await ctx.author.dm_channel.send(embed=embed)
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    await ctx.author.create_dm()
    embed = Embed(color=discord.Color.green())
    embed.add_field(name="📒True Help Window",
                    value="🟠Commands: If you want to see **True** commands: **t!cmd**\n🚩If you need support, use the **t!ticket** command. I will create a new channel called **ticket-yourname**. In that channel you can chat with the staff & discuss about your problem.\n⛔If you find any bug/problem, you can report it at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
    embed.set_footer(text=f"Timestamp: {time.ctime()}")

    await ctx.author.dm_channel.send(embed=embed)

@client.command()
async def verify(ctx):
    try:
        role = get(ctx.guild.roles, name="✔Verified")
        await ctx.author.add_roles(role)

        embed = Embed(color=discord.Color.blue())
        embed.add_field(name=f"USER {ctx.author.mention} VERIFIED CORRECTLY",
                        value=f"The user {ctx.author.mention} has been correctly verified. Now you can access to all the server features.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
        
        await ctx.send(embed=embed)
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.red())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAD",
                        value=f"We're sorry {ctx.author.mention}. The command you're trying to use doesn't exists. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
        
        await ctx.send(embed=embed)

@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def clear(ctx, amount=1000000):
    try:
        await ctx.channel.purge(limit=amount)
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        await ctx.send(embed=embed)


@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def ban(ctx, member: discord.Member, *, reason):
    try:
        await member.ban(reason=reason)
        e18 = Embed(title=f'**USER {member.mention} HAS BEEN BANNED FROM THE SERVER**',
                    color=discord.Color.red())
        e18.add_field(name='**❌USER BANNED❌**',
                    value=f'A USER HAS BEEN BANNED FROM THE SERVER.\n**BAN AUTHOR**: **{ctx.author.mention}**\n**MOTIVATION**: {reason}\n**BANNED USER**: {member.mention}')
        e18.set_footer(text=f"Timestamp: {time.ctime()}")
        await ctx.send(embed=e18)
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        await ctx.send(embed=embed)


@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def kick(ctx, member: discord.Member, *, reason):
    try:
        await member.kick(reason=reason)
        e19 = Embed(title=f'**USER {member.mention} HAS BEEN KICCKED FROM THE SERVER**',
                    color=discord.Color.dark_blue())
        e19.add_field(name='**❌USER KICCKED❌**',
                    value=f'A USER HAS BEEN KICCKED FROM THE SERVER.\n**KICK AUTHOR**: **{ctx.author.mention}**\n**MOTIVATION**: {reason}\n**KICCKED USER**: {member.mention}')
        e19.set_footer(text=f"Timestamp: {time.ctime()}")
        await ctx.send(embed=e19)
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        await ctx.send(embed=embed)

@client.command()
async def ticket(ctx):
    staff = get(ctx.guild.roles, name="🐱‍💻Staff")
    Mute = get(ctx.guild.roles, name="❌mute")
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True),
        staff: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True),
        Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
    }
    
    ticket_role = await ctx.guild.create_role(name=f"❗ticket-{ctx.author}")
    ticket_r = get(ctx.guild.roles, name=f"{ticket_role}")
    await ctx.guild.create_text_channel(f'❗ticket-{ctx.author}', overwrites=overwrites)
    await ctx.author.add_roles(ticket_r)

@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def close(ctx, member : discord.Member, ticket_r):
    try:
        role = get(ctx.guild.roles, name=ticket_r)
        await member.remove_roles(role)
        await ctx.channel.delete(reason="Ticket closed")
        await role.delete()
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        await ctx.send(embed=embed)

@client.command()
async def bugreport(ctx, *, bug):
    e9 = Embed(color=discord.Color.red())
    e9.add_field(name=f'🔻**BUG REPORT MESSAGE FROM {ctx.author.mention}**🔻',
                 value=f'WE THANK YOU FOR YOUR COLLABORATION {ctx.author.mention}! WE WILL TAKE ACCOUNT OF YOUR REPORT AND FIX THE BUG REPORTED TO US.\nREPORTED BUG: **{bug}**')
    e9.set_footer(text=f"Timestamp: {time.ctime()}")
    await ctx.send(embed=e9)


@client.command()
async def usereport(ctx, user : discord.Member, *, reason):
    staff = get(ctx.guild.roles, name="🐱‍💻Staff")
    e10 = Embed(color=discord.Color.red())
    e10.add_field(name=f'🔻**USER REPORT MESSAGE FROM {ctx.author.mention}**🔻',
                  value=f'The following user will be reported: {user.mention}')
    e10.set_footer(text=f"Timestamp: {time.ctime()}")
    await ctx.send(embed=e10)
    await ctx.send(f"{staff.mention}")

@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def sudo(ctx, member : discord.Member, *, reason):
    try:
        embed = Embed(color=discord.Color.red())
        embed.add_field(name=f"⛔**SUDO TO {member.mention}**⛔",
                        value=f"WARNING {member.mention}, you're getting reported by a Staff member. You get a **Sudo**. This means you're doing somwthing wrong. Plese stop.\nSudo's reason: **{reason}**")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
        
        await ctx.send(embed=embed)
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        await ctx.send(embed=embed)

@client.command()
async def cmd(ctx):
    await ctx.author.create_dm()
    embed = Embed(color=discord.Color.teal())
    embed.add_field(name="📒True Commands",
                    value=f"1️⃣: **t!help**: If you need help, I can help you to solve your issues!\n2️⃣: **t!ticket**: If you need support from the staff, you can use this command to generate a ticket. A channel with thw name **❗ticket-yourusername** will be created into the server. Only you and the staff can access to this channel.\n3️⃣: **t!usereport**: If you think a user has a wrong behavior, you can report that user by using this command; Syntax: ```python\nt!usereport @user reason\n```\n4️⃣: **t!bugreport**: If you find a bug into the server, you can report it at the staff by using this command; Syntax: ```python\nt!bugreport bug\n```\n5️⃣: **t!verify**: If you're new in the server you need to verify your self.\n6️⃣: **t!how_to**: To see a detailed documentation about True.")
    embed.set_footer(text=f"Timestamp: {time.ctime()}")
    
    await ctx.author.dm_channel.send(embed=embed)

@client.command()
async def bot_settings(ctx):
    try:
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="🤖BOT GUILD SETTINGS",
                        value="Use this command if you want to change the BOT settings in your server. There some options avaible.\n1️⃣: If you don't want the user verification in your server, just type **bot_change1**.\n2️⃣: If you don't want the Staff Log, just type: **bot_change2**\n3️⃣: If you want only the verification, just type **bot_change3**. **Note: \n4️⃣If you want the Staff Log, just type bot_change4**")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
        
        await ctx.send(embed=embed)
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.red())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAD",
                        value=f"We're sorry {ctx.author.mention}. The command you're trying to use doesn't exists. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
        
        await ctx.send(embed=embed)

@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def bot_change1(ctx):
    try:
        role = get(ctx.guild.roles, name="✔Verified")
        channel = get(ctx.guild.channels, name="✅verify")

        await channel.delete(reason="BOT Settings changed")
        await role.delete()

        embed = Embed(color=discord.Color.green())
        embed.add_field(name="🤖BOT Settings successfully changed",
                        value="The BOT settings have been successfully changed.\nCHANGE: **Deleting Verify system**")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
        
        await ctx.send(embed=embed)
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        await ctx.send(embed=embed)

@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def bot_change2(ctx):
    try:
        login = get(ctx.guild.channels, name="💢log-in")
        logout = get(ctx.guild.channels, name="💢log-out")

        await login.delete(reason="BOT Settings changed")
        await logout.delete(reason="BOT Settings changed")

        embed = Embed(color=discord.Color.green())
        embed.add_field(name="🤖BOT Settings successfully changed",
                        value="The BOT settings have been successfully changed.\nCHANGE: **Deleting Staff Log system**")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
        
        await ctx.send(embed=embed)
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        await ctx.send(embed=embed)

@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def bot_change3(ctx):
    try:
        Verified = await ctx.guild.create_role(name="✔Verified", color=discord.Color.green())
        Staff = get(ctx.guild.roles, name="🐱‍💻Staff")

        overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                Verified: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True),
                Staff: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, manage_messages=True),
            }

        await ctx.guild.create_text_channel("✅verify", overwrites=overwrites)
            
        embed = Embed(color=discord.Color.green())
        embed.add_field(name="🤖BOT Settings successfully changed",
                        value="The BOT settings have been successfully changed.\nCHANGE: **Setting User Verification System**")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
            
        await ctx.send(embed=embed)
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        await ctx.send(embed=embed)

@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def bot_change4(ctx):
    try:
        Verified = get(ctx.guild.roles, name="✔Verified")
        Staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        Mute = get(ctx.guild.roles, name="❌mute")

        login = {
                ctx.guild.default_role : discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
                Verified : discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
                Staff: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, manage_messages=True),
                Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
            }

        logout = {
            ctx.guild.default_role : discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Verified : discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Staff: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, manage_messages=True),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
            }
        
        await ctx.guild.create_text_channel("💢log-in", overwrites=login)
        await ctx.guild.create_text_channel("💢log-out", overwrites=logout)

        embed = Embed(color=discord.Color.green())
        embed.add_field(name="🤖BOT Settings successfully changed",
                            value="The BOT settings have been successfully changed.\nCHANGE: **Staff Log System**")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                
        await ctx.send(embed=embed)
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        await ctx.send(embed=embed)


@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def bot_reset(ctx):
    try:
        Verified = await ctx.guild.create_role(name="✔Verified", color=discord.Color.green())
        await ctx.guild.create_role(name="❌mute", color=discord.Color.orange())
        Staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        Mute = get(ctx.guild.roles, name="❌mute")
        
        login = {
            ctx.guild.default_role : discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Verified : discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Staff: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, manage_messages=True),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }

        logout = {
            ctx.guild.default_role : discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Verified : discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Staff: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, manage_messages=True),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True),
            Staff: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, manage_messages=True),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }

        await ctx.guild.create_text_channel("💢log-in", overwrites=login)
        await ctx.guild.create_text_channel("💢log-out", overwrites=logout)
        await ctx.guild.create_text_channel("✅verify", overwrites=overwrites)

        embed = Embed(color=discord.Color.green())
        embed.add_field(name="🤖BOT Settings reset",
                        value="All the BOT settings have been successfully restored.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
        
        await ctx.send(embed=embed)
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        await ctx.send(embed=embed)


@client.command()
async def how_to(ctx):
    try:
        first_page = Page(color=discord.Color.blue())
        first_page.add_field(name="📒How to set up True for your guild",
                            value="By default, True has a set of automatic settings that, when entering the server, are set as default. The first step consists of generating three chats: One for verification and two to manage the inputs and outputs in the server. The second and final phase consists of the creation of two roles, always related to verification and staff. If you want to change the settings, you can do so by accessing the following commands:\n**bot_change1**\n**bot_change2**\n**bot_change3**\n**bot_change4**. If you would like to learn more about the documentation of the following commands, see **bot_settings**.")
        
        second_page = Page(color=discord.Color.green())
        second_page.add_field(name="📒User Verification",
                            value="Each time a user enters the server, they will have to perform a verification. By performing the verification, the user will have access to all the channels of the server. In case you want to remove the verification system, run the command **t! bot_change1**.")
        
        third_page = Page(color=discord.Color.orange())
        third_page.add_field(name="📒Log-in / Log Out",
                            value="Another of True’s default settings is the creation of two chats dedicated to the inputs and outputs in the server. These chats are especially dedicated to the Server Staff. In case you want to delete the above, use the **t command! bot_change2**.")
        
        fourth_page = Page(color=discord.Color.purple())
        fourth_page.add_field(name="📒Staff Commands",
                            value="To see all the Staff's commands, use the command **t!helpstaff**")
        
        fifth_page = Page(color=discord.Color.magenta())
        fifth_page.add_field(name="📒Users commands",
                            value="Tp see all the User's commands, use the command **t!cmd**")

        menu = PaginatedMenu(ctx)
        menu.add_pages([first_page, second_page, third_page, fourth_page, fifth_page])
        await menu.open()

    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.red())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAD",
                        value=f"We're sorry {ctx.author.mention}. The command you're trying to use doesn't exists. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
        
        await ctx.send(embed=embed)

@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def mute(ctx, member : discord.Member, time_mute : int, *, reason):
    #try:
    role = get(ctx.guild.roles, name="❌mute")
    await member.add_roles(role)

    embed = Embed(color=discord.Color.gold())
    embed.add_field(name="**❌MEMBER MUTED IN THE GUILD**",
                        value=f"The member {member.mention} has been muted in the guild.\nTime: **{time_mute}** minutes\nReason: **{reason}**.\nStaff member: {ctx.author.mention}",)
    embed.set_footer(text=f"Timestamp: {time.ctime()}")
        
    await ctx.send(embed=embed)

    with open("files/log.txt", "w") as f:
        f.write(f"{ctx.author}:{time_mute}")
        f.close()
    
    #except:
        #staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        #embed = Embed(color=discord.Color.orange())
        #embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        #value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        #embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        #await ctx.send(embed=embed)

@client.command()
@commands.has_any_role("🐱‍💻Staff")
async def unmute(ctx, member : discord.Member):
    try:
        role = get(ctx.guild.roles, name="❌mute")
        await member.remove_roles(role)

        embed = Embed(color=discord.Color.purple())
        embed.add_field(name="**❌MEMBER UNMUTED IN THE GUILD**",
                            value=f"The member {member.mention} has been unmuted in the guild.\nStaff member: {ctx.author.mention}",)
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
            
        await ctx.send(embed=embed)

        f = open('files/log.txt', 'r+')
        f.truncate(0)
        f.close()
    
    except:
        staff = get(ctx.guild.roles, name="🐱‍💻Staff")
        embed = Embed(color=discord.Color.orange())
        embed.add_field(name="❓ERROR WHILE TRYING USING THE COMMAND",
                        value=f"We're sorry {ctx.author.mention}. If see this message, it knows that you don't have the necessary permissions to use this command. If you think this is an error, please contact the {staff.mention}. If you think this's a BOT error, please report at: https://forms.gle/sH97ZjbR7opgU9ic6. Thanks for your contribution.")
        embed.set_footer(text=f"Timestamp: {time.ctime()}")
                    
        await ctx.send(embed=embed)

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        client.load_extension(f"cogs.{file[:-3]}")

client.run(token)
