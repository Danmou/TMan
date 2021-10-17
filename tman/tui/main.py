#  Copyright (c) 2021, Daniel Mouritzen.

"""Main TUI entry point."""

from appdirs import user_config_dir, user_data_dir, user_log_dir
from loguru import logger

from tman.api import TManAPI
from tman.util.logging import init_logging


def run() -> None:
    """Start TUI."""
    app_name = "TMan"
    init_logging(verbosity="DEBUG", logdir=user_log_dir(app_name), stdout=False)

    logger.debug("Initializing backend")
    api = TManAPI(  # noqa: F841
        data_dir=user_data_dir(app_name), config_file=user_config_dir(app_name) + "/config.json"
    )

    logger.debug("Starting UI")

    logger.info("Finished successfully.")
