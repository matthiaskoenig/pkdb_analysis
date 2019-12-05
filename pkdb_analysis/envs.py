"""
Access to important environment variables.
"""
import os
import logging
from pkdb_analysis.logging_utils import bcolors

logger = logging.getLogger(__name__)

try:
    API_BASE = os.environ['API_BASE']
    # fix terminal slash
    if API_BASE.endswith('/'):
        API_BASE = API_BASE[:-1]

    USER = os.environ['USER']
    PASSWORD = os.environ['PASSWORD']
    DEFAULT_USER_PASSWORD = os.environ['DEFAULT_USER_PASSWORD']

    API_URL = os.path.join(API_BASE, "api/v1")

except KeyError:
    logger.error(
        f"Environment variables have not been initialized. "
        f"1. add authentication credentials; and 2. run {bcolors.OKBLUE}set -a && source .env.local{bcolors.ENDC}")
    logger.error(f"")
    exit()