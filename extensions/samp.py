import datetime
from typing import Optional

from naff import (Embed, Extension, OptionTypes, SlashCommandChoice,
                  slash_command, slash_option)
from samp_client.client import SampClient


class samp(Extension):
    @slash_command(
        "samp", description="Show SA-MP server info and basic player information"
    )
    @slash_option(
        name="type",
        description="Type of information to show",
        required=True,
        opt_type=OptionTypes.INTEGER,
        choices=[
            SlashCommandChoice(name="General vibes", value=1),
            SlashCommandChoice(name="Server info only", value=2),
            SlashCommandChoice(name="Player info only", value=3),
        ],
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
    async def samp(self, ctx, type: int, ip: str, port: Optional[int] = 7777):
        with SampClient(address=ip, port=port) as kung:
            info = kung.get_server_info()
            players = kung.get_server_clients_detailed()
            numpang = kung.get_server_clients()
        # need to defer it, otherwise, it fails
        await ctx.defer()
        try:
            if type == 1:
                embed = Embed(title=info.hostname, color=0x0083F5)  # Create embed
                embed.add_field(name="IP", value=f"`{ip}:{port}`", inline=True)
                embed.add_field(
                    name="Gamemode : ", value=f"`{info.gamemode}`", inline=True
                )
                embed.add_field(
                    name="Language : ", value=f"`{info.language}`", inline=True
                )
                embed.add_field(
                    name="Passworded? : ", value=f"`{info.password}`", inline=True
                )
                embed.add_field(
                    name="Players : ",
                    value=f"`{info.players}` / `{info.max_players}` Players",
                    inline=True,
                )
                if info.players == 0:
                    embed.add_field(
                        name="[only show 10 player max] Connected Clients :",
                        value="No players connected",
                        inline=False,
                    )
                if info.players > 0:
                    for ppq in numpang:
                        embed.add_field(
                            name="[only show 10 player max] Connected Clients :",
                            value=f"```==============================================\nName                        | Score\n ==============================================\n {ppq.name}                    | {ppq.score}```",
                            inline=False,
                        )
                if info.players > 10:
                    embed.add_field(
                        name="Note:",
                        value="due to __*discord limitations*__, i can't show connected clients summary 😔",
                        inline=False,
                    )
                embed.set_footer(
                    text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
                )
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)  # Send the embed
            if type == 2:
                embed = Embed(title=info.hostname, color=0x0083F5)  # Create embed
                embed.add_field(name="IP", value=f"`{ip}:{port}`", inline=True)
                embed.add_field(
                    name="Gamemode : ", value=f"`{info.gamemode}`", inline=True
                )
                embed.add_field(
                    name="Language : ", value=f"`{info.language}`", inline=True
                )
                embed.add_field(
                    name="Passworded? : ", value=f"`{info.password}`", inline=True
                )
                embed.set_footer(
                    text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
                )
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)  # Send the embed
            if type == 3:
                if info.players == 0:
                    embed = Embed(
                        description=f"<:cross:839158779815657512> No players connected",
                        color=0xFF0000,
                    )  # Create embed
                else:
                    if info.players > 10:
                        embed = Embed(
                            title=info.hostname,
                            description="Note: due to __*discord limitations*__, i can't show detailed connected clients 😔",
                            color=0xF6ADAB,
                        )  # Create embed
                        embed.add_field(
                            name="Players : ",
                            value=f"`{info.players}` / `{info.max_players}` Players",
                            inline=True,
                        )
                        embed.set_footer(
                            text=f"Requested by {ctx.author}",
                            icon_url=ctx.author.avatar.url,
                        )
                        embed.timestamp = datetime.datetime.utcnow()
                    else:
                        embed = Embed(
                            title=info.hostname, color=0x4C8404
                        )  # Create embed
                        embed.add_field(
                            name="Players : ",
                            value=f"`{info.players}` / `{info.max_players}` Players",
                            inline=True,
                        )
                        for ppq in players:
                            embed.add_field(
                                name="[only show 10 player max] Detailed Connected Clients :",
                                value=f"```==============================================\nID |Name                        | Score | Ping\n ==============================================\n {ppq.id} | {ppq.name}                    | {ppq.score} | {ppq.ping}```",
                                inline=False,
                            )
                        embed.set_footer(
                            text=f"Requested by {ctx.author}",
                            icon_url=ctx.author.avatar.url,
                        )
                        embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)  # Send the embed
        except:
            embed = Embed(
                description=f"<:cross:839158779815657512> Couldn't connect to the server",
                color=0xFF0000,
            )


def setup(bot):
    # This is called by dis-snek so it knows how to load the Extension
    samp(bot)
