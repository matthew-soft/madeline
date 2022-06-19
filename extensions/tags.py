import asyncio
import math
import os
import re
from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from naff import (
    ActionRow,
    AutocompleteContext,
    Button,
    ButtonStyles,
    Client,
    Embed,
    Extension,
    InteractionContext,
    OptionTypes,
    Permissions,
    check,
    slash_command,
    slash_option,
    spread_to_rows,
)
from pymongo import MongoClient

from utilities.catbox import CatBox as catbox
from utilities.checks import *

load_dotenv()

cluster = MongoClient(os.getenv("MONGODB_URL"))

tags = cluster["madeline"]["tags"]


def geturl(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


def find_member(ctx, userid):
    members = [m for m in ctx.guild.members if m.id == userid]
    if members != []:
        for m in members:
            return m
    return None


class Tags(Extension):
    def __init__(self, bot: Client):
        self.bot = bot

    @slash_command(
        name="tag",
        sub_cmd_name="use",
        sub_cmd_description="allow's me to recall tags",
    )
    @slash_option(
        name="tagname",
        description="Type a name of a tag",
        opt_type=OptionTypes.STRING,
        required=True,
    )
    async def t(self, ctx: InteractionContext, tagname: str):
        regx = {"$regex": f"^{tagname}$", "$options": "i"}
        tppk = tags.find_one({"names": regx, "guild_id": ctx.guild_id})
        if tppk is None:
            embed = Embed(
                description=f"<:cross:839158779815657512> `{tagname}` is not a tag",
                color=0xDD2222,
            )
            await ctx.send(embed=embed, ephemeral=True)
        else:
            at = tppk["attachment_url"]
            cont = tppk["content"]
            if at is not None:
                if cont is not None:
                    await ctx.send(f"{cont}\n{at}")
                else:
                    await ctx.send(f"{at}")
            else:
                await ctx.send(f"{cont}")
            uses = tppk["no_of_times_used"]
            tags.update_one(
                {"names": regx, "guild_id": ctx.guild_id},
                {"$set": {"no_of_times_used": uses + 1}},
            )


def setup(bot):
    Tags(bot)
