"""
Querying PK-DB
"""
import logging
import os
from copy import deepcopy
from urllib import parse as urlparse

import numpy as np
import pandas as pd
import requests

from pkdb_analysis.data import PKData
from pkdb_analysis.envs import USER, PASSWORD, API_URL, API_BASE

logger = logging.getLogger(__name__)


class PKFilter(object):
    """Filter objects for PKData"""
    KEYS = ['groups', 'individuals', "interventions", "outputs", "timecourses"]

    def __init__(self, normed=True):
        """ Create new Filter instance.

        :param normed: [True, False, None] return [normed data, unnormalized data,
                        normed and unnormalized data]
        """
        self.groups = dict()
        self.individuals = dict()
        self.interventions = dict()
        self.outputs = dict()
        self.timecourses = dict()
        self.studies = dict()


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

    @classmethod
    def query(cls, pkfilter: PKFilter = PKFilter(), page_size: int = 2000) -> "PKData":
        """ Create a PKData representation and gets the data for the provided filters.
        If no filters are given the complete data is retrieved.

        :param pkfilter: Filter object to select subset of data, if no Filter is provided the complete data is returned
        :param page_size: number of entries per query
        """
        pkfilter = pkfilter.to_dict()
        parameters = {"format": "json", 'page_size': page_size}
        logger.info("*** Querying data ***")
        pkdata = PKData(
            studies=cls._get_subset("studies", **{**parameters, **pkfilter.get("studies", {})}),
            interventions=cls._get_subset("interventions_analysis", **{**parameters, **pkfilter.get("interventions", {})}),
            individuals=cls._get_subset("individuals_analysis",
                                        **{**parameters, **pkfilter.get("individuals", {})}),
            groups=cls._get_subset("groups_analysis",
                                   **{**parameters, **pkfilter.get("groups", {})}),
            outputs=cls._get_subset("output_analysis",
                                    **{**parameters, **pkfilter.get("outputs", {})}),
            timecourses=cls._get_subset("timecourse_analysis",
                                        **{**parameters, **pkfilter.get("timecourses", {})})
        )

        return cls._intervention_pk_update(pkdata)

    @classmethod
    def _get_subset(cls, name, **parameters):
        """

        :param name: name of the view
        :param parameters: query parameters
        :return:
        """
        if not name in [
            "individuals_analysis",  # individuals
            "groups_analysis",  # groups
            "interventions_analysis",  # interventions
            "output_analysis",  # outputs
            "timecourse_analysis",  # timecourses
            "studies",  # studies

        ]:
            raise ValueError(f"{name} not supported")

        url = API_URL + f'/{name}/'
        return cls._get_data(url, cls.get_authentication_headers(API_BASE, USER, PASSWORD), **parameters)

    @classmethod
    def get_authentication_headers(cls, api_base, username, password):
        """ Get authentication header with token for given user.

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
                f"Error Connecting (probably wrong url <{api_base}>): ", e)

        if response.status_code != 200:
            logger.error(f"Request headers could not be retrieved from: {auth_token_url}")
            logger.warning(response.text)
            raise requests.exceptions.ConnectionError(response)

        token = response.json().get("token")
        return {'Authorization': f'token {token}'}

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

        if "timecourse" in url:
            # every element must be converted individually
            for column in float_columns:
                if column in df:
                    col_loc = df.columns.get_loc(column)
                    for k in range(len(df)):
                        value = df.iloc[k, col_loc]
                        if value is not None:
                            df.at[k, column] = np.array(value).astype(float)
        else:
            for column in float_columns:
                if column in df.columns:
                    df[column] = df[column].astype(float)

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
                df[column] = df[column].replace({np.nan: -1}).astype(int)

        return df

    @staticmethod
    def _map_intervention_pks(pkdata):
        interventions_output = pd.DataFrame()
        interventions_timecourse = pd.DataFrame()

        if not pkdata.outputs.empty :
            interventions_output = pkdata.outputs.df.pivot_table(values="intervention_pk", index="output_pk",
                                                             aggfunc=lambda x: frozenset(x))
        if not pkdata.timecourses.empty:
            interventions_timecourse = pkdata.timecourses.df.pivot_table(values="intervention_pk", index="timecourse_pk",
                                                                     aggfunc=lambda x: frozenset(x))

        interventions = interventions_output.append(interventions_timecourse).drop_duplicates(
            "intervention_pk").reset_index()
        interventions.index = interventions.index.set_names(['intervention_pk_updated'])

        return interventions["intervention_pk"].reset_index()

    @staticmethod
    def _update_interventions(pkdata, mapping_int_pks):
        mapping_int_pks = mapping_int_pks.copy()
        mapping_int_pks["intervention_pk"] = mapping_int_pks.intervention_pk.apply(lambda x: list(x))
        mapping_int_pks = mapping_int_pks.intervention_pk.apply(pd.Series).stack().reset_index(level=-1,
                                                                                               drop=True).astype(
            int).reset_index()
        mapping_int_pks = mapping_int_pks.rename(columns={"index": "intervention_pk_updated", 0: "intervention_pk"})
        return pd.merge(mapping_int_pks, pkdata.interventions, on="intervention_pk").drop(
            columns=["intervention_pk"]).rename(columns={"intervention_pk_updated": "intervention_pk"})

    @staticmethod
    def _update_outputs(pkdata, mapping_int_pks):
        mapping_int_pks = mapping_int_pks.copy()

        interventions_output = pkdata.outputs.df.pivot_table(values="intervention_pk", index="output_pk",
                                                             aggfunc=lambda x: frozenset(x))
        mapping_int_pks = pd.merge(interventions_output.reset_index(), mapping_int_pks, on="intervention_pk",how="left" )[
            ["output_pk", "intervention_pk_updated"]]

        return pd.merge(mapping_int_pks, pkdata.outputs.df.drop_duplicates(subset="output_pk") ,how='left').drop(columns=["intervention_pk"]).rename(
            columns={"intervention_pk_updated": "intervention_pk"})

    @staticmethod
    def _update_timecourses(pkdata, mapping_int_pks):
        mapping_int_pks = mapping_int_pks.copy()
        interventions_timecourse = pkdata.timecourses.df.pivot_table(values="intervention_pk", index="timecourse_pk",
                                                                     aggfunc=lambda x: frozenset(x))
        mapping_int_pks = pd.merge(interventions_timecourse.reset_index(), mapping_int_pks, on="intervention_pk",how="left")[
            ["timecourse_pk", "intervention_pk_updated"]]
        result = pd.merge(mapping_int_pks, pkdata.timecourses.df.drop_duplicates(subset="timecourse_pk"), how='left').drop(columns=["intervention_pk"]).rename(
            columns={"intervention_pk_updated": "intervention_pk"})

        return result

    @classmethod
    def _intervention_pk_update(cls, pkdata):
        if not pkdata.outputs.empty or not pkdata.timecourses.empty:
            mapping_int_pks = cls._map_intervention_pks(pkdata)

            data_dict = pkdata.as_dict()
            data_dict["interventions"] = cls._update_interventions(pkdata, mapping_int_pks)
            if not pkdata.outputs.empty:
                data_dict["outputs"] = cls._update_outputs(pkdata, mapping_int_pks)
            if not pkdata.timecourses.empty:
                data_dict["timecourses"] = cls._update_timecourses(pkdata, mapping_int_pks)

            return PKData(**data_dict)
        else:
            return pkdata
