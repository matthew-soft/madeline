from samp_client.client import SampClient
import cloudscraper
import datetime
from naff import (
    Embed,
)

scraper = cloudscraper.create_scraper()

def query(ctx, ip: str, port: int):
    try:
        with SampClient(address=ip, port=port) as kung:
            info = kung.get_server_info()
            players = kung.get_server_clients_detailed()
            numpang = kung.get_server_clients()
            rule = kung.get_server_rules()

            pleyers = []
            for ppq in numpang:
                pleyers.append(f"{ppq.name}                    | {ppq.score}")

        general = Embed(title=info.hostname, color=0x0083F5)  # Create embed
        general.add_field(name="IP", value=f"`{ip}:{port}`", inline=True)
        general.add_field(
            name="Players : ",
            value=f"`{info.players}` / `{info.max_players}` Players",
            inline=True,
        )
        general.add_field(
            name="Gamemode : ", value=f"`{info.gamemode}`", inline=True
        )
        general.add_field(
            name="Language : ", value=f"`{info.language}`", inline=True
        )
        general.add_field(
            name="Passworded? : ", value=f"`{info.password}`", inline=True
        )
        if info.players == 0:
            general.add_field(
                name="[only show 10 player max] Connected Clients :",
                value="No players connected",
                inline=False,
            )
        if info.players > 0:
            listed = "\n".join(pleyers)
            if pleyers == []:
                general.add_field(
                    name="Note:",
                    value="due to __*discord limitations*__, i can't show connected clients summary 😔",
                    inline=False,
                )
            else:
                general.add_field(
                    name="[only show 10 player max] Connected Clients :",
                    value=f"```==============================================\nName                        | Score\n ==============================================\n {listed}```",
                    inline=False,
                )
        general.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        general.timestamp = datetime.datetime.utcnow()

        srv_info = Embed(title=info.hostname, color=0x0083F5)  # Create embed
        srv_info.add_field(name="IP", value=f"`{ip}:{port}`", inline=False)
        srv_info.add_field(name="Gamemode", value=info.gamemode, inline=False)
        srv_info.add_field(name="Language", value=info.language, inline=False)
        if info.password is True:
            srv_info.add_field(name="Passworded?", value="Yes", inline=False)
        for i in rule:
            srv_info.add_field(name=i.name, value=i.value, inline=True)
        srv_info.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        srv_info.timestamp = datetime.datetime.utcnow()

        if info.players == 0:
            p_info = Embed(
                description=f"<:cross:839158779815657512> No players connected",
                color=0xFF0000,
            )  # Create embed
            p_info.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url,
            )
            p_info.timestamp = datetime.datetime.utcnow()
        else:
            if info.players > 10:
                p_info = Embed(
                    title=info.hostname,
                    description="Note: due to __*discord limitations*__, i can't show detailed connected clients 😔",
                    color=0xF6ADAB,
                )  # Create embed
                p_info.add_field(
                    name="Players : ",
                    value=f"`{info.players}` / `{info.max_players}` Players",
                    inline=True,
                )
                p_info.set_footer(
                    text=f"Requested by {ctx.author}",
                    icon_url=ctx.author.avatar.url,
                )
                p_info.timestamp = datetime.datetime.utcnow()
            else:
                p_info = Embed(title=info.hostname, color=0x4C8404)  # Create embed
                p_info.add_field(
                    name="Players : ",
                    value=f"`{info.players}` / `{info.max_players}` Players",
                    inline=True,
                )
                if info.players > 0:
                    if pleyers != []:
                        listed = "\n".join(pleyers)
                        p_info.add_field(
                            name="[only show 10 player max] Connected Clients :",
                            value=f"```==============================================\nName                        | Score\n ==============================================\n {listed}```",
                            inline=False,
                        )
                p_info.set_footer(
                    text=f"Requested by {ctx.author}",
                    icon_url=ctx.author.avatar.url,
                )
                p_info.timestamp = datetime.datetime.utcnow()
        embeds = [general, srv_info, p_info]
        return embeds
    except:
        return None

def wiki(ctx, query: str):
    data = scraper.get(
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
        return embeds
    except:
        return None