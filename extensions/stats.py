import datetime
import os

import aiohttp
import psutil
from dotenv import load_dotenv
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

    @slash_command(name="help", description="Get the list of available commands")
    async def help(self, ctx: InteractionContext):
        owner = self.bot.get_user(self.bot.owner.id)
        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()

        embed = Embed(
            title="Main Help Page",
            description=f"A Multifunctional SA-MP Discord Bot written in NAFF (python).\n\nFYI: The bot is absolutely free to use, you don't have to pay anything.\nHowever, to keep the host online 24/7/365, We need sponsors.\nYou can help us by [__**Sponsoring us**__](https://github.com/sponsors/madeline-bot), so we can keep the bot up and running, _forever._\n\n__Useful Links__\n[Official Documentations](https://www.madeline.my.id) | [Support Server](https://discord.gg/mxkvjpknTN) | [Invite me to your server](https://discord.com/oauth2/authorize?client_id=859991918800011295&permissions=313344&scope=bot%20applications.commands)",
            color=0x738BD7,
        )
        embed.set_author(
            name="Madeline™, The Discord Bot",
            url="https://discord.gg/mxkvjpknTN",
            icon_url=self.bot.user.avatar.url,
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Owner", value=f"{owner.mention}", inline=False)
        embed.add_field(name="Guilds", value=len(self.bot.guilds), inline=True)
        embed.add_field(
            name="Process",
            value=f"{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU",
            inline=True,
        )
        embed.add_field(
            name="Local time",
            value=f"<t:{int(datetime.datetime.utcnow().timestamp())}:F>",
            inline=False,
        )
        embed.add_field(
            name="Start time",
            value=f"<t:{int(self.bot.start_time.timestamp())}:F>",
            inline=True,
        )
        embed.add_field(
            name="Uptime", value=self.get_bot_uptime(brief=True), inline=True
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        embed.timestamp = datetime.datetime.utcnow()

        ckc = Embed(
            title="Cool Kids Commands™️",
            description=f"Some cool commands to try out 👀",
            color=0x738BD7,
        )
        ckc.add_field(
            name="`/ckc fonts uwu <text>`", value=f"UwUfy your messages.", inline=False
        )
        ckc.add_field(
            name="`/ckc fonts aesthetics <text>`",
            value=f"Returns your text as fullwidth.",
            inline=False,
        )
        ckc.add_field(
            name="`/ckc fonts bold-fancy <text>`",
            value=f"Returns your text as bold cursive.",
            inline=False,
        )
        ckc.add_field(
            name="`/ckc fonts bold-fraktur <text>`",
            value=f"Returns your text as bold blackletter.",
            inline=False,
        )
        ckc.add_field(
            name="`/ckc fonts double <text>`",
            value=f"The example would return '𝕎𝕠𝕒𝕙, 𝕕𝕠𝕦𝕓𝕝𝕖 𝕤𝕥𝕣𝕦𝕔𝕜 𝕥𝕖𝕩𝕥'",
            inline=False,
        )
        ckc.add_field(
            name="`/ckc fonts fancy <text>`",
            value=f"Returns your text as cursive.",
            inline=False,
        )
        ckc.add_field(
            name="`/ckc fonts fraktur <text>`",
            value=f"Returns your text as blackletter.",
            inline=False,
        )
        ckc.add_field(
            name="`/ckc fonts small-caps <text>`",
            value=f"Returns your text as smallcaps.",
            inline=False,
        )
        ckc.add_field(
            name="`/ckc 8ball [question]`",
            value=f"It's like any other 8ball command on discord. Annoying, useless and unreasonably popular.",
            inline=False,
        )
        ckc.add_field(
            name="`/ckc dice [sides] [rolls]`", value=f"Roll a dice", inline=False
        )
        ckc.add_field(name="`/ckc coinflip`", value=f"Flips a coin", inline=False)
        ckc.add_field(
            name="`/ckc lmgtfy <search_terms>`",
            value=f"Returns you a LMGTFY link. Good to counter people who lazy enough to open up Google in their browser :3",
            inline=False,
        )

        samp = Embed(
            title="SA-MP Commands",
            description=f"The main features of this bot.",
            color=0x738BD7,
        )
        samp.add_field(
            name="`/samp wiki <query>`",
            value=f"Returns an article from open.mp wiki",
            inline=False,
        )
        samp.add_field(
            name="`/samp query [ip] [port]`",
            value=f"Query your favorite SA-MP server",
            inline=False,
        )
        samp.add_field(
            name="`/samp bookmark add [ip] [port]`",
            value=f"Add your server to the bookmark",
            inline=False,
        )
        samp.add_field(
            name="`/samp bookmark edit [ip] [port]`",
            value=f"Edit your SA-MP server's bookmark",
            inline=False,
        )
        samp.add_field(
            name="`/samp bookmark remove`",
            value=f"Remove your server's bookmark",
            inline=False,
        )

        tags = Embed(
            title="Tags Commands",
            description=f"Tags are used to store text or attachment or both that can be used later on.",
            color=0x738BD7,
        )
        tags.add_field(
            name="`/tag get <name>`",
            value=f"Get a tag",
            inline=False,
        )
        tags.add_field(
            name="`/tag create <name> [content] [attachment]`",
            value=f"Create a tag",
            inline=False,
        )
        tags.add_field(
            name="`/tag edit <name> [content] [attachment]`",
            value=f"Edit a tag",
            inline=False,
        )
        tags.add_field(
            name="`/tag delete <name>`",
            value=f"Delete a tag",
            inline=False,
        )
        tags.add_field(
            name="`/tag mod delete <name>`",
            value=f"Delete a tag (Requires `MANAGE_MESSAGES` Permissions)",
            inline=False,
        )
        tags.add_field(
            name="`/tags [search]`",
            value=f"Get a list of tags and/or inspect a tag",
            inline=False,
        )

        tools = Embed(
            title="Tools Commands",
            description=f"Some tools that can be used to make your life easier.",
            color=0x738BD7,
        )
        tools.add_field(
            name="`/tools ping`",
            value=f"Check the bot's latency",
            inline=False,
        )
        tools.add_field(
            name="`/tools server info`",
            value=f"Get information about the server",
            inline=False,
        )
        tools.add_field(
            name="`/tools user avatar [member]`",
            value=f"See your/other member avatar",
            inline=False,
        )
        tools.add_field(
            name="`/tools user guild-avatar [member]`",
            value=f"See your/other member guild avatar",
            inline=False,
        )
        tools.add_field(
            name="`/tools user info [member]`",
            value=f"Get information about a member",
            inline=False,
        )
        tools.add_field(
            name="`/tools wikipedia <search_terms> [only_first_result]`",
            value=f"Search for a term on the Wikipedia",
            inline=False,
        )
        tools.add_field(
            name="`/tools ddocs <search_terms>`",
            value=f"Scours the discord api documentations for help",
            inline=False,
        )
        tools.add_field(
            name="`/tools urban <word>`",
            value=f"Search for a term on the Urban Dictionary",
            inline=False,
        )
        tools.add_field(
            name="`/tools weather <city>`",
            value=f"Get the weather for a city",
            inline=False,
        )
        tools.add_field(
            name="`/tools konesyntees <input> [voice] [speed]`",
            value=f"Use superior Estonian technology to express your feelings like you've never before!",
            inline=False,
        )

        embeds = [embed, ckc, samp, tags, tools]

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
