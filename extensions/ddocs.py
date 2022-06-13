import datetime

from algoliasearch.search_client import SearchClient
from naff import Embed, Extension, OptionTypes, slash_command, slash_option


class ddocs(Extension):
    def __init__(self, ctx):
        ## Fill out from trying a search on the ddevs portal
        app_id = "BH4D9OD16A"
        api_key = "f37d91bd900bbb124c8210cca9efcc01"
        self.search_client = SearchClient.create(app_id, api_key)
        self.index = self.search_client.init_index("discord")

    @slash_command(
        "ddocs", description="Scours the discord api documentations for help"
    )
    @slash_option(
        name="search_term",
        description="Name of the plugin to get the commands for",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def ddocs(self, ctx, *, search_term):

        results = await self.index.search_async(search_term)
        description = ""
        hits = []
        for hit in results["hits"]:
            title = self.get_level_str(hit["hierarchy"])
            if title in hits:
                continue
            hits.append(title)
            url = hit["url"].replace(
                "https://discord.com/developers/docs", "https://discord.dev"
            )
            description += f"[{title}]({url})\n"
            if len(hits) == 10:
                break
        embed = Embed(
            title="Your help has arrived!",
            description=description,
            color=0x7289DA,
        )
        embed.set_footer(
            text=f"Requested by {ctx.author} | Powered by Algolia DocSearch",
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
    # This is called by dis-snek so it knows how to load the Extensions
    ddocs(bot)
