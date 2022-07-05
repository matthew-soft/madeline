import asyncio
import datetime
import functools
import logging
import os
import traceback
from collections import Counter

import psutil
from naff import (
    Embed,
    Extension,
    InteractionContext,
    OptionTypes,
    slash_command,
    slash_option,
)

from core.base import CustomClient


class stats(Extension):
    bot: CustomClient

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


def setup(bot: CustomClient):
    """Let naff load the extension"""

    stats(bot)
