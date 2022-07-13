import datetime
import random
import re
import statistics
import string
import urllib.parse

import aiohttp
from naff import (
    Embed,
    Extension,
    InteractionContext,
    OptionTypes,
    slash_command,
    slash_option,
)

from core.base import CustomClient

smallcaps_alphabet = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ1234567890"

uppercase_fraktur = "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ"
lowercase_fraktur = "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷1234567890"

uppercase_boldfraktur = "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"
lowercase_boldfraktur = "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟1234567890"


double_uppercase = "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"

double_lowercase = "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘"

bold_fancy_lowercase = "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃1234567890"
bold_fancy_uppercase = "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"

fancy_lowercase = "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢"
fancy_uppercase = "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"


alphabet = dict(zip("abcdefghijklmnopqrstuvwxyz1234567890", range(0, 36)))
uppercase_alphabet = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(0, 26)))
punctuation = dict(zip("§½!\"#¤%&/()=?`´@£$€{[]}\\^¨~'*<>|,.-_:", range(0, 37)))
space = " "
aesthetic_space = "\u3000"
aesthetic_punctuation = '§½！"＃¤％＆／（）＝？`´＠£＄€｛［］｝＼＾¨~＇＊＜＞|，．－＿：'
aesthetic_lowercase = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ１２３４５６７８９０"
aesthetic_uppercase = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"


