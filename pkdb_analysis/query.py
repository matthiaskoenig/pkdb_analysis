"""
Querying PK-DB
"""
import logging
from copy import deepcopy
from urllib import parse as urlparse

import numpy as np
import pandas as pd
import requests

from pkdb_analysis.data import PKData

logger = logging.getLogger(__name__)


class PKFilter(object):
    """
    Filter objects for PKData
    """
    KEYS = ['groups', 'individuals', "interventions", "outputs", "timecourses"]

    def __init__(self, normed=True):
        """ Create new Filter instance.

        :param normed: [True, False, None] return [normed data, unnormalized data, normed and unnormalized data]
        """
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
            for filter_key in ["interventions", "outputs", "timecourses"]:
                d = getattr(self, filter_key)
                d["normed"] = normed_value

    def __str__(self) -> str:
        return str(self.to_dict())

    def to_dict(self) -> dict:
        return {filter_key: deepcopy(getattr(self, filter_key)) for filter_key in PKFilter.KEYS}

    def add_to_all(self, key, value) -> None:
        """ Adds entry (key, value) to all KEY dictionaries

        :return: None
        """
        for filter_key in PKFilter.KEYS:
            getattr(self, filter_key)[key] = value


class PKFilterFactory(object):
    """ Factory for simple creation of PKFilters. """

    @staticmethod
    def by_study_sid(study_sid: str) -> PKFilter:
        """ Creates filter based on study_sid.
        Only data for the given study_sid is returned.
        """
        pkfilter = PKFilter()
        pkfilter.add_to_all("study_sid", study_sid)
        return pkfilter

    @staticmethod
    def by_study_name(study_name: str) -> PKFilter:
        """ Creates filter based on study_name.
        Only data for the given study_name is returned.
        """
        pkfilter = PKFilter()
        pkfilter.add_to_all("study_name", study_name)
        return pkfilter


class PKDB(object):
    """ Querying PKData from PK-DB. """
    PKDB_URL = "http://0.0.0.0:8000"
    PKDB_USERNAME = "admin"
    PKDB_PASSWORD = "pkdb_admin"
    URL_BASE = urlparse.urljoin(PKDB_URL, '/api/v1/')

    @classmethod
    def query(cls, pkfilter: PKFilter = PKFilter(), page_size: int = 2000) -> "PKData":
        """ Create a PKDBData representation and gets the data for the provided filters.
        If no filters are given the complete data is retrieved.

        :param pkfilter: Filter object to select subset of data, if no Filter is provided the complete data is returned
        :param page_size: number of entries per query
        """
        pkfilter = pkfilter.to_dict()
        parameters = {"format": "json", 'page_size': page_size}
        logger.warning("*** Querying data ***")
        return PKData(
            interventions=cls._get_subset("interventions_elastic",
                                          **{**parameters, **pkfilter.get("interventions", {})}),
            individuals=cls._get_subset("characteristica_individuals",
                                        **{**parameters, **pkfilter.get("individuals", {})}),
            groups=cls._get_subset("characteristica_groups",
                                   **{**parameters, **pkfilter.get("groups", {})}),
            outputs=cls._get_subset("output_intervention",
                                    **{**parameters, **pkfilter.get("outputs", {})}),
            timecourses=cls._get_subset("timecourse_intervention",
                                        **{**parameters, **pkfilter.get("timecourses", {})})
        )

    @classmethod
    def _get_subset(cls, name, **parameters):
        """

        :param name: name of the view
        :param parameters: query parameters
        :return:
        """
        if not name in [
            # FIXME: unify names
            "characteristica_individuals",  # individuals
            "characteristica_groups",  # groups
            "interventions_elastic",  # interventions FIXME: why plural
            "output_intervention",  # outputs
            "timecourse_intervention",  # timecourses

        ]:
            raise ValueError(f"{name} not supported")

        url = urlparse.urljoin(cls.URL_BASE, f'{name}/')
        return cls._get_data(url, cls._get_headers(), **parameters)

    @classmethod
    def _get_login_token(cls):
        url = f"{cls.PKDB_URL}/api-token-auth/"
        payload = {'username': cls.PKDB_USERNAME, 'password': cls.PKDB_PASSWORD}
        response = requests.post(url, data=payload)
        return response.json().get("token")

    @classmethod
    def _get_headers(cls):
        token = cls._get_login_token()
        headers = {'Authorization': f'Token {token}'}
        return headers

    @staticmethod
    def _get_data(url, headers, **parameters) -> pd.DataFrame:
        """Gets data from a paginated rest API."""
        url_params = "?" + urlparse.urlencode(parameters)
        actual_url = urlparse.urljoin(url, url_params)
        logger.warning(actual_url)

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
            logger.warning(url_current)

            response = requests.get(url_current, headers=headers)
            data += response.json()["data"]["data"]

        # convert to data frame
        df = pd.DataFrame(data)

        # convert columns to float columns
        float_columns = [
            "mean",
            "median",
            "value",
            "sd",
            "se",
            "cv",
            "min",
            "max",
            "time"
        ]
        if "timecourse" not in url:
            for column in float_columns:
                if column in df.columns:
                    df[column] = df[column].astype(float)
        else:
            # every element must be converted individually
            for column in float_columns:
                if column in df:
                    col_loc = df.columns.get_loc(column)
                    for k in range(len(df)):
                        value = df.iloc[k, col_loc]
                        if value is not None:
                            df.at[k, column] = np.array(value).astype(float)

        # convert columns to int columns
        int_columns = [
            "timecourse_pk",
            "intervention_pk",
            "group_pk",
            "individual_pk",
            "group_parent_pk",
            "raw_pk",
        ]
        for column in int_columns:
            if column in df.columns:
                df[column] = df[column].replace({pd.np.nan: -1}).astype(int)

        return df