"""
Access to important environment variables.
"""
import logging
import os
from urllib import parse as urlparse

from pkdb_analysis.logging_utils import bcolors


logger = logging.getLogger(__name__)

try:
    BASE_URL = os.environ["API_BASE"]
    # fix terminal slash
    if BASE_URL.endswith("/"):
        BASE_URL = BASE_URL[:-1]

    USER = os.environ["USER"]
    PASSWORD = os.environ["PASSWORD"]

    API_URL = BASE_URL + "/api/v1"

except KeyError:

    USER = None
    PASSWORD = None
    BASE_URL = "https://alpha.pk-db.com"

    API_URL = BASE_URL + "/api/v1"
    logger.warning(
        f"Environment variables have not been initialized. "
        f"1. add authentication credentials; and 2. run {bcolors.OKBLUE}set -a && "
        f"source .env.local{bcolors.ENDC}. "
        f"Queries will be performed as 'anonymous user' on endpoint '{BASE_URL}"
    )
