import re
from typing import Awaitable, Callable, Union

from naff import Permissions
from naff.client.errors import *
from naff.models.naff.context import Context

TYPE_CHECK_FUNCTION = Callable[[Context], Awaitable[bool]]


class MissingPermissions(CommandException):
    """User is missing permissions"""


def member_permissions(*permissions: Permissions) -> TYPE_CHECK_FUNCTION:
    """
    Check if member has any of the given permissions.

    Args:
        *permissions: The Permission(s) to check for
    """

    async def check(ctx: Context) -> bool:
        if ctx.guild is None:
            return False
        if any(ctx.author.has_permission(p) for p in permissions):
            return True

    return check

def is_owner():
    """
    Is the author the owner of the bot.
    """

    async def check(ctx: Context) -> bool:
        return ctx.author.id == 351150966948757504

    return check