import datetime

from naff import ActionRow, Button, ButtonStyles, Embed, Extension, slash_command


class help(Extension):
    @slash_command("help", description="Get the list of available commands")
    async def help(self, ctx):
        embed = Embed(
            description=f"Visit our [Official Documentations](https://madeline.my.id) for more info.",
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
            value="`about`, `help`, `ping`",
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


def setup(bot):
    # This is called by dis-snek so it knows how to load the Extension
    help(bot)
