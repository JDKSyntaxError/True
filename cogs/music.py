import discord
import random
import os
import time
import wavelink
import re
import typing as t
from discord.ext import commands
from discord import Embed, Color
from discord.utils import get
from enum import Enum
import asyncio
from dpymenus import Page, PaginatedMenu

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

OPTIONS = {
    "1️⃣": 0,
    "2️⃣": 1,
    "3️⃣": 2,
    "4️⃣": 3,
    "5️⃣": 4,
}

class AlreadyConnectedToChannel(commands.CommandError):
    pass

class NoVoiceChannel(commands.CommandError):
    pass

class QueueIsEmpty(commands.CommandError):
    pass

class NoTracksFound(commands.CommandError):
    pass

class PlayerIsAlreadyPaused(commands.CommandError):
    pass

class InvalidRepeatMode(commands.CommandError):
    pass

class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2




class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    def add(self, *args):
        self._queue.extend(args)

    @property
    def is_empty(self):
        return not self._queue
    
    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]
    
    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty
        
        return self._queue[self.position + 1]
    
    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[: self.position]
    
    @property
    async def lenght(self):
        return len(self._queue)

    @property
    def get_first_track(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[0]
    
    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty
            
        self.position += 1
        
        if self.position < 0:
            return None

        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            
            else:
                return None
        
        return self._queue[self.position]
    
    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[: self.position + 1]
        self._queue.extend(upcoming)
    
    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    
    def empty(self):
        self._queue.clear()


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()
    
    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel
        
        if(channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel
        
        await super().connect(channel.id)
        return channel

    async def teardown(self, ctx):
        try:
            player = ctx.message.guild.voice_client
            await player.disconnect()

        except KeyError:
            pass
    
    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        
        elif len(tracks) == 1:
            self.queue.add(tracks[0])

            embed = Embed(color=discord.Color.blue())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name="🎶MUSIC ADDED TO THE QUEUE",
                            value=f"{tracks[0].title} has been added to the queue.\nAdded by: {ctx.author.mention}")
            
            embed.set_footer(text=f"Timestamp: {time.ctime()}")

            await ctx.send(embed=embed)
        
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)

                embed = Embed(color=discord.Color.blue())
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.add_field(name="🎶MUSIC ADDED TO THE QUEUE",
                                value=f"{tracks[0].title} has been added to the queue.\nAdded by: {ctx.author.mention}")
                
                embed.set_footer(text=f"Timestamp: {time.ctime()}")

                await ctx.send(embed=embed)
            
        if not self.is_playing and self.queue.is_empty:
            await self.start_playback()
    
    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return(
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )
        
        embed = Embed(color=discord.Color.blue(),
                    title="CHOOSE A SONG",
                    description=(
                        "\n".join(
                            f"**{i + 1}.** {t.title} ({t.lenght//6000}:{str(t.lenght%60).zfill(2)})"
                            for i, t in enumerate(tracks[:5])
                        )
                    ))
        embed.set_footer(text=f"Invoked by {ctx.author.mention}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)

        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)
        
        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60, check=_check)
        
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]
        
    async def start_playback(self):
        await self.play(self.queue.current_track)
    
    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        
        except QueueIsEmpty:
            pass
    
    async def repeat_track(self):
        await self.play(self.queue.current_track)
        

