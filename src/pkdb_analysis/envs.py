"""
Access to important environment variables.
"""
import logging
import os
from urllib import parse as urlparse

from pkdb_analysis.logging_utils import bcolors


# FIXME: this makes changing endpoints programmatically extremely difficult.
# FIXME: better environment variable names

logger = logging.getLogger(__name__)

try:
    BASE_URL = os.environ["API_BASE"]
    # fix terminal slash
    if BASE_URL.endswith("/"):
        BASE_URL = BASE_URL[:-1]

except KeyError as err:
    BASE_URL = "https://alpha.pk-db.com"
    logger.warning(f"No 'BASE_URL' set, using: '{BASE_URL}'")
    logger.warning(
        f"Environment variables have not been initialized. "
        f"1. add authentication credentials; and 2. run {bcolors.OKBLUE}set -a && "
        f"source .env.local{bcolors.ENDC}. "
        f"Queries will be performed as 'anonymous user' on endpoint '{BASE_URL}"
    )

API_URL = BASE_URL + "/api/v1"

try:
    USER = os.environ["USER"]
except KeyError as err:
    USER = None
    logger.warning(f"No 'USER' set, using: '{USER}'")

try:
    PASSWORD = os.environ["PASSWORD"]
except KeyError as err:
    PASSWORD = None
    logger.warning(f"No 'PASSWORD' set, using: '{PASSWORD}'")
