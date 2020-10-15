"""
Querying PK-DB
"""
import logging
from copy import deepcopy
from pathlib import Path
from typing import List
from urllib import parse as urlparse

import numpy as np
import pandas as pd
import requests

from pkdb_analysis.data import PKData
from pkdb_analysis.envs import API_URL, BASE_URL, PASSWORD, USER


logger = logging.getLogger(__name__)


def query_pkdb_data(
    h5_path: Path = None, username: str = None, study_names: List = None
) -> PKData:
    """Query the complete database.

    Filtering by study name is supported.

    :param filter_study_names: Iterable of study_names to filter for.
    :param username: filter studies by username
    """
    if h5_path.exists():
        logger.warning(f"Existing data file is overwritten: {h5_path}")

    if study_names is not None:
        study_filter = PKFilter()
        study_filter.add_to_all("study_name__in", "__".join(study_names))
        pkdata = PKDB.query(pkfilter=study_filter)
    else:
        pkdata = PKDB.query()

    if username is not None:
        # Filter studies by username
        pkdata.studies["username"] = pkdata.studies.creator.apply(pd.Series).username
        pkdata = pkdata.filter_study(
            f_idx=lambda pkdata: pkdata["username"] == username
        )

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
    ]

    def __init__(self, normed=True):
        """Create new Filter instance.

        :param normed: [True, False, None] return [normed data, unnormalized data,
                        normed and unnormalized data]
        """
        self.studies = dict()
        self.groups = dict()
        self.individuals = dict()
        self.interventions = dict()
        self.outputs = dict()
        self.timecourses = dict()

        self._set_normed(normed)

    def _set_normed(self, normed=True) -> None:
        """Set the normed attribute

        :param normed:
        :return: None
        """
        if normed not in [True, False, None]:
            raise ValueError

        if normed in [True, False]:
            if normed:
                normed_value = "true"
            else:
                normed_value = "false"
            for filter_key in ["interventions", "outputs"]:
                d = getattr(self, filter_key)
                d["normed"] = normed_value

    def __str__(self) -> str:
        return str(self.to_dict())

    def to_dict(self) -> dict:
        return {
            filter_key: deepcopy(getattr(self, filter_key))
            for filter_key in PKFilter.KEYS
        }

    def add_to_all(self, key, value) -> None:
        """Adds entry (key, value) to all KEY dictionaries

        :return: None
        """
        for filter_key in PKFilter.KEYS:
            # FIXME: THIS IS A REPLACE, NOT A ADD !!!!
            getattr(self, filter_key)[key] = value


class PKFilterFactory(object):
    """ Factory for simple creation of PKFilters. """

    @staticmethod
    def by_study_sid(study_sid: str) -> PKFilter:
        """Creates filter based on study_sid.
        Only data for the given study_sid is returned.
        """
        pkfilter = PKFilter()
        pkfilter.add_to_all("study_sid", study_sid)
        return pkfilter

    @staticmethod
    def by_study_name(study_name: str) -> PKFilter:
        """Creates filter based on study_name.
        Only data for the given study_name is returned.
        """
        pkfilter = PKFilter()
        pkfilter.add_to_all("study_name", study_name)
        return pkfilter


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
    def get_authentication_headers(cls, api_base, username, password):
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
        is_timecourse = "timecourse" in url
        return PKData._clean_types(df, is_timecourse)





