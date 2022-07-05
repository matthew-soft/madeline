from io import BytesIO

import aiohttp
import pytesseract
from naff import (
    Embed,
    Extension,
    InteractionContext,
    OptionTypes,
    slash_command,
    slash_option,
)
from PIL import Image

from core.base import CustomClient


class ocr(Extension):
    bot: CustomClient

    @slash_command(
        name="ocr",
        description="Read text inside of an image (Optical Character Recognition)",
    )
    @slash_option(
        name="attachment",
        description="The image to read",
        opt_type=OptionTypes.ATTACHMENT,
        required=True,
    )
    async def ocr(self, ctx: InteractionContext, attachment: OptionTypes.ATTACHMENT):

        # needs to be deferred, otherwise it will error
        await ctx.defer()

        if (
            (attachment.content_type == "image/png")
            or (attachment.content_type == "image/jpg")
            or (attachment.content_type == "image/jpeg")
        ):
            # get the image from the attachment
            async with aiohttp.ClientSession() as session:
                async with session.get(str(attachment.url)) as response:
                    image_url = await response.read()

            # then use pytesseract to read the image
            img1 = Image.open(BytesIO(image_url))
            text = pytesseract.image_to_string(img1)

            # limit the text to 2048 characters
            if len(text) > 4096:
                text = text[:4093] + "..."

            # create the embed
            embed = Embed(color=0x848585)
            embed.set_author(
                name=f"{ctx.author}",
                icon_url=ctx.author.avatar.url,
                url=f"https://discord.com/users/{ctx.author.id}",
            )
            embed.title = "Here's the result!"
            embed.description = f"```{text}```"
            embed.set_image(url=image_url)
            embed.set_footer(
                text=f"Optical Character Recognition",
                icon_url="https://cdn.notsobot.com/brands/google-go.png",
            )
            return await ctx.send(embed=embed)
        else:
            embed = Embed(
                description=f"<:cross:839158779815657512> Can't read the attachments, maybe it's not an image? (We only support `png`, `jpg`, and `jpeg` filetypes)",
                color=0xDD2222,
            )
            return await ctx.send(embed=embed, ephemeral=True)


def setup(bot: CustomClient):
    """Let naff load the extension"""

    ocr(bot)
