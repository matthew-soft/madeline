async def send_guild_stats(self, e, guild, r_channel):
    owner = await self.bot.fetch_user(guild._owner_id)
    e.add_field(name="Name", value=guild.name)
    e.add_field(name="ID", value=guild.id)
    e.add_field(name="Owner", value=f"{owner.mention} (ID: {owner.id})")

    total = guild.member_count
    e.add_field(name="Members", value=str(total))

    if guild.icon:
        e.set_thumbnail(url=guild.icon.url)

    if guild.me:
        e.timestamp = guild.me.joined_at

    ch = self.bot.get_channel(r_channel)
    await ch.send(embed=e)