import datetime
from typing import Optional

from naff import (
    Embed,
    Extension,
    OptionTypes,
    SlashCommandChoice,
    slash_command,
    slash_option,
)
from naff.ext.paginators import Paginator
from samp_client.client import SampClient


class samp(Extension):
    @slash_command(
        "samp-query", description="Show SA-MP server info and basic player information"
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
        # need to defer it, otherwise, it fails
        await ctx.defer()
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


def setup(bot):
    # This is called by dis-snek so it knows how to load the Extension
    samp(bot)
