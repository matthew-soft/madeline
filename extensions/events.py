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

    def __init__(self, *args, **kwargs):
        self.top_gg_token = os.getenv("TOPGG_TOKEN")

        if self.top_gg_token:
            self.upload_stats.start()
        else:
            log.warning("No top.gg token provided, not posting to top.gg")


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
        if self.top_gg_token:
            await self.bot.wait_until_ready()

            async with aiohttp.ClientSession(headers={"Authorization": self.top_gg_token}) as session:
                resp = await session.post(
                    f"https://top.gg/api/bots/{self.bot.app.id}/stats",
                    json={
                        "server_count": len(self.bot.guilds),
                    },
                )
                if resp.status == 200:
                    log.debug("Posted stats to top.gg")
                else:
                    log.warning(f"Failed to post stats to top.gg: {resp.status} {resp.reason}")


def setup(bot: CustomClient):
    """Let naff load the extension"""

    events(bot)
