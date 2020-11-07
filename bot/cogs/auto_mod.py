import asyncio
import os
import time
from typing import Optional
import discord
from discord import Color, Embed
from discord.ext import commands
from discord.utils import get
from dpymenus import Page, PaginatedMenu


class AutoMod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        bad_words = ['4r5e', '5h1t', '5hit', 'a55', 'anal,anus', 'ar5e', 'arrse', 'arse', 'ass,ass-fucker', 'asses,assfucker', 'assfukka', 'asshole', 'assholes', 'asswhole', 'a_s_s', 'b!tch', 'b00bs', 'b17ch', 'b1tch', 'ballbag', 'balls', 'ballsack', 'bastard', 'beastial', 'beastiality', 'bellend', 'bestial', 'bestiality', 'bi+ch', 'biatch', 'bitch', 'bitcher', 'bitchers', 'bitches', 'bitchin', 'bitching', 'bloody', 'blowjob', 'blowjob', 'blowjobs', 'boiolas', 'bollock', 'bollok', 'boner', 'boob', 'boobs', 'booobs', 'boooobs', 'booooobs', 'booooooobs', 'breasts', 'buceta', 'bugger', 'bum', 'bunnyfucker', 'butt', 'butthole', 'buttmunch', 'buttplug', 'c0ck', 'c0cksucker', 'carpetmuncher', 'cawk', 'chink', 'cipa', 'cl1t', 'clit', 'clitoris', 'clits', 'cnut', 'cock', 'cock-sucker', 'cockface', 'cockhead', 'cockmunch', 'cockmuncher', 'cocks', 'cocksuck', 'cocksucked', 'cocksucker', 'cocksucking', 'cocksucks', 'cocksuka', 'cocksukka', 'cok', 'cokmuncher', 'coksucka', 'coon', 'cox', 'crap', 'cum', 'cummer', 'cumming', 'cums', 'cumshot', 'cunilingus', 'cunillingus', 'cunnilingus', 'cunt', 'cuntlick', 'cuntlicker', 'cuntlicking', 'cunts', 'cyalis', 'cyberfuc', 'cyberfuck', 'cyberfucked', 'cyberfucker', 'cyberfuckers', 'cyberfucking', 'd1ck', 'damn', 'dick', 'dickhead', 'dildo', 'dildos', 'dink', 'dinks', 'dirsa', 'dlck', 'dog-fucker', 'doggin', 'dogging', 'donkeyribber', 'doosh', 'duche', 'dyke', 'ejaculate', 'ejaculated', 'ejaculates', 'ejaculating', 'ejaculatings', 'ejaculation', 'ejakulate', 'fuck', 'fucker', 'f4nny', 'fag', 'fagging', 'faggitt', 'faggot', 'faggs', 'fagot', 'fagots', 'fags', 'fanny', 'fannyflaps', 'fannyfucker', 'fanyy', 'fatass', 'fcuk', 'fcuker', 'fcuking', 'feck', 'fecker', 'felching', 'fellate', 'fellatio', 'fingerfuck', 'fingerfucked', 'fingerfucker', 'fingerfuckers', 'fingerfucking', 'fingerfucks', 'fistfuck', 'fistfucked', 'fistfucker', 'fistfuckers', 'fistfucking', 'fistfuckings', 'fistfucks', 'flange', 'fook', 'fooker', 'fuck', 'fucka', 'fucked', 'fucker', 'fuckers', 'fuckhead', 'fuckheads', 'fuckin', 'fucking', 'fuckings', 'fuckingshitmotherfucker', 'fuckme', 'fucks', 'fuckwhit', 'fuckwit', 'fudgepacker', 'fudgepacker', 'fuk', 'fuker', 'fukker', 'fukkin', 'fuks', 'fukwhit', 'fukwit', 'fux', 'fux0r', 'f_u_c_k', 'gangbang', 'gangbanged', 'gangbangs', 'gaylord', 'gaysex', 'goatse', 'God', 'god-dam', 'god-damned', 'goddamn', 'goddamned', 'hardcoresex', 'hell', 'heshe', 'hoar', 'hoare', 'hoer', 'homo', 'hore', 'horniest', 'horny', 'hotsex', 'jack-off', 'jackoff', 'jap', 'jerk-off', 'jism', 'jiz', 'jizm', 'jizz', 'kawk', 'knob', 'knobead', 'knobed', 'knobend', 'knobhead', 'knobjocky', 'knobjokey', 'kock', 'kondum', 'kondums', 'kum', 'kummer', 'kumming', 'kums', 'kunilingus', 'l3i+ch', 'l3itch', 'labia', 'lmfao', 'lust', 'lusting', 'm0f0', 'm0fo', 'm45terbate', 'ma5terb8', 'ma5terbate', 'masochist', 'master-bate', 'masterb8', 'masterbat*', 'masterbat3', 'masterbate', 'masterbation', 'masterbations', 'masturbate', 'mo-fo', 'mof0', 'mofo', 'mothafuck', 'mothafucka', 'mothafuckas', 'mothafuckaz', 'mothafucked', 'mothafucker', 'mothafuckers', 'mothafuckin', 'mothafucking', 'mothafuckings', 'mothafucks', 'motherfucker', 'motherfuck', 'motherfucked', 'motherfucker', 'motherfuckers', 'motherfuckin', 'motherfucking', 'motherfuckings', 'motherfuckka', 'motherfucks', 'muff', 'mutha', 'muthafecker', 'muthafuckker', 'muther', 'mutherfucker', 'n1gga', 'n1gger', 'nigg3r', 'nigg4h', 'nigga', 'niggah', 'niggas', 'niggaz', 'nigger', 'niggers', 'nob', 'nobjokey', 'nobhead', 'nobjocky', 'nobjokey', 'numbnuts', 'nutsack', 'orgasim', 'orgasims', 'orgasm', 'orgasms', 'p0rn', 'pawn', 'pecker', 'penis', 'penisfucker', 'phonesex', 'phuck', 'phuk', 'phuked', 'phuking', 'phukked', 'phukking', 'phuks', 'phuq', 'pigfucker', 'pimpis', 'piss', 'pissed', 'pisser', 'pissers', 'pisses', 'pissflaps', 'pissin', 'pissing', 'pissoff', 'poop', 'porn', 'porno', 'pornography', 'pornos', 'prick', 'pricks', 'pron', 'pube', 'pusse', 'pussi', 'pussies', 'pussy', 'pussys', 'rectum', 'retard', 'rimjaw', 'rimming', 'shit', 's.o.b.', 'sadist', 'schlong', 'screwing', 'scroat', 'scrote', 'scrotum', 'semen', 'sex', 'sh!+' , 'sh!t', 'sh1t', 'shag', 'shagger', 'shaggin', 'shagging', 'shemale', 'shi+', 'shit', 'shitdick', 'shite', 'shited', 'shitey', 'shitfuck', 'shitfull', 'shithead', 'shiting', 'shitings', 'shits', 'shitted', 'shitter', 'shitters', 'shitting', 'shittings', 'shitty', 'skank', 'slut', 'sluts', 'smegma', 'smut', 'snatch', 'son-of-a-bitch, spac', 'spunk', 's_h_i_t', 't1tt1e5', 't1tties', 'teets', 'teez', 'testical', 'testicle', 'tit', 'titfuck', 'tits', 'titt', 'tittie5', 'tittiefucker', 'titties', 'tittyfuck', 'tittywank', 'titwank', 'tosser', 'turd', 'tw4t', 'twat', 'twathead', 'twatty', 'twunt', 'twunter', 'v14gra', 'v1gra', 'vagina', 'viagra', 'vulva', 'w00se', 'wang', 'wank', 'wanker', 'wanky', 'whoar', 'whore', 'willies', 'willy', 'xrated', 'xxx']

        if get(message.guild.roles, name="✔Verified"):
            ver = get(message.guild.roles, name="✔Verified")
            muted = get(message.guild.roles, name="❌mute")

            for word in bad_words:
                if message.content.count(str(word)) > 0:
                    await message.channel.purge(limit=1)
                    embed = Embed(color=discord.Color.red())
                    embed.add_field(name="🔺BAD WORD HAS BEEN SAYD",
                                    value=f"A bad word has been sayd:\n**Author**: {message.author.mention}\n**Word**: {word}\n**Channel**: {message.channel}")

                    embed.set_footer(
                        text=f"Timestamp: {time.ctime()}\nAutomoderation System", icon_url=message.author.avatar_url)

                    await message.channel.send(embed=embed)
                    await message.author.remove_roles(ver)
                    await message.author.add_roles(muted)

        else:
            muted = get(message.guild.roles, name="❌mute")

            for word in bad_words:
                if message.content.count(str(word)) > 0:
                    await message.channel.purge(limit=1)
                    embed = Embed(color=discord.Color.red())
                    embed.add_field(name="🔺BAD WORD HAS BEEN SAYD",
                                    value=f"A bad word has been sayd:\n**Author**: {message.author.mention}\n**Word**: {word}\n**Channel**: {message.channel}")

                    embed.set_footer(
                        text=f"Timestamp: {time.ctime()}\nAutomoderation System", icon_url=message.author.avatar_url)

                    await message.channel.send(embed=embed)
                    await message.author.add_roles(muted)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason):
        await member.ban(reason=reason)
        e18 = Embed(title=f'**USER {member.mention} HAS BEEN BANNED FROM THE SERVER**',
                    color=discord.Color.red())
        e18.add_field(name='**❌USER BANNED❌**',
                      value=f'A USER HAS BEEN BANNED FROM THE SERVER.\n**BAN AUTHOR**: **{ctx.author.mention}**\n**MOTIVATION**: {reason}\n**BANNED USER**: {member.mention}')
        e18.set_footer(
            text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e18)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason):
        await member.kick(reason=reason)
        e19 = Embed(color=discord.Color.red())
        e19.add_field(name='**❌USER KICCKED❌**',
                      value=f'A USER HAS BEEN KICCKED FROM THE SERVER.\n**KICK AUTHOR**: **{ctx.author.mention}**\n**MOTIVATION**: {reason}\n**KICCKED USER**: {member.mention}')
        e19.set_footer(
            text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e19)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def sudo(self, ctx, member: discord.Member, *, reason):
        embed = Embed(color=discord.Color.red())
        embed.add_field(name=f"⛔**SUDO TO {member.mention}**⛔",
                        value=f"WARNING {member.mention}, you're getting reported by a Staff member. You got a **Sudo**. This means you're doing something wrong. Plese stop.\nReason: **{reason}**")
        embed.set_footer(
            text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason, role=Optional[discord.Role]):
        if get(ctx.guild.roles, name="✔Verified"):
            role = get(ctx.guild.roles, name="❌mute")
            ver = get(ctx.guild.roles, name="✔Verified")
            await member.remove_roles(ver)
            await member.add_roles(role)

            embed = Embed(color=discord.Color.gold())
            embed.add_field(name="**❌MEMBER MUTED IN THE GUILD**",
                            value=f"The member {member.mention} has been muted in the guild.\nReason: **{reason}**.\nStaff member: {ctx.author.mention}",)
            embed.set_footer(
                text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

        else:
            role = get(ctx.guild.roles, name="❌mute")
            await member.add_roles(role)

            embed = Embed(color=discord.Color.gold())
            embed.add_field(name="**❌MEMBER MUTED IN THE GUILD**",
                            value=f"The member {member.mention} has been muted in the guild.\nReason: **{reason}**.\nStaff member: {ctx.author.mention}",)
            embed.set_footer(
                text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, member: discord.Member, role=Optional[discord.Role]):
        if get(ctx.guild.roles, name="✔Verified"):
            role = get(ctx.guild.roles, name="❌mute")
            ver = get(ctx.guild.roles, name="✔Verified")
            await member.remove_roles(role)
            await member.add_roles(ver)

            embed = Embed(color=discord.Color.purple())
            embed.add_field(name="**❌MEMBER UNMUTED IN THE GUILD**",
                            value=f"The member {member.mention} has been unmuted in the guild.\nStaff member: {ctx.author.mention}",)
            embed.set_footer(
                text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

        else:
            role = get(ctx.guild.roles, name="❌mute")
            await member.remove_roles(role)
            await member.set_permissions(send_messages=True, read_messages=True)

            embed = Embed(color=discord.Color.purple())
            embed.add_field(name="**❌MEMBER UNMUTED IN THE GUILD**",
                            value=f"The member {member.mention} has been unmuted in the guild.\nStaff member: {ctx.author.mention}",)
            embed.set_footer(
                text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)
    
    @commands.command(name="warn", aliases=['warn_user'])
    async def warn_command(self, ctx, user : discord.Member, *, text):
        await user.send(text)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="❗**BAN** COMMAND ERROR",
                            value=f"{ctx.author.mention} you've missed a **Required Argument** when trying to use the command. Please retry.")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingPermissions):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="❗**BAN** COMMAND ERROR",
                            value=f"We're sorry {ctx.author.mention}. You don't have necessary permissions to use this command.")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="❗**KICK** COMMAND ERROR",
                            value=f"{ctx.author.mention} you've missed a **Required Argument** when trying to use the command. Please retry.")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingPermissions):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="❗**KICK** COMMAND ERROR",
                            value=f"We're sorry {ctx.author.mention}. You don't have necessary permissions to use this command.")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="❗**MUTE** COMMAND ERROR",
                            value=f"{ctx.author.mention} you've missed a **Required Argument** when trying to use the command. Please retry.")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingPermissions):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="❗**MUTE** COMMAND ERROR",
                            value=f"We're sorry {ctx.author.mention}. You don't have necessary permissions to use this command.")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="❗**UNMUTE** COMMAND ERROR",
                            value=f"{ctx.author.mention} you've missed a **Required Argument** when trying to use the command. Please retry.")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingPermissions):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="❗**UNMUTE** COMMAND ERROR",
                            value=f"We're sorry {ctx.author.mention}. You don't have necessary permissions to use this command.")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)

    @sudo.error
    async def sudo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="❗**SUDO** COMMAND ERROR",
                            value=f"{ctx.author.mention} you've missed a **Required Argument** when trying to use the command. Please retry.")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingPermissions):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="❗**SUDO** COMMAND ERROR",
                            value=f"We're sorry {ctx.author.mention}. You don't have necessary permissions to use this command.")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)
    
    @warn_command.error
    async def wanr_command_error(self, ctx, exc):
        if isinstance(exc, commands.MissingPermissions):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="❗**WARN** COMMAND ERROR",
                            value=f"We're sorry {ctx.author.mention}. You don't have necessary permissions to use this command.")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(AutoMod(client))
