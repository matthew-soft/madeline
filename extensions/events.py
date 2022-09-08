import datetime
import os

import aiohttp
from dotenv import load_dotenv
from naff import (
    Activity,
    ActivityType,
    Embed,
    Extension,
    IntervalTrigger,
    Status,
    Task,
    listen,
)
from naff.api.events.discord import GuildJoin, GuildLeft

from core.base import CustomClient
from utilities.events import *

load_dotenv()


class events(Extension):
    bot: CustomClient

    @listen()
    async def on_guild_join(self, event: GuildJoin):
        if self.bot.is_ready:
            guild = event.guild
            e = Embed(color=0x53DDA4, title="Joined a Guild")
            await send_guild_stats(self, e, guild, 997921447701921953)

    @listen()
    async def on_guild_left(self, event: GuildLeft):
        guild = event.guild
        e = Embed(color=0x53DDA4, title="Left a Guild")
        await send_guild_stats(self, e, guild, 997921473861799976)

    @Task.create(IntervalTrigger(seconds=30))
    async def presence_changes(self):
        await self.bot.change_presence(
            status=Status.ONLINE,
            activity=Activity(
                name=f"{len(self.bot.guilds)} servers | /help",
                type=ActivityType.COMPETING,
            ),
        )

    @listen()
    async def on_startup(self):
        """Gets triggered on startup"""

        self.presence_changes.start()

    @Task.create(IntervalTrigger(minutes=30))
    async def upload_stats(self):
        payload = {
            "server_count": len(self.bot.guilds),
        }
        headers = {
            "Authorization": str(os.getenv("TOPGG_TOKEN")),
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            await session.post(
                f"https://top.gg/api/bots/{self.bot.user.id}/stats",
                json=payload,
                headers=headers,
            )


def setup(bot: CustomClient):
    """Let naff load the extension"""

    events(bot)
