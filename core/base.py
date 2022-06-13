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

    @listen()
    async def on_startup(self):
        """Gets triggered on startup"""

        self.logger.info(f"{os.getenv('PROJECT_NAME')} - Startup Finished!")
        self.logger.info(
            "Note: Discord needs up to an hour to load your global commands / context menus. They may not appear immediately\n"
        )
