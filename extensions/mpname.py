import random

from naff import Extension, slash_command


class mpname(Extension):
    @slash_command(
        "mpname",
        description="scrapes the web for the next BIG samp ripoff.",
    )
    async def mpname(self, ctx):
        coolwordsxd = [
            "CJ",
            "O.G.",
            "SAMP",
            "adorable",
            "bay",
            "bone",
            "bulgarian",
            "capital",
            "carl",
            "evolve",
            "gay",
            "god",
            "godfather",
            "halal",
            "infinity",
            "las",
            "leaked",
            "mom",
            "next",
            "one",
            "payday",
            "pisd",
            "pure",
            "red",
            "role",
            "san",
            "scavenge",
            "sexy",
            "texas",
        ]

        morewords = [
            "SAMP",
            "andreas",
            "area",
            "christian",
            "cops",
            "county",
            "day",
            "game",
            "gangstas",
            "ginger",
            "halal",
            "johnson",
            "life",
            "one",
            "parrot",
            "pisd",
            "play",
            "survive",
            "turtle",
            "world",
        ]

        await ctx.send(f"{random.choice(coolwordsxd)} {random.choice(morewords)}")


def setup(bot):
    # This is called by dis-snek so it knows how to load the Extension
    mpname(bot)
