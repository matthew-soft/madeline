import datetime

# import cloudscraper
import requests
from naff import Embed, Extension, OptionTypes, slash_command, slash_option

# scraper = cloudscraper.create_scraper()


class wiki(Extension):
    @slash_command("wiki", description="Returns an article from open.mp wiki.")
    @slash_option(
        name="query",
        description="The wiki term to search",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def wiki(self, ctx, *, query):
        openmp_url = "https://open.mp/"
        # r = scraper.get(f"https://api.open.mp/docs/search?q={query}").json()
        r = requests.get(f"https://api.open.mp/docs/search?q={query}").json()
        try:
            if r["hits"]:
                title = r["hits"][0]["title"]
                desc = r["hits"][0]["desc"]
                url = r["hits"][0]["url"]
                embed = Embed(
                    title=f"Documentation Search Results: {query}",
                    description=f"[`{title}`]({openmp_url}{url}): {desc}",
                )  # Create embed
                embed.set_footer(
                    text=f"Requested by {ctx.author} • Powered by open.mp API 😉",
                    icon_url=ctx.author.avatar.url,
                )
                embed.timestamp = datetime.datetime.utcnow()
                return await ctx.send(embed=embed)  # Send the embed
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
