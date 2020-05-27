"""
Access to important environment variables.
"""
import os
import logging
from urllib import parse as urlparse
from pkdb_analysis.logging_utils import bcolors

logger = logging.getLogger(__name__)

try:
    API_BASE = os.environ['API_BASE']
    # fix terminal slash
    if API_BASE.endswith('/'):
        API_BASE = API_BASE[:-1]

    USER = os.environ['USER']
    PASSWORD = os.environ['PASSWORD']

    API_URL = API_BASE + "/api/v1"

except KeyError:

    USER = None
    PASSWORD = None
    API_BASE = "https://develop.pk-db.com"

    API_URL = API_BASE + "/api/v1"
    logger.warning(
        f"Environment variables have not been initialized. "
        f"1. add authentication credentials; and 2. run {bcolors.OKBLUE}set -a && "
        f"source .env.local{bcolors.ENDC}. Queries will be performed as a anonymous user.")
