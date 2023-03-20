"""
    :module_name: tilematch_tools
    :module_summary: entry point to the tilematch_tools package
    :module_author: Nathan Mendoza (nathancm@uci.edu)
"""

import logging
import os

from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger(__name__)
LOG_HANDLER = logging.StreamHandler()
LOG_FORMAT = logging.Formatter('[%(asctime)s|%(name)s|%(levelname)s] - %(message)s')

log_level_map = {
    'release': logging.CRITICAL,
    'develop': logging.DEBUG
}

LOGGER.setLevel(log_level_map.get(os.getenv('logconf', 'release'), 'release'))
LOG_HANDLER.setLevel(log_level_map.get(os.getenv('logconf', 'release'), 'release'))

LOG_HANDLER.setFormatter(LOG_FORMAT)
LOGGER.addHandler(LOG_HANDLER)

__version__ = (0, 0, 1)

from .core import *
from .model import *
from .view import *
