import datetime

import psutil
from algoliasearch.search_client import SearchClient
from naff import Embed, Extension, InteractionContext, slash_command, slash_option

from core.base import CustomClient
from utilities.uptime import *


class help(Extension):
    bot: CustomClient

    def __init__(self, bot):
        self.process = psutil.Process()
        ## Fill out from trying a search on the docs
        app_id = "BYGLTBMRH0"
        api_key = "ba2ad6b12791eddbc7079344250ed2ce"
        self.search_client = SearchClient.create(app_id, api_key)
        self.index = self.search_client.init_index("docs")

    @slash_command(name="help", description="Get the list of available commands")
    @slash_option(
        name="plugin_name",
        description="Name of the plugin to get the commands for",
        required=False,
        opt_type=OptionTypes.STRING,
    )
    async def help(self, ctx: InteractionContext, plugin_name=None):
        if plugin_name is None:
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
                name="Uptime", value=get_bot_uptime(self, brief=True), inline=True
            )
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
            )
            embed.timestamp = datetime.datetime.utcnow()

            return await ctx.send(embed=embed)

        results = await self.index.search_async(plugin_name)
        description = ""
        hits = []
        for hit in results["hits"]:
            title = self.get_level_str(hit["hierarchy"])
            if title in hits:
                continue
            hits.append(title)
            url = hit["url"]
            description += f"[{title}]({url})\n"
            if len(hits) == 10:
                break
        embed = Embed(
            title="Your help has arrived!",
            description=description,
            color=0x7289DA,
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        embed.timestamp = datetime.datetime.utcnow()
        return await ctx.send(embed=embed)


def setup(bot: CustomClient):
    """Let naff load the extension"""

    help(bot)
