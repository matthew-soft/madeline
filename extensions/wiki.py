import datetime

import requests
from naff import Embed, Extension, OptionTypes, slash_command, slash_option
from naff.ext.paginators import Paginator


class wiki(Extension):
    @slash_command("samp-wiki", description="Returns an article from open.mp wiki.")
    @slash_option(
        name="query",
        description="The wiki term to search",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def wiki(self, ctx, *, query: str):
        data = requests.get(
            "https://api.open.mp/docs/search", params=dict(q=query)
        ).json()

        try:
            embeds = []
            openmp_url = "https://open.mp/"
            for page_data in data["hits"]:

                docs_title = page_data["title"]
                url = page_data["url"]
                docs_description = page_data["desc"]

                if len(docs_title) > 256:
                    docs_title = "{}...".format(docs_title[:253])
                if len(docs_description) > 2048:
                    docs_description = "{}...".format(docs_description[:2045])

                embed = Embed()
                embed.title = f"Documentation Search Results: {query}"
                embed.add_field(name=docs_title, value=docs_description, inline=False)
                embed.add_field(
                    name="Documentation URL:", value=f"{openmp_url}{url}", inline=True
                )
                embed.set_footer(
                    text=f"Requested by {ctx.author} • Powered by open.mp API 😉",
                    icon_url=ctx.author.avatar.url,
                )
                embed.timestamp = datetime.datetime.utcnow()

                embeds.append(embed)

            if embeds is not None and len(embeds) > 0:

                paginators = Paginator(
                    client=self.bot,
                    pages=embeds,
                    timeout_interval=30,
                    show_select_menu=False,
                )
                await paginators.send(ctx)

        except:
            embed = Embed(
                title=f"No results: {query}",
                description="There were no results for that query.",
            )  # Create embed
            embed.set_footer(
                text=f"Requested by {ctx.author} • Powered by open.mp API 😉",
                icon_url=ctx.author.avatar.url,
            )
            embed.timestamp = datetime.datetime.utcnow()
            return await ctx.send(embed=embed)  # Send the embed


def setup(bot):
    # This is called by dis-snek so it knows how to load the Extension
    wiki(bot)
