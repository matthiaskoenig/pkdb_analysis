"""
Querying PK-DB
"""
import logging
from copy import deepcopy
from io import BytesIO
from pathlib import Path
from typing import List, Set
from urllib import parse as urlparse

import pandas as pd
import requests

from pkdb_analysis.data import PKData
from pkdb_analysis.envs import API_URL, BASE_URL, PASSWORD, USER
from pkdb_analysis.utils import recursive_iter


logger = logging.getLogger(__name__)


class PKFilter(object):
    """Filter objects for PKData"""

    KEYS = [
        "studies",
        "groups",
        "individuals",
        "interventions",
        "outputs",
        "timecourses",
        # special keys
        "concise",
        "download",
    ]

    def __init__(self, concise: bool = False, download: bool = True):
        """Create new Filter instance."""
        self.studies = dict()
        self.groups = dict()
        self.individuals = dict()
        self.interventions = dict()
        self.outputs = dict()
        self.timecourses = dict()

        # special arguments
        self.concise = f"{concise}".lower()
        self.download = f"{download}".lower()

    @property
    def url_params(self) -> str:
        """Parse filters to url"""
        return "?" + urlparse.urlencode(self._flat_params())

    def _flat_params(self) -> dict:
        """Helper function to parse filters to url"""
        return {
            "__".join(keys): value for keys, value in recursive_iter(self.to_dict())
        }

    def to_dict(self) -> dict:
        """Reformat filter instance to a dictonary."""
        return {
            filter_key: deepcopy(getattr(self, filter_key))
            for filter_key in PKFilter.KEYS
        }


def query_pkdb_data(
    h5_path: Path = None,
    zip_path: Path = None,
    pkfilter: PKFilter = None,
    creator: str = None,
    curators: List[str] = None,
    study_names: List = None,
) -> PKData:
    """Query the PK-DB database.

    If no usernames or study_names are provided the complete database will be
    queried.
    """
    # update filters
    if pkfilter is None:
        pkfilter = PKFilter()

    if creator:
        pkfilter.studies["creator"] = creator
    if curators:
        pkfilter.studies["curators__in"] = "__".join(curators)
    if study_names is not None:
        pkfilter.studies["name__in"] = "__".join(study_names)

    # query data
    pkdata = PKDB.query(pkfilter)

    if h5_path is not None:
        logger.info(f"Storing pkdata to HDF5: {h5_path}")
        pkdata.to_hdf5(h5_path)

    if zip_path is not None:
        logger.info(f"Storing pkdata to zip archive: {zip_path}")
        pkdata.to_archive(zip_path)

    return pkdata


class PKDB(object):
    """Interface to PK-DB.

    Helpers for querying PKData from PK-DB.
    """

    @classmethod
    def query(cls, pkfilter: PKFilter = None) -> PKData:
        """Creates a PKData representation and gets the data for the provided filters.

        If no filters are given the complete data is retrieved.
        """
        if pkfilter is None:
            pkfilter = PKFilter()

        url = API_URL + "/filter/" + pkfilter.url_params
        headers = cls.get_authentication_headers(BASE_URL, USER, PASSWORD)
        logger.warning(url)

        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            bytes_buffer = BytesIO()
            for chunk in r.iter_content(chunk_size=8192):
                bytes_buffer.write(chunk)
            return PKData.from_download(bytes_buffer)

    @classmethod
    def query_info_nodes_sids(cls) -> Set[str]:
        """Queries the sids of the info nodes"""
        url = API_URL + "/info_nodes/"
        headers = cls.get_authentication_headers(BASE_URL, USER, PASSWORD)
        logger.warning(url)
        df = cls._get_data(url, headers, page_size=1000)
        return set(df["sid"])

    @classmethod
    def get_authentication_headers(cls, api_base, username, password) -> dict:
        """Get authentication header with token for given user.

        Returns admin authentication as default.
        """
        auth_dict = {"username": username, "password": password}
        for key, value in auth_dict.items():
            if value is None:
                return {}
        auth_token_url = urlparse.urljoin(api_base, "api-token-auth/")
        try:
            response = requests.post(auth_token_url, json=auth_dict)
        except requests.exceptions.ConnectionError as e:
            raise requests.exceptions.InvalidURL(
                f"Error Connecting (probably wrong url <{api_base}>): ", e
            )

        if response.status_code != 200:
            logger.error(
                f"Request headers could not be retrieved from: {auth_token_url}"
            )
            logger.warning(response.text)
            raise requests.exceptions.ConnectionError(response)

        token = response.json().get("token")
        return {"Authorization": f"token {token}"}

    @staticmethod
    def _get_data(url, headers, **parameters) -> pd.DataFrame:
        """Gets data from a paginated rest API."""
        url_params = "?" + urlparse.urlencode(parameters)
        actual_url = urlparse.urljoin(url, url_params)
        logger.info(actual_url)

        # FIXME: make first request fast
        response = requests.get(actual_url, headers=headers)
        try:
            response.raise_for_status()
            num_pages = response.json()["last_page"]

        except requests.exceptions.HTTPError as err:
            raise err

        data = []
        for page in range(1, num_pages + 1):
            url_current = actual_url + f"&page={page}"
            logger.info(url_current)

            response = requests.get(url_current, headers=headers)
            data += response.json()["data"]["data"]

        # convert to data frame
        df = pd.DataFrame(data)
        is_array = "timecourse" in url or "scatters" in url

        return PKData._clean_types(df, is_array)
