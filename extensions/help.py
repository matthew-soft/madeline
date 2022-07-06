import datetime

from algoliasearch.search_client import SearchClient
from naff import (
    ActionRow,
    Button,
    ButtonStyles,
    Embed,
    Extension,
    OptionTypes,
    slash_command,
    slash_option,
)


class help(Extension):
    def __init__(self, ctx):
        ## Fill out from trying a search on the madeline docs
        app_id = "BYGLTBMRH0"
        api_key = "ba2ad6b12791eddbc7079344250ed2ce"
        self.search_client = SearchClient.create(app_id, api_key)
        self.index = self.search_client.init_index("docs")

    @slash_command("help", description="Get the list of available commands")
    @slash_option(
        name="search_term",
        description="Name of the plugin to get the commands for",
        required=False,
        opt_type=OptionTypes.STRING,
    )
    async def help(self, ctx, *, search_term=None):
        if search_term is None:
            embed = Embed(
                description=f"Use [<:slash:894692029941039194>`help [command]`] for more info on a command\nor Visit our [Official Documentations](https://madeline.my.id) for more info.",
                color=0x0083F5,
            )
            embed.set_author(
                name="Madeline™, The Discord Bot",
                url="https://discord.gg/mxkvjpknTN",
                icon_url=self.bot.user.avatar.url,
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.add_field(
                name="__Tool Commands__",
                value="`ddocs`, `guild-avatar`, `avatar`, `user-info`, `server-info`, `urban`, `konesyntees`",
                inline=False,
            )
            embed.add_field(
                name="__Cool Kids Club™️ Commands__",
                value="`aesthetics`, `fraktur`, `bold-fraktur`, `fancy`, `bold-fancy`, `double`, `small-caps`, `8ball`, `weather`, `coinflip`, `dice`, `lmgtfy`",
                inline=False,
            )
            embed.add_field(
                name="__SA-MP Related Commands__",
                value="`samp-query`, `samp-wiki`",
                inline=False,
            )
            embed.add_field(
                name="__Tags Commands__",
                value="`tag get`, `tag create`, `tag edit`, `tag delete`, `tags`",
                inline=False,
            )
            embed.add_field(
                name="__Context Menu Commands__",
                value="`Avatar`, `Guild Avatar`, `User Info`",
                inline=False,
            )
            embed.add_field(
                name="__Bot Status Commands__",
                value="`uptime`, `about`, `help`, `ping`",
                inline=False,
            )
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
            )
            embed.timestamp = datetime.datetime.utcnow()
            components: list[ActionRow] = [
                ActionRow(
                    Button(
                        style=ButtonStyles.URL,
                        label="Official Documentations",
                        emoji="🚀",
                        url="https://madeline.my.id",
                    ),
                    Button(
                        style=ButtonStyles.URL,
                        label="Invite me to your server",
                        emoji="🤖",
                        url="https://discord.com/oauth2/authorize?client_id=859991918800011295&permissions=313344&scope=bot%20applications.commands",
                    ),
                    Button(
                        style=ButtonStyles.URL,
                        label="Support Server",
                        emoji="❓",
                        url="https://discord.gg/mxkvjpknTN",
                    ),
                )
            ]
            return await ctx.send(embed=embed, components=components)

        results = await self.index.search_async(search_term)
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
            title=f"Documentation Search Results: {search_term}",
            description=description,
            color=0x7289DA,
        )
        embed.set_footer(
            text=f"Requested by {ctx.author} • Powered by Algolia DocSearch",
            icon_url=ctx.author.avatar.url,
        )
        embed.timestamp = datetime.datetime.utcnow()
        return await ctx.send(embed=embed)

    def get_level_str(self, levels):
        last = ""
        for level in levels.values():
            if level is not None:
                last = level
        return last


def setup(bot):
    # This is called by dis-snek so it knows how to load the Extension
    help(bot)