def aesthetics(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += aesthetic_lowercase[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += aesthetic_uppercase[uppercase_alphabet[letter]]
            elif letter in punctuation:
                returnthis += aesthetic_punctuation[punctuation[letter]]
            elif letter == space:
                returnthis += aesthetic_space
            else:
                returnthis += letter
    return returnthis


def double_font(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += double_lowercase[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += double_uppercase[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis


def fraktur(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += lowercase_fraktur[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += uppercase_fraktur[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis


def bold_fraktur(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += lowercase_boldfraktur[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += uppercase_boldfraktur[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis


def fancy(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += fancy_lowercase[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += fancy_uppercase[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis


def bold_fancy(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += bold_fancy_lowercase[alphabet[letter]]
            elif letter in uppercase_alphabet:
                returnthis += bold_fancy_uppercase[uppercase_alphabet[letter]]
            elif letter == space:
                returnthis += " "
            else:
                returnthis += letter
    return returnthis


def smallcaps(string):
    returnthis = ""
    for word in string:
        for letter in word:
            if letter in alphabet:
                returnthis += smallcaps_alphabet[alphabet[letter]]
            else:
                returnthis += letter
    return returnthis


eight_ball_responses = [
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes, definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful",
]


class CoolKidsClub(Extension):
    bot: CustomClient

    @slash_command(
        name="ckc", description="Cool Kids Commands™ 😎",
        group_name="fonts",
        group_description="Font Manipulation Commands",
        sub_cmd_name="aesthetics", sub_cmd_description="Generate aesthetics words from a string"
    )
    @slash_option(
        name="text",
        description="The text to be converted",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def aes(self, ctx: InteractionContext, text: str):
        # respond to the interaction
        await ctx.send(aesthetics(text))

    @slash_command(name="ckc", description="Cool Kids Commands™ 😎",
        group_name="fonts",
        group_description="Font Manipulation Commands", sub_cmd_name="fraktur", sub_cmd_description="Generate fraktur words from a string")
    @slash_option(
        name="text",
        description="The text to be converted",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def fraktur(self, ctx: InteractionContext, text: str):
        # respond to the interaction
        await ctx.send(fraktur(text))

    @slash_command(
        name="ckc", description="Cool Kids Commands™ 😎",
        group_name="fonts",
        group_description="Font Manipulation Commands", sub_cmd_name="bold-fraktur", sub_cmd_description="Generate bold fraktur words from a string"
    )
    @slash_option(
        name="text",
        description="The text to be converted",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def bold_fraktur(self, ctx: InteractionContext, text: str):
        # respond to the interaction
        await ctx.send(bold_fraktur(text))

    @slash_command(name="ckc", description="Cool Kids Commands™ 😎",
        group_name="fonts",
        group_description="Font Manipulation Commands", sub_cmd_name="fancy", sub_cmd_description="Generate fancy words from a string")
    @slash_option(
        name="text",
        description="The text to be converted",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def fancy(self, ctx: InteractionContext, text: str):
        # respond to the interaction
        await ctx.send(fancy(text))

    @slash_command(
        name="ckc", description="Cool Kids Commands™ 😎",
        group_name="fonts",
        group_description="Font Manipulation Commands",
        sub_cmd_name="bold-fancy", sub_cmd_description="Generate bold fancy words from a string"
    )
    @slash_option(
        name="text",
        description="The text to be converted",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def bold_fancy(self, ctx: InteractionContext, text: str):
        # respond to the interaction
        await ctx.send(bold_fancy(text))

    @slash_command(name="ckc", description="Cool Kids Commands™ 😎",
        group_name="fonts",
        group_description="Font Manipulation Commands", sub_cmd_name="double", sub_cmd_description="Generate double font from a string")
    @slash_option(
        name="text",
        description="The text to be converted",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def db(self, ctx: InteractionContext, text: str):
        # respond to the interaction
        await ctx.send(double_font(text))

    @slash_command(
        name="ckc", description="Cool Kids Commands™ 😎",
        group_name="fonts",
        group_description="Font Manipulation Commands",
        sub_cmd_name="small-caps", sub_cmd_description="Generate small caps words from a string"
    )
    @slash_option(
        name="text",
        description="The text to be converted",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def smallcaps(self, ctx: InteractionContext, text: str):
        # respond to the interaction
        await ctx.send(smallcaps(text))

    @slash_command(name="ckc", description="Cool Kids Commands™ 😎",
        group_name="fun",
        group_description="Fun Commands", sub_cmd_name="8ball", sub_cmd_description="Ask the 8 Ball a question")
    @slash_option(
        name="question",
        description="The question you wanna ask 8 Ball (could be empty)",
        required=False,
        opt_type=OptionTypes.STRING,
    )
    async def ball(self, ctx: InteractionContext, question=None):
        # respond to the interaction
        r = random.choice(eight_ball_responses)
        await ctx.send(":8ball: | {}, **{}**".format(r, ctx.author.display_name))


    @slash_command(name="ckc", description="Cool Kids Commands™ 😎",
        group_name="fun",
        group_description="Fun Commands", sub_cmd_name="coinflip", sub_cmd_description="Flip a coin")
    async def flipcoin(self, ctx: InteractionContext):
        # respond to the interaction
        await ctx.send(random.choice(("Heads", "Tails")))

    @slash_command(name="ckc", description="Cool Kids Commands™ 😎",
        group_name="fun",
        group_description="Fun Commands", sub_cmd_name="dice", sub_cmd_description="Roll a dice")
    @slash_option(
        name="sides",
        description="The number of sides on the dice",
        required=False,
        opt_type=OptionTypes.INTEGER,
    )
    @slash_option(
        name="rolls",
        description="The number of dice to roll",
        required=False,
        opt_type=OptionTypes.INTEGER,
    )
    async def dice(self, ctx: InteractionContext, sides: int = 6, rolls: int = 1):
        results = []
        if sides > 1000000000000 or rolls > 100:
            return
        for _ in range(rolls):
            results.append(random.randint(1, sides))
        median = statistics.median(results)
        mean = statistics.mean(results)
        if len(results) <= 30:
            results = ", ".join([str(x) for x in results])
            # results = ', '.join(results)
            await ctx.send(
                "You rolled **{0}** **{1}-sided** dice, results: **{2}**\nMedian: **{3}**, mean: **{4:.2f}**".format(
                    rolls, sides, results, median, mean
                )
            )
        else:
            await ctx.send(
                "You rolled **{0}** **{1}-sided** dice\nMedian: **{2}**, mean: **{3:.2f}**".format(
                    rolls, sides, median, mean
                )
            )

    @slash_command(name="ckc", description="Cool Kids Commands™ 😎",
        group_name="fun",
        group_description="Fun Commands", sub_cmd_name="lmgtfy", sub_cmd_description="Create a lmgtfy link.")
    @slash_option(
        "search_terms", "Term to search for", OptionTypes.STRING, required=True
    )
    async def lmgtfy(self, ctx: InteractionContext, search_terms: str):
        search_terms = urllib.parse.quote_plus(search_terms)
        await ctx.send("https://lmgtfy.app/?q={}".format(search_terms))


def setup(bot: CustomClient):
    """Let naff load the extension"""

    CoolKidsClub(bot)
