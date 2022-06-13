import random

from naff import Extension, slash_command


class rpname(Extension):
    @slash_command(
        "rpname",
        description="the next big unique dynamic server.",
    )
    async def rpname(self, ctx):
        rpfirst = [
            "CJ",
            "O.G.",
            "SAMP",
            "Bay",
            "Bone",
            "Bulgarian",
            "Capital",
            "Carl",
            "Evolve",
            "Gay",
            "German",
            "God",
            "Godfather",
            "Grand",
            "Halal",
            "Infinity",
            "Las",
            "Leaked",
            "Los",
            "Next",
            "One",
            "Payday",
            "Pisd",
            "Pure",
            "Red",
            "Role",
            "San",
            "Scavenge",
            "Sexy",
            "Texas",
            "Kungkingkang",
            "Mengontol",
            "Misebah",
        ]

        rpsecond = [
            "SAMP",
            "Andreas",
            "Area",
            "Christian",
            "Cops",
            "County",
            "Day",
            "Game",
            "Gangstas",
            "Ginger",
            "Halal",
            "Johnson",
            "Larceny",
            "Life",
            "One",
            "Parrot",
            "Pisd",
            "Play",
            "Survive",
            "Turtle",
            "World",
            "Timer",
        ]

        await ctx.send(f"{random.choice(rpfirst)} {random.choice(rpsecond)} Roleplay")


def setup(bot):
    # This is called by dis-snek so it knows how to load the Extension
    rpname(bot)
