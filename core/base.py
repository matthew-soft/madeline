import datetime
import logging
import os
from time import time

import sentry_sdk
from dotenv import load_dotenv
from naff import (
    Activity,
    ActivityType,
    Client,
    Embed,
    InteractionContext,
    IntervalTrigger,
    Status,
    Task,
    listen,
    logger_name,
)
from naff.api.events.discord import GuildJoin, GuildLeft
from naff.client.errors import CommandCheckFailure, CommandOnCooldown, HTTPException
from pymongo import MongoClient

from src.utilities.events import *

load_dotenv()

start_time = time()

cluster = MongoClient(os.getenv("MONGODB_URL"))

context = cluster["madeline"]["context"]
error_logs = cluster["madeline"]["error"]


def __init__(self, *args, **kwargs):
    self.top_gg_token = os.getenv("TOPGG_TOKEN")

    if self.top_gg_token:
        self.upload_stats.start()
    else:
        log.warning("No top.gg token provided, not posting to top.gg")


class CustomClient(Client):
    """Subclass of naff.Client with our own customized methods"""

    # you can use that logger in all your extensions
    logger = logging.getLogger(logger_name)

    # sentry sdk init
    sentry_sdk.init(
        os.getenv("SENTRY_DSN"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )

    async def on_command_error(self, ctx, error):
        """Gets triggered on a command error"""
        if isinstance(error, CommandCheckFailure):
            if isinstance(ctx, InteractionContext):
                symbol = "/"

            await ctx.send(
                embeds=Embed(
                    description="<:cross:839158779815657512> I'm afraid, I can't let you use that!",
                    color=0xFF0000,
                ),
                ephemeral=True,
            )
            self.logger.warning(
                f"Check failed on Command: [{symbol}{ctx.invoke_target}]"
            )

        elif isinstance(error, CommandOnCooldown):
            if isinstance(ctx, InteractionContext):
                symbol = "/"

            await ctx.send(
                embeds=Embed(
                    description=f"<:cross:839158779815657512> Cooldown is active for this command. You'll be able to use it in {int(error.cooldown.get_cooldown_time())} seconds!",
                    color=0xFF0000,
                ),
                ephemeral=True,
            )
            self.logger.warning(
                f"Command Ratelimited for {int(error.cooldown.get_cooldown_time())} seconds on: [{symbol}{ctx.invoke_target}]"
            )

        elif isinstance(error, HTTPException):
            if isinstance(ctx, InteractionContext):
                symbol = "/"

                await ctx.send(
                    embeds=Embed(
                        description=f"<:cross:839158779815657512> Something happened while trying to process your request, Please try again later!",
                        color=0xFF0000,
                    ),
                    ephemeral=True,
                )

    async def on_command(self, ctx):
        """Gets triggered on a command"""
        if isinstance(ctx, InteractionContext):
            symbol = "/"

        errs = {
            "time": datetime.datetime.utcnow(),
            "guild_id": ctx.guild_id,
            "author_id": ctx.author.id,
            "cmd_name": f"{symbol}{ctx.invoke_target}",
            "cmd_args": f"{ctx.args}",
            "cmd_kwargs": f"{ctx.kwargs}",
        }
        context.insert_one(errs)

        self.logger.info(
            f"Command: [{symbol}{ctx.invoke_target}] was executed with {ctx.args = } | {ctx.kwargs = }"
        )

    @listen()
    async def on_startup(self):
        """Gets triggered on startup"""
        self.status_change.start()
        self.logger.warn(f"Logged in as {self.user}")
        self.logger.warn(f"Total Shards: {self.total_shards}")
        self.logger.warn(f"Ready within: {round((time() - start_time), 2)} seconds")
        self.logger.info(f"{os.getenv('PROJECT_NAME')} - Startup Finished!")
        self.logger.info(
            "Note: Discord needs up to an hour to load global commands / context menus. They may not appear immediately\n"
        )

    # i'll deal with this later
    # @listen()
    # async def on_guild_join(self, event: GuildJoin):
    #     if self.is_ready:
    #         guild = event.guild

    @listen()
    async def on_guild_left(self, event: GuildLeft):
        guild = event.guild
        e = Embed(color=0x53DDA4, title="Left a Guild")
        await send_guild_stats(self, e, guild, 997921473861799976)

    @Task.create(IntervalTrigger(seconds=30))
    async def status_change(self):
        await self.change_presence(
            Status.ONLINE, get_random_presence(len(self.guilds), self.total_shards)
        )

    @Task.create(IntervalTrigger(minutes=30))
    async def upload_stats(self):
        if self.top_gg_token:
            await self.wait_until_ready()

            async with aiohttp.ClientSession(
                headers={"Authorization": self.top_gg_token}
            ) as session:
                resp = await session.post(
                    f"https://top.gg/api/bots/{self.app.id}/stats",
                    json={
                        "server_count": len(self.guilds),
                    },
                )
                if resp.status == 200:
                    log.debug("Posted stats to top.gg")
                else:
                    log.warning(
                        f"Failed to post stats to top.gg: {resp.status} {resp.reason}"
                    )
