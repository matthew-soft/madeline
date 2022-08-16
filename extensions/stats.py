import datetime
import os
import aiohttp
from dotenv import load_dotenv

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
from naff.ext.paginators import Paginator

from core.base import CustomClient

load_dotenv()


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

    @slash_command(name="about", description="Learn more about me")
    async def meee(self, ctx: InteractionContext):
        owner = self.bot.get_user(self.bot.owner.id)
        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()

        embed = Embed(
            title="Help Page",
            description=f"__Useful Links__\n[Official Documentations](https://www.madeline.my.id) | [Support Server](https://discord.gg/mxkvjpknTN) | [Invite me to your server](https://discord.com/oauth2/authorize?client_id=859991918800011295&permissions=313344&scope=bot%20applications.commands)",
            color=0x738BD7,
        )
        embed.set_author(
            name="Madeline™, The Discord Bot",
            url="https://discord.gg/mxkvjpknTN",
            icon_url=self.bot.user.avatar.url,
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(
            name="__Tool Commands__",
            value="`tools ddocs`, `tools wikipedia`, `tools user guild-avatar`, `tools user avatar`, `tools user info`, `tools server info`, `tools urban`, `tools konesyntees`, `tools weather`, `tools ping`, `tools speedtest`(<:be:999874963936903228><:ta:999874979439050762>)",
            inline=False,
        )
        embed.add_field(
            name="__Cool Kids Club™️ Commands__",
            value="`ckc fonts uwu`, `ckc fonts aesthetics`, `ckc fonts fraktur`, `ckc fonts bold-fraktur`, `ckc fonts fancy`, `ckc fonts bold-fancy`, `ckc fonts double`, `ckc fonts small-caps`, `ckc fun 8ball`, `ckc fun coinflip`, `ckc fun dice`, `ckc fun lmgtfy`",
            inline=False,
        )
        embed.add_field(
            name="__SA-MP Related Commands__",
            value="`samp query`, `samp wiki`, `samp bookmark add`, `samp bookmark edit`, `samp bookmark remove`",
            inline=False,
        )
        embed.add_field(
            name="__Tags Commands__",
            value="`tag get`, `tag create`, `tag edit`, `tag delete`, `tags`, `tag mod delete`",
            inline=False,
        )
        embed.add_field(
            name="__Context Menu Commands__",
            value="`Avatar`, `Guild Avatar`, `User Info`",
            inline=False,
        )
        embed.add_field(
            name="__Help Commands__",
            value="`about`",
            inline=False,
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        embed.timestamp = datetime.datetime.utcnow()

        about = Embed()
        about.color = 0x738BD7
        about.title = "Stats Page"
        about.description = "A Multifunctional SA-MP Discord Bot written in NAFF (python).\n\nFYI: The bot is absolutely free to use, you don't have to pay anything.\nHowever, to keep the host online 24/7/365, We need sponsors.\nYou can help us by [__**Sponsoring us**__](https://github.com/sponsors/madeline-bot), so we can keep the bot up and running, _forever._"
        about.set_author(
            name="Madeline™, The Discord Bot",
            url="https://discord.gg/mxkvjpknTN",
            icon_url=self.bot.user.avatar.url,
        )
        about.add_field(name="Owner", value=f"{owner.mention}", inline=False)
        about.add_field(name="Guilds", value=len(self.bot.guilds), inline=True)
        about.add_field(
            name="Process",
            value=f"{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU",
            inline=True,
        )
        about.add_field(
            name="Local time",
            value=f"<t:{int(datetime.datetime.utcnow().timestamp())}:F>",
            inline=False,
        )
        about.add_field(
            name="Start time",
            value=f"<t:{int(self.bot.start_time.timestamp())}:F>",
            inline=True,
        )
        about.add_field(
            name="Uptime", value=self.get_bot_uptime(brief=True), inline=True
        )
        about.set_footer(
            text="Made with 💖 with NAFF", icon_url="http://i.imgur.com/5BFecvA.png"
        )

        embeds = [embed, about]

        paginators = Paginator(
            client=self.bot,
            pages=embeds,
            timeout_interval=30,
            show_first_button=False,
            show_back_button=False,
            show_next_button=False,
            show_last_button=False,
            show_callback_button=False,
            show_select_menu=True,
        )
        return await paginators.send(ctx)

    async def send_guild_stats(self, e, guild, r_channel):
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

        ch = self.bot.get_channel(r_channel)
        await ch.send(embed=e)

    @listen()
    async def on_guild_join(self, event: GuildJoin):
        if self.bot.is_ready:
            guild = event.guild
            e = Embed(color=0x53DDA4, title="Joined a Guild")
            await self.send_guild_stats(e, guild, 997921447701921953)

    @listen()
    async def on_guild_left(self, event: GuildLeft):
        guild = event.guild
        e = Embed(color=0x53DDA4, title="Left a Guild")
        await self.send_guild_stats(e, guild, 997921473861799976)

    @Task.create(IntervalTrigger(seconds=30))
    async def presence_changes(self):
        await self.bot.change_presence(
            status=Status.AFK,
            activity=Activity(
                name=f"{len(self.bot.guilds)} servers | /about",
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

    stats(bot)
