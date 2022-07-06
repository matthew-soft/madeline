import asyncio
import datetime
import functools
import logging
import os
import traceback
from collections import Counter

import psutil
from naff import (
    Activity,
    ActivityType,
    Embed,
    Extension,
    InteractionContext,
    IntervalTrigger,
    OptionTypes,
    Status,
    Task,
    listen,
    slash_command,
    slash_option,
)
from naff.api.events.discord import GuildJoin, GuildLeft

from core.base import CustomClient


class stats(Extension):
    bot: CustomClient

    def __init__(self, bot):
        self.process = psutil.Process()

    def get_bot_uptime(self, *, brief=False):
        now = datetime.datetime.utcnow()
        delta = now - self.bot.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = "{d} days, {h} hours, {m} minutes, and {s} seconds"
            else:
                fmt = "{h} hours, {m} minutes, and {s} seconds"
        else:
            fmt = "{h}h {m}m {s}s"
            if days:
                fmt = "{d}d " + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    @slash_command(name="uptime", description="Get the bot uptime")
    async def uptime(self, ctx: InteractionContext):
        """Tells you how long the bot has been up for."""
        em = Embed(
            title="Local time",
            description=str(datetime.datetime.utcnow())[:-7],
            color=0x14E818,
        )
        em.set_author(name=self.bot.user.username, icon_url=self.bot.user.avatar.url)
        em.add_field(
            name="Current uptime", value=self.get_bot_uptime(brief=True), inline=True
        )
        em.add_field(
            name="Start time", value=str(self.bot.start_time)[:-7], inline=True
        )
        await ctx.send(embed=em)

    @slash_command(name="about", description="About me!")
    async def meee(self, ctx: InteractionContext):
        embed = Embed(description="Madeline v2 | Rewrite")
        embed.title = "About:"
        embed.color = 0x738BD7

        owner = self.bot.get_user(self.bot.owner.id)

        embed.set_author(name=str(owner), icon_url=owner.avatar.url)

        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
        embed.add_field(
            name="Process", value=f"{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU"
        )

        embed.add_field(name="Guilds", value=len(self.bot.guilds))
        embed.add_field(name="Uptime", value=self.get_bot_uptime(brief=True))
        embed.set_footer(
            text="Made with 💖 with NAFF", icon_url="http://i.imgur.com/5BFecvA.png"
        )
        await ctx.send(embed=embed)

    @slash_command("ping", description="Check the bot's latency")
    async def ping(self, ctx: InteractionContext):
        results = Embed(
            color=0x0083F5,
            title="🏓 Pong!",
            description=(f"🌐 WebSocket latency: {self.bot.latency * 1000:.2f}ms\n"),
        )
        results.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        results.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=results)

    async def send_guild_stats(self, e, guild):
        owner = await self.bot.fetch_user(guild._owner_id)
        e.add_field(name="Name", value=guild.name)
        e.add_field(name="ID", value=guild.id)
        e.add_field(name="Owner", value=f"{owner.mention} (ID: {owner.id})")

        total = guild.member_count
        e.add_field(name="Members", value=str(total))

        if guild.icon:
            e.set_thumbnail(url=guild.icon.url)

        if guild.me:
            e.timestamp = guild.me.joined_at

        ch = self.bot.get_channel(993972357414785076)
        await ch.send(embed=e)

    @listen()
    async def on_guild_join(self, event: GuildJoin):
        if self.bot.is_ready:
            guild = event.guild
            e = Embed(color=0x53DDA4, title="New Guild")
            await self.send_guild_stats(e, guild)

    @listen()
    async def on_guild_left(self, event: GuildLeft):
        guild = event.guild
        e = Embed(color=0x53DDA4, title="Left Guild")
        await self.send_guild_stats(e, guild)

    @Task.create(IntervalTrigger(seconds=30))
    async def presence_changes(self):
        await self.bot.change_presence(
            status=Status.AFK,
            activity=Activity(
                name=f"{len(self.bot.guilds)} servers | /help",
                type=ActivityType.COMPETING,
            ),
        )

    @listen()
    async def on_startup(self):
        """Gets triggered on startup"""

        self.presence_changes.start()


def setup(bot: CustomClient):
    """Let naff load the extension"""

    stats(bot)
