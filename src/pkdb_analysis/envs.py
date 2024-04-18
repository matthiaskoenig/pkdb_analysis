"""Definition of environment variables."""
import os

from pkdb_analysis.log import get_logger

# FIXME: this makes changing endpoints programmatically extremely difficult.
# FIXME: better environment variable names

logger = get_logger(__name__)

try:
    BASE_URL = os.environ["API_BASE"]
    if BASE_URL.endswith("/"):
        BASE_URL = BASE_URL[:-1]

except KeyError as err:
    BASE_URL = "https://alpha.pk-db.com"
    logger.warning(f"No 'BASE_URL' set, using: '{BASE_URL}'")
    logger.warning(
        f"Environment variables have not been initialized. "
        f"1. add authentication credentials; and 2. run 'set -a && "
        f"source .env'. "
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
