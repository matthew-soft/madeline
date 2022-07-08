import datetime
import os
from typing import Optional

import cloudscraper
from dotenv import load_dotenv
from naff import (
    Embed,
    Extension,
    OptionTypes,
    Permissions,
    SlashCommandChoice,
    check,
    slash_command,
    slash_option,
)
from naff.ext.paginators import Paginator
from pymongo import MongoClient
from samp_client.client import SampClient

from utilities.checks import *

load_dotenv()

cluster = MongoClient(os.getenv("MONGODB_URL"))

server = cluster["madeline"]["servers"]
scraper = cloudscraper.create_scraper()


class samp(Extension):
    @slash_command("samp-wiki", description="Returns an article from open.mp wiki.")
    @slash_option(
        name="query",
        description="The wiki term to search",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def wiki(self, ctx, *, query: str):
        await ctx.defer()
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

    @slash_command(
        "samp-query", description="Show SA-MP server info and basic player information"
    )
    @slash_option(
        "ip",
        "Please enter the Server IP (only support public ip address or domains!)",
        OptionTypes.STRING,
        required=False,
    )
    @slash_option(
        "port",
        "Please enter Server Port (optional, default port is 7777)",
        OptionTypes.INTEGER,
        required=False,
    )
    async def samp(self, ctx, ip=None, port: Optional[int] = 7777):
        # need to defer it, otherwise, it fails
        await ctx.defer()

        if ip is None:
            try:
                find = server.find_one({"guild_id": ctx.guild_id})
                ip = find["ip"]
                port = find["port"]
            except:
                return await ctx.send(
                    "Cannot find server info in database. Please use `/query add` to add your server info to bookmark."
                )

        try:
            with SampClient(address=ip, port=port) as kung:
                info = kung.get_server_info()
                players = kung.get_server_clients_detailed()
                numpang = kung.get_server_clients()

            general = Embed(title=info.hostname, color=0x0083F5)  # Create embed
            general.add_field(name="IP", value=f"`{ip}:{port}`", inline=True)
            general.add_field(
                name="Gamemode : ", value=f"`{info.gamemode}`", inline=True
            )
            general.add_field(
                name="Language : ", value=f"`{info.language}`", inline=True
            )
            general.add_field(
                name="Passworded? : ", value=f"`{info.password}`", inline=True
            )
            general.add_field(
                name="Players : ",
                value=f"`{info.players}` / `{info.max_players}` Players",
                inline=True,
            )
            if info.players == 0:
                general.add_field(
                    name="[only show 10 player max] Connected Clients :",
                    value="No players connected",
                    inline=False,
                )
            if info.players > 0:
                for ppq in numpang:
                    general.add_field(
                        name="[only show 10 player max] Connected Clients :",
                        value=f"```==============================================\nName                        | Score\n ==============================================\n {ppq.name}                    | {ppq.score}```",
                        inline=False,
                    )
            if info.players > 10:
                general.add_field(
                    name="Note:",
                    value="due to __*discord limitations*__, i can't show connected clients summary 😔",
                    inline=False,
                )
            general.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
            )
            general.timestamp = datetime.datetime.utcnow()

            srv_info = Embed(title=info.hostname, color=0x0083F5)  # Create embed
            srv_info.add_field(name="IP", value=f"`{ip}:{port}`", inline=True)
            srv_info.add_field(
                name="Gamemode : ", value=f"`{info.gamemode}`", inline=True
            )
            srv_info.add_field(
                name="Language : ", value=f"`{info.language}`", inline=True
            )
            srv_info.add_field(
                name="Passworded? : ", value=f"`{info.password}`", inline=True
            )
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
                    for ppq in players:
                        p_info.add_field(
                            name="[only show 10 player max] Detailed Connected Clients :",
                            value=f"```==============================================\nID |Name                        | Score | Ping\n ==============================================\n {ppq.id} | {ppq.name}                    | {ppq.score} | {ppq.ping}```",
                            inline=False,
                        )
                    p_info.set_footer(
                        text=f"Requested by {ctx.author}",
                        icon_url=ctx.author.avatar.url,
                    )
                    p_info.timestamp = datetime.datetime.utcnow()
            embeds = [general, srv_info, p_info]

            paginators = Paginator(
                client=self.bot,
                pages=embeds,
                timeout_interval=30,
                show_select_menu=False,
            )
            return await paginators.send(ctx)
        except:
            embed = Embed(
                description=f"<:cross:839158779815657512> Couldn't connect to the server",
                color=0xFF0000,
            )
            return await ctx.send(embed=embed)

    @slash_command(
        name="query",
        sub_cmd_name="add",
        sub_cmd_description="Bookmark your server to the list of servers to query",
    )
    @slash_option(
        "ip",
        "Please enter the Server IP (only support public ip address or domains!)",
        OptionTypes.STRING,
        required=True,
    )
    @slash_option(
        "port",
        "Please enter Server Port (optional, default port is 7777)",
        OptionTypes.INTEGER,
        required=False,
    )
    @check(member_permissions(Permissions.MANAGE_MESSAGES))
    async def add(self, ctx, ip: str, port: Optional[int] = 7777):
        # need to defer it, otherwise, it fails
        await ctx.defer()
        find = server.find_one({"guild_id": ctx.guild_id})
        if find is not None:
            return await ctx.send("You already have a server in the list!")
        else:
            server.insert_one(
                {
                    "guild_id": ctx.guild_id,
                    "ip": ip,
                    "port": port,
                    "created_by": ctx.author.id,
                    "created_at": int(datetime.datetime.utcnow().timestamp()),
                    "edited_at": None,
                }
            )
            return await ctx.send("Server added to the list!")

    @slash_command(
        name="query",
        sub_cmd_name="edit",
        sub_cmd_description="Edit your server's bookmark",
    )
    @slash_option(
        "ip",
        "Please enter the Server IP (only support public ip address or domains!)",
        OptionTypes.STRING,
        required=True,
    )
    @slash_option(
        "port",
        "Please enter Server Port (optional, default port is 7777)",
        OptionTypes.INTEGER,
        required=False,
    )
    @check(member_permissions(Permissions.MANAGE_MESSAGES))
    async def edit(self, ctx, ip: str, port: Optional[int] = 7777):
        # need to defer it, otherwise, it fails
        await ctx.defer()
        find = server.find_one({"guild_id": ctx.guild_id})
        if find is None:
            return await ctx.send(
                "Your server is not in our list, Please register it first!"
            )
        else:
            server.update_one(
                {
                    "guild_id": ctx.guild_id,
                },
                {
                    "$set": {
                        "ip": ip,
                        "port": port,
                        "edited_at": int(datetime.datetime.utcnow().timestamp()),
                    }
                },
            )
            return await ctx.send("Your server has been updated!")

    @slash_command(
        name="query",
        sub_cmd_name="remove",
        sub_cmd_description="Remove your server's bookmark",
    )
    @check(member_permissions(Permissions.MANAGE_MESSAGES))
    async def remove(self, ctx):
        # need to defer it, otherwise, it fails
        await ctx.defer()
        find = server.find_one({"guild_id": ctx.guild_id})
        if find is None:
            return await ctx.send(
                "Your server is not in our list, Please register it first!"
            )
        else:
            server.delete_one(
                {
                    "guild_id": ctx.guild_id,
                }
            )
            return await ctx.send("Your server has been removed from our database!")


def setup(bot):
    # This is called by dis-snek so it knows how to load the Extension
    samp(bot)
