"""
Querying PK-DB
"""
import logging
import tempfile
import zipfile
from copy import deepcopy
from io import BytesIO, StringIO
from pathlib import Path
from typing import List, Set
from urllib import parse as urlparse

import numpy as np
import pandas as pd
import requests

from pkdb_analysis.data import PKData
from pkdb_analysis.envs import API_URL, BASE_URL, PASSWORD, USER
from pkdb_analysis.utils import recursive_iter


logger = logging.getLogger(__name__)


def query_pkdb_data(
    h5_path: Path = None, username: str = None, study_names: List = None
) -> PKData:
    """Query the complete database.

    Filtering by study name is supported.

    :param study_names: Iterable of study_names to filter for.
    :param username: filter studies by username
    """
    studies_filter = {}
    if username is not None:
        studies_filter = {"creator": username}
    if study_names is not None:
        studies_filter = {"name__in": "__".join(study_names), **studies_filter}
    pkfilter = PKFilter()
    pkfilter.studies = studies_filter
    pkdata = PKDB.query_(pkfilter)
    if h5_path is not None:
        logger.info(f"Storing pkdb data: {h5_path}")
        pkdata.to_hdf5(h5_path)
    return pkdata

class PKFilter(object):
    """Filter objects for PKData"""

    KEYS = [
        "studies",
        "groups",
        "individuals",
        "interventions",
        "outputs",
        "timecourses",
        "concise",
        "download",
    ]

    def __init__(self, concise=False, download=True):
        """Create new Filter instance."""
        # Filter keys
        self.studies = dict()
        self.groups = dict()
        self.individuals = dict()
        self.interventions = dict()
        self.outputs = dict()
        self.timecourses = dict()
        # Special arguments
        self.concise = f"{concise}".lower()
        self.download = f"{download}".lower()

        # self._set_normed(normed)

    @property
    def url_params(self) -> str:
        """ Parse filters to url """
        return "?" + urlparse.urlencode(self._flat_params())

    def _flat_params(self) -> dict:
        """ Helper function to parse filters to url"""
        return {
            "__".join(keys): value for keys, value in recursive_iter(self.to_dict())
        }

    def to_dict(self) -> dict:
        """ Reformat filter instance to a dictonary."""
        return {
            filter_key: deepcopy(getattr(self, filter_key))
            for filter_key in PKFilter.KEYS
        }


class PKDB(object):
    """ Querying PKData from PK-DB. """

    @classmethod
    def query(cls, pkfilter: PKFilter = PKFilter(), page_size: int = 2000) -> "PKData":
        """Create a PKData representation and gets the data for the provided filters.
        If no filters are given the complete data is retrieved.

        :param pkfilter: Filter object to select subset of data, if no Filter is provided the complete data is returned
        :param page_size: number of entries per query
        """
        pkfilter = pkfilter.to_dict()
        parameters = {"format": "json", "page_size": page_size}
        logger.info("*** Querying data ***")
        pkdata = PKData(
            studies=cls._get_subset(
                "pkdata/studies", **{**parameters, **pkfilter.get("studies", {})}
            ),
            interventions=cls._get_subset(
                "pkdata/interventions",
                **{**parameters, **pkfilter.get("interventions", {})},
            ),
            individuals=cls._get_subset(
                "pkdata/individuals",
                **{**parameters, **pkfilter.get("individuals", {})},
            ),
            groups=cls._get_subset(
                "pkdata/groups", **{**parameters, **pkfilter.get("groups", {})}
            ),
            outputs=cls._get_subset(
                "pkdata/outputs", **{**parameters, **pkfilter.get("outputs", {})}
            ),
            timecourses=cls._get_subset(
                "pkdata/timecourses",
                **{**parameters, **pkfilter.get("timecourses", {})},
            ),
        )
        return pkdata._intervention_pk_update()

    @classmethod
    def _get_subset(cls, name, **parameters):
        """FIXME: document me.

        :param name: name of the view
        :param parameters: query parameters
        :return:
        """
        if not name in [
            "pkdata/individuals",  # individuals
            "pkdata/groups",  # groups
            "pkdata/interventions",  # interventions
            "pkdata/outputs",  # outputs
            "pkdata/timecourses",  # timecourses
            "pkdata/studies",  # studies
        ]:
            raise ValueError(f"{name} not supported")

        url = API_URL + f"/{name}/"
        return cls._get_data(
            url, cls.get_authentication_headers(BASE_URL, USER, PASSWORD), **parameters
        )

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

    @classmethod
    def query_(cls, pkfilter: PKFilter = PKFilter()) -> "PKData":
        url = API_URL + "/filter/" + pkfilter.url_params
        headers = cls.get_authentication_headers(BASE_URL, USER, PASSWORD)
        logger.warning(url)

        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            bytes_buffer = BytesIO()
            for chunk in r.iter_content(chunk_size=8192):
                bytes_buffer.write(chunk)
            return PKData.from_archive(bytes_buffer)


    @classmethod
    def query_info_nodes(cls) -> Set[str]:
        url = API_URL + "/info_nodes/"
        headers = cls.get_authentication_headers(BASE_URL, USER, PASSWORD)
        logger.warning(url)
        df = cls._get_data(url, headers, page_size=1000)
        return set(df["sid"])



