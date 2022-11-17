import datetime
import os
import subprocess
from functools import cached_property

import naff
import psutil
from dotenv import load_dotenv
from naff import (
    Embed,
    Extension,
    InteractionContext,
    OptionTypes,
    slash_command,
    slash_option,
)
from naff.ext.paginators import Paginator

from core.base import CustomClient
from src.help import *
from src.utilities import *

load_dotenv()


class help(Extension):
    bot: CustomClient

    def __init__(self, bot):
        self.top_gg_token = os.getenv("TOPGG_TOKEN")
        self.process = psutil.Process()

    @cached_property
    def madeline_commit(self) -> str:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("ascii")
            .strip()
        )

    @slash_command(name="help", description="Get the list of available commands")
    async def help(self, ctx: InteractionContext):
        owner = self.bot.get_user(self.bot.owner.id)
        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()

        embed = Embed(
            title="Main Help Page",
            description=f"A Multifunctional SA-MP Discord Bot written in NAFF (python).\n\nFYI: The bot is absolutely free to use, you don't have to pay anything.\nHowever, to keep the host online 24/7/365, We need sponsors.\nYou can help us by [__**Sponsoring us**__](https://github.com/sponsors/madeline-bot), so we can keep the bot up and running, _forever._\n\n__**Useful Links**__\n[Official Documentations](https://www.madeline.my.id) | [Support Server](https://discord.gg/mxkvjpknTN) | [Invite me to your server](https://discord.com/oauth2/authorize?client_id=859991918800011295&permissions=313344&scope=bot%20applications.commands)",
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
            name="NAFF version",
            value=f"{naff.const.__version__}",
            inline=True,
        )
        embed.add_field(
            name="Last Commit",
            value=f"[{self.madeline_commit}](https://github.com/madeline-bot/madeline/commit/{self.madeline_commit})",
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
            name="Uptime", value=get_bot_uptime(self, brief=True), inline=True
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
            name="</ckc fonts uwu:996967239976747170>",
            value=f"UwUfy your messages.",
            inline=False,
        )
        ckc.add_field(
            name="</ckc fonts aesthetics:996967239976747170>",
            value=f"Returns your text as fullwidth.",
            inline=False,
        )
        ckc.add_field(
            name="</ckc fonts bold-fancy:996967239976747170>",
            value=f"Returns your text as bold cursive.",
            inline=False,
        )
        ckc.add_field(
            name="</ckc fonts bold-fraktur:996967239976747170>",
            value=f"Returns your text as bold blackletter.",
            inline=False,
        )
        ckc.add_field(
            name="</ckc fonts double:996967239976747170>",
            value=f"The example would return '𝕎𝕠𝕒𝕙, 𝕕𝕠𝕦𝕓𝕝𝕖 𝕤𝕥𝕣𝕦𝕔𝕜 𝕥𝕖𝕩𝕥'",
            inline=False,
        )
        ckc.add_field(
            name="</ckc fonts fancy:996967239976747170>",
            value=f"Returns your text as cursive.",
            inline=False,
        )
        ckc.add_field(
            name="</ckc fonts fraktur:996967239976747170>",
            value=f"Returns your text as blackletter.",
            inline=False,
        )
        ckc.add_field(
            name="</ckc fonts small-caps:996967239976747170>",
            value=f"Returns your text as smallcaps.",
            inline=False,
        )
        ckc.add_field(
            name="</ckc fun 8ball:996967239976747170>",
            value=f"It's like any other 8ball command on discord. Annoying, useless and unreasonably popular.",
            inline=False,
        )
        ckc.add_field(
            name="</ckc fun dice:996967239976747170>",
            value=f"Roll a dice",
            inline=False,
        )
        ckc.add_field(
            name="</ckc fun coinflip:996967239976747170>",
            value=f"Flips a coin",
            inline=False,
        )
        ckc.add_field(
            name="</ckc fun lmgtfy:996967239976747170>",
            value=f"Returns you a LMGTFY link. Good to counter people who lazy enough to open up Google in their browser :3",
            inline=False,
        )
        ckc.add_field(
            name="</ckc image ocr:996967239976747170>",
            value=f"Read text inside of an image (Optical Character Recognition)",
            inline=False,
        )

        samp = Embed(
            title="SA-MP Commands",
            description=f"The main features of this bot.",
            color=0x738BD7,
        )
        samp.add_field(
            name="</samp wiki:996967239976747169>",
            value=f"Returns an article from open.mp wiki",
            inline=False,
        )
        samp.add_field(
            name="</samp query:996967239976747169>",
            value=f"Query your favorite SA-MP server",
            inline=False,
        )
        samp.add_field(
            name="</samp bookmark add:996967239976747169>",
            value=f"Add your server to the bookmark",
            inline=False,
        )
        samp.add_field(
            name="</samp bookmark edit:996967239976747169>",
            value=f"Edit your SA-MP server's bookmark",
            inline=False,
        )
        samp.add_field(
            name="</samp bookmark remove:996967239976747169>",
            value=f"Remove your server's bookmark",
            inline=False,
        )

        tools = Embed(
            title="Tools Commands",
            description=f"Some tools that can be used to make your life easier.",
            color=0x738BD7,
        )
        tools.add_field(
            name="</tools ping:997202321945669673>",
            value=f"Check the bot's latency",
            inline=False,
        )
        tools.add_field(
            name="</tools server info:997202321945669673>",
            value=f"Get information about the server",
            inline=False,
        )
        tools.add_field(
            name="</tools user avatar:997202321945669673>",
            value=f"See your/other member avatar",
            inline=False,
        )
        tools.add_field(
            name="</tools user guild-avatar:997202321945669673>",
            value=f"See your/other member guild avatar",
            inline=False,
        )
        tools.add_field(
            name="</tools user info:997202321945669673>",
            value=f"Get information about a member",
            inline=False,
        )
        tools.add_field(
            name="</tools wikipedia:997202321945669673>",
            value=f"Search for a term on the Wikipedia",
            inline=False,
        )
        tools.add_field(
            name="</tools urban:997202321945669673>",
            value=f"Search for a term on the Urban Dictionary",
            inline=False,
        )
        tools.add_field(
            name="</tools weather:997202321945669673>",
            value=f"Get the weather for a city",
            inline=False,
        )
        tools.add_field(
            name="</tools konesyntees:997202321945669673>",
            value=f"Use superior Estonian technology to express your feelings like you've never before!",
            inline=False,
        )

        embeds = [embed, ckc, samp, tools]

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

    @slash_command("vote", description="Vote for the bot on top.gg")
    async def top_gg_vote(self, ctx: InteractionContext):
        if self.top_gg_token:
            await ctx.send(
                "Thanks for voting! You won't get anything, but it helps the bot grow!\n\nhttps://top.gg/bot/{}/vote".format(
                    self.bot.app.id
                )
            )
        else:
            await ctx.send("Voting has been temporarily disabled", ephemeral=True)
