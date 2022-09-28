import logging
import os

import sentry_sdk
from dotenv import load_dotenv
from naff import Client, listen, logger_name


class CustomClient(Client):
    """Subclass of naff.Client with our own logger and on_startup event"""

    # you can use that logger in all your extensions
    logger = logging.getLogger(logger_name)

    load_dotenv()

    # sentry sdk init
    sentry_sdk.init(
        os.getenv("SENTRY_DSN"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )

    async def on_error(self, source, error):
        """Gets triggered on an error"""
        self.logger.error(f"{source} raised {error}")
    
    async def on_command_error(self, ctx, error):
        """Gets triggered on a command error"""
        self.logger.error(f"Command error: {ctx} raised {error}")
    
    async def on_command(self, ctx):
        """Gets triggered on a command"""
        self.logger.info(f"Command: {ctx} was executed")

    @listen()
    async def on_startup(self):
        """Gets triggered on startup"""

        self.logger.info(f"{os.getenv('PROJECT_NAME')} - Startup Finished!")
        self.logger.info(
            "Note: Discord needs up to an hour to load global commands / context menus. They may not appear immediately\n"
        )
