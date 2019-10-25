"""
Functions for working with PKDB data.

# TODO: Fix the columns data type, use basic data types for everything
# TODO: study endpoint and add to PKDBData
# TODO: reorder fields in order of importance
# TODO: consistent naming of endpoints
# TODO: consistent naming of fields, e.g. pk, study_sid
# TODO: split groups and individuals (?!)
"""
from json import JSONDecodeError

import numpy as np
import requests
import pandas as pd
from urllib import parse as urlparse
from copy import copy
import logging
from collections import OrderedDict

from pkdb_analysis.pkfilter import PKFilter

class PKData(object):
    """ Abstraction of subset of pkdb data.
    """
    PKDB_URL = "http://0.0.0.0:8000"
    PKDB_USERNAME = "admin"
    PKDB_PASSWORD = "pkdb_admin"
    URL_BASE = urlparse.urljoin(PKDB_URL, '/api/v1/')

    KEYS = ["individuals", "groups", "interventions", "outputs", "timecourses"]
    PK_COLUMNS = {
        "interventions": "pk",
        "individuals": "individual_pk",
        "groups": "group_pk",
        "outputs": "output_pk",
        "timecourses": "timecourse_pk"
        }

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

        if not self.individuals.empty:
            self.individuals.substance = self.individuals.substance.astype(str)
        if not self.groups.empty:
            self.groups.substance = self.individuals.substance.astype(str)

        self.choices = self.get_choices()

    def __str__(self):
        """ Overview of content.

        :return:
        """
        lines = [str(type(self))]
        for key in self.KEYS:
            lines.append(f"\t{key}: {len(getattr(self, key))}")
        return "\n".join(lines)

    def __or__(self, other: 'PKData') -> 'PKData':
        """ combines two PKData instances
        :param other: other PkData instance
        :return: PKData
        """

        resulting_kwargs = dict()

        for df_key in self.KEYS:
            df = getattr(self, df_key)
            other_df = getattr(other, df_key)
            resulting_df = df.append(other_df)
            resulting_df = resulting_df.loc[~resulting_df.index.duplicated(keep='first')]

            resulting_kwargs[df_key] = resulting_df


        return PKData(**resulting_kwargs)

    def __and__(self, other: 'PKData') -> 'PKData':
        """ combines instances were instances have to

        param other: other PkData instance
        :return: PKData
        """

        resulting_kwargs = dict()
        for df_key in PKData.KEYS:
            df = getattr(self,df_key)
            other_df = getattr(other,df_key)

            pk = PKData.PK_COLUMNS
            pks = set(df[pk])
            other_pks =  set(other_df[pk])

            intersection_pks = pks.intersection(other_pks)
            df = df[df[pk].isin(intersection_pks)]
            other_df = other_df[other_df[pk].isin(intersection_pks)]

            resulting_df = df.append(other_df)
            resulting_df = resulting_df.loc[~resulting_df.index.duplicated(keep='first')]
            resulting_kwargs[df_key] = resulting_df

        return PKData(**resulting_kwargs)


    @staticmethod
    def _validate_df_key(df_key):
        if df_key not in PKData.KEYS:
            raise ValueError(f"Unsupported key '{df_key}', key must be in '{PKData.KEYS}'")

    @property
    def _len(self):
        return sum([len(getattr(self, df_key)) for df_key in PKData.KEYS])


    def _concise(self):
        previous_len = np.inf
        logging.warning("Consice DataFrames")
        while previous_len > self._len:
            previous_len = copy(self._len)

            # concise based on interventions
            intervention_pks = set(self.interventions["pk"])
            outputs_intervention_pks = set(self.outputs["intervention_pk"])
            timecourses_intervention_pks = set(self.timecourses["intervention_pk"])

            current_intervention_pks = (intervention_pks.intersection(outputs_intervention_pks)) or \
                                       (intervention_pks.intersection(timecourses_intervention_pks))

            self.interventions = self.interventions[self.interventions["pk"].isin(current_intervention_pks)]
            self.timecourses = self.timecourses[self.timecourses["intervention_pk"].isin(current_intervention_pks)]
            self.outputs = self.outputs[self.outputs["intervention_pk"].isin(current_intervention_pks)]

            # concise based on individuals
            individual_pks = set(self.individuals["individual_pk"])
            outputs_individual_pks = set(self.outputs["individual_pk"])
            timecourses_individual_pks = set(self.timecourses["individual_pk"])

            current_individual_pks = (individual_pks.intersection(outputs_individual_pks)) or \
                                     (individual_pks.intersection(timecourses_individual_pks))
            current_individual_pks.add(-1)

            for df_key in ["individuals", "timecourses", "outputs"]:
                df = getattr(self,df_key)
                setattr(self, df_key, df[df["individual_pk"].isin(current_individual_pks)])

            # concise based on groups
            group_pks = set(self.groups["group_pk"])
            outputs_group_pks = set(self.outputs["group_pk"])
            timecourses_group_pks = set(self.timecourses["group_pk"])

            current_group_pks = (group_pks.intersection(outputs_group_pks)) or \
                                (group_pks.intersection(timecourses_group_pks))

            current_group_pks.add(-1)

            for df_key in ["groups", "timecourses", "outputs"]:
                df = getattr(self,df_key)
                setattr(self, df_key, df[df["group_pk"].isin(current_group_pks)])


    def get_choices(self):
        """ This is experimental.
        returns choices

        :return:
        """
        logging.warning("Calculating choices")
        all_choices = OrderedDict()
        for df_key in self.KEYS:
            df = getattr(self, df_key)
            choices = OrderedDict()
            for key in df.columns:
                if df[key].dtype in ['bool', 'object']:
                    if df_key == "timecourses":
                        if key in ["time", "value", "mean", "median", "sd", "se", "min", "max", "cv"]:
                            continue

                    # remove None so sorting is working
                    values = [c for c in df[key].unique() if c is not None]
                    choices[key] = sorted(values)

            all_choices[df_key] = choices
        return all_choices

    def print_choices(self, key=None, field=None):
        """ Prints the choices

        :param key: key of dataframe
        :param field: header field
        :return:
        """
        if key == None:
            df_keys = PKData.KEYS
        else:
            self._validate_df_key(key)
            df_keys = [key]

        all_choices = self.choices
        for df_key in df_keys:
            choices = all_choices[df_key]
            if field is not None:
                if field not in choices.keys():
                    raise ValueError(f"Unsupported field '{field}', field must be in '{choices.keys()}'")
                fields = [field]
            else:
                fields = choices.keys()

            for field in fields:
                print(f"*** {field} ***")
                print(choices[field])

    @staticmethod
    def _from_db(pkfilter: PKFilter = PKFilter(), page_size: int = 2000) -> "PKData":

        pkfilter = pkfilter.to_dict()
        parameters = {"format": "json", 'page_size': page_size}
        logging.warning("*** Querying data ***")
        return PKData(
            interventions=PKData._get_subset("interventions_elastic",
                                             **{**parameters, **pkfilter.get("interventions", {})}),
            individuals=PKData._get_subset("characteristica_individuals",
                                           **{**parameters, **pkfilter.get("individuals", {})}),
            groups=PKData._get_subset("characteristica_groups", **{**parameters, **pkfilter.get("groups", {})}),
            outputs=PKData._get_subset("output_intervention", **{**parameters, **pkfilter.get("outputs", {})}),
            timecourses=PKData._get_subset("timecourse_intervention",
                                           **{**parameters, **pkfilter.get("timecourses", {})})
        )

    def _from_db_missing(self) -> "PKData":
        """
        Each DataFrame of PKData has a pk column (e.g. groups -> group_pk). The value on the pk column must not be unique
        on each row. Hence, the database may contain further rows with same value in the pk_column (e.g. each row of the
        groups DataFrame contains a characteristica related to a group_pk. The database maybe contain further
        characteristica for the same group_pks which are in the groups DataFrame). This functions queries all missing
        related rows.
        :return: PKData instance
        """
        pkfilter = PKFilter()

        for df_key, pk in PKData.PK_COLUMNS.items():
            df = getattr(self, df_key)
            pks_url = "__".join([str(pk) for pk in df[pk].unique()])

            key_filter = getattr(pkfilter, df_key)
            key_filter[f"{pk}__in"] = pks_url

        return PKData._from_db(pkfilter)


    @staticmethod
    def from_db(pkfilter: PKFilter = PKFilter(), page_size: int = 2000) -> "PKData":
        """ Create a PKDBData representation and gets the data for the provided filters.
        If no filters are given the complete data is retrieved.

        :param pkfilter: Filter object to select subset of data, if no Filter is provided the complete data is returned
        :param page_size: number of entries per query
        """
        pkdata = PKData._from_db(pkfilter, page_size)
        pkdata._concise()
        return pkdata._from_db_missing()




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

        return PKData(**data_dict)

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
        try:
            response.raise_for_status()
            num_pages = response.json()["last_page"]

        except requests.exceptions.HTTPError as err:
            raise err

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
    data = PKData.from_db()
    h5_path = Path("../results/") / "test.h5"

    data.to_hdf5(h5_path)
    data2 = PKData.from_hdf5(h5_path)
