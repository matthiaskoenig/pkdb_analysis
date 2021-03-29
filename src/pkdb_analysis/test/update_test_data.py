"""Update test data files."""
from pathlib import Path

import requests

from pkdb_analysis import PKData
from pkdb_analysis.envs import API_URL
from pkdb_analysis.test import (
    TEST_HDF5,
    TESTDATA_CONCISE_FALSE_ZIP,
    TESTDATA_CONCISE_TRUE_ZIP,
)


# API_URL = "http://localhost:8000/api/v1"
API_URL = "https://alpha.pk-db.com/api/v1"


def update_test_data(path_zip: Path, concise: bool) -> None:
    """Downloads latest test data with concise True/False.

    :param path_zip: Path to output zip file for storage
    :param concise: boolean flag to download concise or non-concise data
    """

    url = (
        f"{API_URL}/filter/?download=true&concise=" + f"{concise}".lower()
    )  # +"&studies__sid__in=PKDB00198"
    print(url)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path_zip, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
            print(path_zip)


def update_all() -> None:
    """Update all test data files."""
    update_test_data(TESTDATA_CONCISE_FALSE_ZIP, concise=False)
    update_test_data(TESTDATA_CONCISE_TRUE_ZIP, concise=True)


if __name__ == "__main__":
    update_all()