class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.bot.get_player(member.guild).teardown()
    
    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f"Wavelink node {node.identifier} ready")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        
        else:
            await payload.player.advance()
    
    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            embed = Embed(color=discord.Color.blue())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name="🎶MUSIC COMMAND",
                            value=f"We're sorry {ctx.author.mention} but music command aren't avaible in DMs.")
            
            await ctx.send(embed=embed)
            return False
        
        return True
    
    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "127.0.0.8",
                "port": 64609,
                "rest_uri": "https://127.0.0.8:64609",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "europe"
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)
    
    @commands.command(name="connect", aliases=["join"])
    async def connect_command(self, ctx, *, channel : t.Optional[discord.VoiceChannel]):
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        
        embed = Embed(color=discord.Color.blue())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="🎶MUSIC COMMAND",
                        value=f"True connected to the channel ({channel.name})")
        
        await ctx.send(embed=embed)
    
    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            embed = Embed(color=discord.Color.red())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name="❗MUSIC COMMAND ERROR",
                            value=f"True already connected to a vocal channel. Please use the disconnect command and than retry.")
            
            await ctx.send(embed=embed)
        
        elif isinstance(exc, NoVoiceChannel):
            embed = Embed(color=discord.Color.red())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name="❗MUSIC COMMAND ERROR",
                            value=f"You have to be connected to a voice channel before you can use this command.")
            
            await ctx.send(embed=embed)
    
    @commands.command(name="disconnect", aliases=["leave"])
    async def disconnect_command(self, ctx):
        player = self.get_player(ctx)
        await player.disconnect()
        embed = Embed(color=discord.Color.blue())
        embed.add_field(name="❗MUSIC COMMAND",
                        value=f"True disconnected to the channel.")
        embed.set_thumbnail(url=ctx.author.avatar_url)
            
        await ctx.send(embed=embed)

    @commands.command(name="play")
    async def play_command(self, ctx, *, querey : t.Optional[str]):
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)

        if querey is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)

            embed = Embed(color=discord.Color.blue())
            embed.add_field(name="PLAYBACK RESUMED",
                            value=f"The playback has been resumed by {ctx.author.mention}")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

        else:
            querey = querey.strip("<>")
            if not re.match(URL_REGEX, querey):
                querey = f"ytsearch: {querey}"
            
            await player.add_track(ctx, await self.wavelink.get_tracks(querey))
    
    @play_command.error
    async def play_command_error(self, ctx, exc):  
        if isinstance(exc, QueueIsEmpty):
            embed = Embed(color=discord.Color.red())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}", icon_url=ctx.author.avatar_url)
            embed.add_field(name="QUEUE IS EMPTY",
                            value=f"{ctx.author.mention} the queue is empty. There are no songs to play.")
            
            await ctx.send(embed=embed)
        
        elif isinstance(exc, NoVoiceChannel):
            embed = Embed(color=discord.Color.red())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}", icon_url=ctx.author.avatar_url)
            embed.add_field(name="NO VOICE CHANNEL",
                            value=f"{ctx.author.mention} you've to connect to a voice channel before start playing music.")
            
            await ctx.send(embed=embed)
    
    @commands.command(name="shuffle")
    async def shuffle_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.shuffle()

        embed = Embed(color=discord.Color.red())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=f"Timestamp: {time.ctime()}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="QUEUE SHUFFLED",
                        value=f"The queue has been shuffled by {ctx.author.mention}")
            
        await ctx.send(embed=embed)
    
    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            embed = Embed(color=discord.Color.red())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=f"Timestamp: {time.ctime()}", icon_url=ctx.author.avatar_url)
            embed.add_field(name="QUEUE IS EMPTY",
                                value=f"{ctx.author.mention} the queue is empty. There are no songs to shuffle.")
                
            await ctx.send(embed=embed)
    
    @commands.command(name="repeat")
    async def repeat_command(self, ctx, mode : str):
        if mode not in ("none", "1", "all"):
            raise InvalidRepeatMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)

        embed = Embed(color=discord.Color.blue())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=f"Timestamp: {time.ctime()}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="REPEAT MODE",
                        value=f"The repeat mode has been set to **{mode}** by **{ctx.author.mention}**")
                
        await ctx.send(embed=embed)
        
    @commands.command(name="pause")
    async def pause_command(self, ctx):
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        
        embed = Embed(color=discord.Color.blue())
        embed.add_field(name="PLAYER PAUSED",
                        value=f"Playback paused by {ctx.author.mention}")
        
        await ctx.send(embed=embed)

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            embed = Embed(color=discord.Color.red())
            embed.add_field(name="PLAYBACK ALREADY PAUSED",
                            value=f"{ctx.author.mention} the playback has been already paused.")
    
    @commands.command(name="stop")
    async def stop_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()

        embed = Embed(color=discord.Color.blue())
        embed.add_field(name="PLAYBACK STOPPED",
                        value=f"The playback has been stopped by {ctx.author.mention}")
        embed.set_footer(text=f"Timestamp: {time.ctime()}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
    
    @commands.command(name="queue")
    async def queue_command(self, ctx, show : t.Optional[int] = 10):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = Embed(title="Querey Result",
                        color=discord.Color.blue,
                        description=f"Showing up to the next {show} tracks")
        embed.set_author(name="Querey Result")
        embed.set_footer(text=f"Timestamp: {time.ctime()}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Currently play",
                        value=player.queue.current_track.title)
        
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Next Up",
                value="\n".join(t.title for t in upcoming)
            )
            
        await ctx.send(embed=embed)

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            embed = Embed(color=discord.Color.blue())
            embed.add_field(name="QUEUE IS EMPTY",
                            value=f"{ctx.author.mention} the queue is currently empty. Please add a song to the queue")

def setup(bot):
    bot.add_cog(Music(bot))