import datetime
import os
from typing import Optional

from dotenv import load_dotenv
from naff import (
    AutocompleteContext,
    Buckets,
    Embed,
    Extension,
    OptionTypes,
    Permissions,
    check,
    cooldown,
    slash_command,
    slash_option,
)
from naff.ext.paginators import Paginator
from pymongo import MongoClient

from src.samp import *
from src.utilities import *

load_dotenv()

cluster = MongoClient(os.getenv("MONGODB_URL"))

server = cluster["madeline"]["servers"]


class samp(Extension):
    @slash_command(
        name="samp",
        description="All SA-MP Commands",
        sub_cmd_name="wiki",
        sub_cmd_description="Returns an article from open.mp wiki.",
    )
    @slash_option(
        name="query",
        description="The wiki term to search",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    @cooldown(bucket=Buckets.USER, rate=1, interval=5)
    async def wiki(self, ctx, query: str):
        await ctx.defer()
        embed = wiki(ctx, query)
        if embed is not None:
            return await ctx.send(embed=embed)
        else:
            return await ctx.send(
                embed=wiki_none(ctx, query), ephemeral=True
            )  # Send the embed

    @slash_command(
        name="samp",
        description="All SA-MP Commands",
        sub_cmd_name="query",
        sub_cmd_description="Query your favorite SA-MP server",
    )
    @slash_option(
        "ip_only",
        "Please enter the Server IP WITHOUT Port (only support public ip address or domains!)",
        OptionTypes.STRING,
        required=False,
    )
    @slash_option(
        "port",
        "Please enter Server Port (optional, default port is 7777)",
        OptionTypes.INTEGER,
        required=False,
    )
    @cooldown(bucket=Buckets.USER, rate=1, interval=10)
    async def samp(self, ctx, ip_only=None, port: Optional[int] = 7777):
        # need to defer it, otherwise, it fails
        await ctx.defer()

        if ip_only is None:
            try:
                find = server.find_one({"guild_id": ctx.guild_id})
                ip_only = find["ip"]
                port = find["port"]
            except:
                embed = Embed(
                    description=f"<:cross:839158779815657512> Cannot find server info in database. Please use </samp bookmark add:996967239976747169> to add your server info to bookmark.",
                    color=0xFF0000,
                )
                return await ctx.send(embed=embed, ephemeral=True)
        embeds = query(ctx, ip_only, port)
        if embeds is not None:
            embeds = query(ctx, ip_only, port)
            paginators = Paginator(
                client=self.bot,
                pages=embeds,
                timeout_interval=30,
                show_select_menu=False,
            )
            return await paginators.send(ctx)
        else:
            return await ctx.send(embed=query_none(), ephemeral=True)  # Send the embed

    @slash_command(
        name="samp",
        description="All SA-MP Commands",
        group_name="bookmark",
        group_description="Manage your guild SA-MP server bookmark",
        sub_cmd_name="add",
        sub_cmd_description="Add your server to the bookmark",
    )
    @slash_option(
        "ip_only",
        "Please enter the Server IP WITHOUT Port (only support public ip address or domains!)",
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
    @cooldown(bucket=Buckets.USER, rate=1, interval=2)
    async def add(self, ctx, ip_only: str, port: Optional[int] = 7777):
        # need to defer it, otherwise, it fails
        await ctx.defer()
        find = server.find_one({"guild_id": ctx.guild_id})
        if find is not None:
            embed = Embed(
                description=f"<:cross:839158779815657512> You already have a server in the list!",
                color=0xFF0000,
            )
            return await ctx.send(embed=embed, ephemeral=True)
        else:
            server.insert_one(
                {
                    "guild_id": ctx.guild_id,
                    "ip": ip_only,
                    "port": port,
                    "created_by": ctx.author.id,
                    "created_at": int(datetime.datetime.utcnow().timestamp()),
                    "edited_at": None,
                    "full_ip": f"{ip_only}:{port}",
                }
            )
            embed = Embed(
                description=f"<:check:839158727512293406> Server added to the list!",
                color=0x00FF00,
            )
            return await ctx.send(embed=embed)

    @slash_command(
        name="samp",
        description="All SA-MP Commands",
        group_name="bookmark",
        group_description="Manage your guild SA-MP server bookmark",
        sub_cmd_name="edit",
        sub_cmd_description="Edit your SA-MP server's bookmark",
    )
    @cooldown(bucket=Buckets.USER, rate=1, interval=2)
    @slash_option(
        "ip_only",
        "Please enter the Server IP WITHOUT Port (only support public ip address or domains!)",
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
    async def edit(self, ctx, ip_only: str, port: Optional[int] = 7777):
        # need to defer it, otherwise, it fails
        await ctx.defer()
        find = server.find_one({"guild_id": ctx.guild_id})
        if find is None:
            embed = Embed(
                description=f"<:cross:839158779815657512> Your server is not in our database yet, Please register it first!",
                color=0xFF0000,
            )
            return await ctx.send(embed=embed, ephemeral=True)
        else:
            server.update_one(
                {
                    "guild_id": ctx.guild_id,
                },
                {
                    "$set": {
                        "ip": ip_only,
                        "port": port,
                        "edited_at": int(datetime.datetime.utcnow().timestamp()),
                        "full_ip": f"{ip_only}:{port}",
                    }
                },
            )
            embed = Embed(
                description=f"<:check:839158727512293406> Your server has been updated!",
                color=0x00FF00,
            )
            return await ctx.send(embed=embed)

    @slash_command(
        name="samp",
        description="All SA-MP Commands",
        group_name="bookmark",
        group_description="Manage your guild SA-MP server bookmark",
        sub_cmd_name="remove",
        sub_cmd_description="Remove your server's bookmark",
    )
    @check(member_permissions(Permissions.MANAGE_MESSAGES))
    @cooldown(bucket=Buckets.USER, rate=1, interval=2)
    async def remove(self, ctx):
        # need to defer it, otherwise, it fails
        await ctx.defer()
        find = server.find_one({"guild_id": ctx.guild_id})
        if find is None:
            embed = Embed(
                description=f"<:cross:839158779815657512> Your server is not in our database yet, Please register it first!",
                color=0xFF0000,
            )
            return await ctx.send(embed=embed, ephemeral=True)
        else:
            server.delete_one(
                {
                    "guild_id": ctx.guild_id,
                }
            )
            embed = Embed(
                description=f"<:check:839158727512293406> Your server has been removed from our database!",
                color=0x00FF00,
            )
            return await ctx.send(embed=embed)
