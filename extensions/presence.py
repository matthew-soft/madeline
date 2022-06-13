from naff import (Activity, ActivityType, Extension, IntervalTrigger, Status,
                  Task, listen)
from naff.api.events import ChannelCreate

from core.base import CustomClient


class presence(Extension):
    bot: CustomClient

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

    presence(bot)
