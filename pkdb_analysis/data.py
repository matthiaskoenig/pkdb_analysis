"""
Functions for working with PKDB data.

# TODO: Fix the columns data type, use basic data types for everything
# TODO: study endpoint and add to PKDBData
# TODO: reorder fields in order of importance
# TODO: consistent naming of endpoints
# TODO: consistent naming of fields, e.g. pk, study_sid
# TODO: split groups and individuals (?!)
"""
import requests
import pandas as pd
from urllib import parse as urlparse
from typing import List, Dict
import logging


class PKDBFilter(object):
    # TODO: general filtering of datasets
    pass


class PKDBData(object):
    """ Abstraction of subset of pkdb data.
    """
    PKDB_URL = "http://0.0.0.0:8000"
    PKDB_USERNAME = "admin"
    PKDB_PASSWORD = "pkdb_admin"
    URL_BASE = urlparse.urljoin(PKDB_URL, '/api/v1/')

    def __init__(self,
                 studies: pd.DataFrame = None,
                 interventions: pd.DataFrame = None,
                 groups: pd.DataFrame = None,
                 individuals: pd.DataFrame = None,
                 outputs: pd.DataFrame = None,
                 timecourses: pd.DataFrame = None
                 ):
        """ Creates PKDB data object from given DataFrames.

        :param studies:
        :param interventions:
        :param individuals:
        :param groups:
        :param outputs:
        :param timecourses:
        """
        self.studies = studies
        self.interventions = interventions
        self.individuals = individuals
        self.groups = groups
        self.outputs = outputs
        self.timecourses = timecourses

    def __str__(self):
        return type(self)

    @staticmethod
    def from_db(filters: Dict[str, Dict[str,str]] = None, page_size: int = 2000):
        """ Create a PKDBData representation and gets the data for the provided filters.
        If no filters are given the complete data is retrieved.

        :param pkdb_url:
        :param page_size:
        """
        #if filters is not None:
        #    for key in ["interventions", "individuals", "groups", "outputs", "timecourses"]:
        #        keyfilters.get(key, {})
        #    # TODO: implement filters on creation (see filters below)
        #    raise NotImplementedError("Filters are not supported yet.")

        parameters = {"format": "json", 'page_size': page_size}
        logging.warning("*** Querying data ***")
        return PKDBData(
            #studies = None,  # FIXME
            interventions = PKDBData._get_subset("interventions_elastic", **{**parameters,**filters.get("interventions",{})}),
            individuals=PKDBData._get_subset("characteristica_individuals", **{**parameters,**filters.get("individuals",{})}),
            groups=PKDBData._get_subset("characteristica_groups", **{**parameters,**filters.get("groups",{})}),
            outputs = PKDBData._get_subset("output_intervention", **{**parameters,**filters.get("outputs",{})}),
            timecourses = PKDBData._get_subset("timecourse_intervention", **{**parameters,**filters.get("timecourses",{})})
        )

    @staticmethod
    def from_hdf5(path):
        """ Load data from HDF5 serialization.

        :param path:
        :return:
        """
        store = pd.HDFStore(path)
        data_dict = {}
        for key in store.keys():
            logging.warning(key)
            # ugly bugfix due to hdf5 key mutation (key -> /key on storage)
            data_dict[key[1:]] = store[key]
        store.close()

        return PKDBData(**data_dict)

    def to_hdf5(self, path):
        """ Store data as HDF5 serialization. """
        store = pd.HDFStore(path)
        # FIXME studies
        for key in ["interventions", "individuals", "groups", "outputs", "timecourses"]:
            logging.warning(key)
            df = getattr(self, key)
            store[key] = df
        store.close()

    def combine(self) -> pd.DataFrame:
        """ Combines multiple PKDBData into a single PKData object based on given strategy

        strategies:
            union
            diff
            ...

        """

        # TODO: implement


        raise NotImplementedError


    def reduce_dfs(self) -> pd.DataFrame:
        """ Reduces all dataframes in a single dataframe based on merging pks.
        ! Make sure right kind of join

        :return:
        """
        # TODO: implement
        raise NotImplementedError

    @classmethod
    def _get_subset(cls, name, **parameters):
        """

        :param name: name of the view
        :param parameters: query parameters
        :return:
        """
        if not name in [
            # FIXME: unify names
            # "studies_elastic",  # studies FIXME: not working
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
        """
        gets the data from a paginated rest api.
        """
        url_params = "?" + urlparse.urlencode(parameters)
        actual_url = urlparse.urljoin(url, url_params)
        logging.warning(actual_url)

        # FIXME: make first request fast
        response = requests.get(actual_url, headers=headers)
        num_pages = response.json()["last_page"]

        data = []
        for page in range(1, num_pages + 1):
            url_current = actual_url + f"&page={page}"
            logging.warning(url_current)

            response = requests.get(url_current,headers=headers)
            data += response.json()["data"]["data"]

        df = pd.DataFrame(data)

        # convert columns to float columns
        if "timecourse" not in url:
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
            for column in float_columns:
                if column in df.columns:
                    df[column] = df[column].astype(float)

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
                df[column] = df[column].replace({pd.np.nan:-1}).astype(int)

        return df

if __name__ == "__main__":
    from pathlib import Path
    data = PKDBData.from_db()
    h5_path = Path("../results/") / "test.h5"

    data.to_hdf5(h5_path)
    data2 = PKDBData.from_hdf5(h5_path)