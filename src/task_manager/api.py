# api.py: Defines the public API
#
# (C) 2020, Daniel Mouritzen

from pathlib import Path

import attr
from loguru import logger


@attr.s
class TaskManagerAPI:
    data_dir: Path = attr.ib(converter=Path)
    config_file: Path = attr.ib(converter=Path)

    def __attrs_post_init__(self):
        logger.info(f'Data: {self.data_dir}')
        logger.info(f'Config: {self.config_file}')
