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
from copy import copy, deepcopy
import logging
from collections import OrderedDict
from typing import List


from pkdb_analysis.pkfilter import PKFilter

import pandas as pd

class PKDataFrame(pd.DataFrame):

    @property
    def _constructor(self):
        return PKDataFrame._internal_ctor

    _metadata = ['pk']

    @classmethod
    def _internal_ctor(cls, *args, **kwargs):
        kwargs['pk'] = None
        return cls(*args, **kwargs)

    def __init__(self, data, pk=None, index=None, columns=None, dtype=None, copy=True):
        if not isinstance(data, pd.core.internals.BlockManager) and not pk:
            raise ValueError("arg pk required")

        super(PKDataFrame, self).__init__(data=data,
                                      index=index,
                                      columns=columns,
                                      dtype=dtype,
                                      copy=copy)
        self.pk = pk

        #self._validate_not_in_columns(columns)



    @staticmethod
    def _validate_not_in_columns(columns):
        if columns:
            assert 'pk' in columns

    def pk_filter(self, f_idx) -> 'PKDataFrame':
        df_pks = self[f_idx][self.pk].unique()
        df_filtered = self[self[self.pk].isin(df_pks)]
        return PKDataFrame(df_filtered, pk=self.pk)

    @property
    def pk_column(self):
        return self[self.pk]

    @property
    def pks(self) -> set:
        return set(self[self.pk].unique())

    @property
    def pk_len(self) -> int:
        return len(self.pks)

    @property
    def df(self):
        df = deepcopy(self)
        del df.pk
        return pd.DataFrame(self)



class PKData(object):
    """ Abstraction of subset of pkdb data.
    """
    PKDB_URL = "http://0.0.0.0:8000"
    PKDB_USERNAME = "admin"
    PKDB_PASSWORD = "pkdb_admin"
    URL_BASE = urlparse.urljoin(PKDB_URL, '/api/v1/')

    KEYS = ["groups", "individuals", "interventions", "outputs", "timecourses"]
    PK_COLUMNS = {key: f"{key[:-1]}_pk" for key in KEYS}

    def __init__(self,
                 interventions: pd.DataFrame = None,
                 groups: pd.DataFrame = None,
                 individuals: pd.DataFrame = None,
                 outputs: pd.DataFrame = None,
                 timecourses: pd.DataFrame = None
                 ):
        """ Creates PKDB data object from given DataFrames.

        :param interventions:
        :param individuals:
        :param groups:
        :param outputs:
        :param timecourses:
        """
        self.groups = PKDataFrame(groups, pk="group_pk")
        self.individuals = PKDataFrame(individuals, pk="individual_pk")
        self.interventions = PKDataFrame(interventions, pk="intervention_pk")
        self.outputs = PKDataFrame(outputs, pk="output_pk")
        self.timecourses = PKDataFrame(timecourses, pk="timecourse_pk")

        if not self.individuals.empty:
            self.individuals.substance = self.individuals.substance.astype(str)
        if not self.groups.empty:
            self.groups.substance = self.groups.substance.astype(str)

        self.choices = self.get_choices()

    def __dict___(self):
        return {df_key:getattr(self,df_key).df for df_key in PKData.KEYS}

    def as_dict(self):
        return self.__dict___()

    def __str__(self):
        """ Overview of content.

        :return:
        """
        lines = [
            "-" * 30,
            f"{self.__class__.__name__ } ({id(self)})",
            "-" * 30
        ]
        for key in self.KEYS:
            df = getattr(self, key)
            nrows = len(df)
            count = df.pk_len

            lines.append(f"{key:<15} {count:>5}  ({nrows:>5})")
        lines.append("-" * 30)
        return "\n".join(lines)

    @property
    def groups_count(self) -> int:
        return self.groups.pk_len

    @property
    def individuals_count(self) -> int:
        return self.individuals.pk_len

    @property
    def interventions_count(self) -> int:
        return self.interventions.pk_len

    @property
    def outputs_count(self) -> int:
        return self.outputs.pk_len

    @property
    def timecourses_count(self) -> int:
        return self.timecourses.pk_len

    @property
    def groups_pks(self) -> set:
        return self.groups.pks

    @property
    def individuals_pks(self) -> set:
        return self.individuals.pks

    @property
    def interventions_pks(self) -> set:
        return self.interventions.pks

    @property
    def outputs_pks(self) -> set:
        return self.outputs.pks

    @property
    def timecourses_pks(self) -> set:
        return self.timecourses.pks

    def intervention_pk_filter(self,f_idx, concise=True):
        dict_pkdata = self.as_dict()
        dict_pkdata["interventions"] = self.interventions.pk_filter(f_idx)
        pkdata  = PKData(**dict_pkdata)
        if concise:
            pkdata._concise()
        return pkdata


    def _df_mi(self, field: str, index_fields: List[str]) -> pd.DataFrame:
        """ Create multi-index DataFrame

        :param field:
        :param index_fields:
        :return:
        """
        df = getattr(self, field)
        if df.empty:
            return pd.DataFrame()  # new empty DataFrame
        # create multi-index DataFrame
        df_mi = df.sort_values(index_fields, ascending=True, inplace=False)
        df_mi.set_index(index_fields, inplace=True)
        return df_mi

    @property
    def groups_mi(self) -> pd.DataFrame:
        """ Multi-index data frame. """
        return self._df_mi('groups', ['group_pk', 'characteristica_pk'])

    @property
    def individuals_mi(self) -> pd.DataFrame:
        """ Multi-index data frame. """
        return self._df_mi('individuals', ['individual_pk', 'characteristica_pk'])

    @property
    def interventions_mi(self) -> pd.DataFrame:
        """ Multi-index data frame. """
        return self._df_mi('interventions', ['intervention_pk'])

    @property
    def outputs_mi(self) -> pd.DataFrame:
        """ Multi-index data frame. """
        return self._df_mi('outputs',
                           ['output_pk', 'intervention_pk', 'group_pk', 'individual_pk'])

    @property
    def timecourses_mi(self) -> pd.DataFrame:
        """ Multi-index data frame. """
        return self._df_mi('timecourses',
                           ['timecourse_pk', 'intervention_pk', 'group_pk', 'individual_pk'])


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
            df = getattr(self, df_key)
            other_df = getattr(other, df_key)

            pk = PKData.PK_COLUMNS
            pks = set(df[pk])
            other_pks = set(other_df[pk])

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
            outputs_intervention_pks = set(self.outputs.intervention_pk)
            timecourses_intervention_pks = set(self.timecourses.intervention_pk)

            current_intervention_pks = (self.interventions.pks.intersection(outputs_intervention_pks)) or \
                                       (self.interventions.pks.intersection(timecourses_intervention_pks))

            self.interventions = self.interventions[self.interventions.intervention_pk.isin(current_intervention_pks)]
            self.timecourses = self.timecourses[self.timecourses.intervention_pk.isin(current_intervention_pks)]
            self.outputs = self.outputs[self.outputs.intervention_pk.isin(current_intervention_pks)]

            # concise based on individuals
            outputs_individual_pks = set(self.outputs.individual_pk)
            timecourses_individual_pks = set(self.timecourses.individual_pk)

            current_individual_pks = (self.individuals.pks.intersection(outputs_individual_pks)) or \
                                     (self.individuals.pks.intersection(timecourses_individual_pks))
            current_individual_pks.add(-1)

            for df_key in ["individuals", "timecourses", "outputs"]:
                df = getattr(self,df_key)
                setattr(self, df_key, df[df["individual_pk"].isin(current_individual_pks)])

            # concise based on groups
            outputs_group_pks = set(self.outputs.group_pk)
            timecourses_group_pks = set(self.timecourses.group_pk)

            current_group_pks = (self.groups.pks.intersection(outputs_group_pks)) or \
                                (self.groups.pks.intersection(timecourses_group_pks))

            current_group_pks.add(-1)

            for df_key in ["groups", "timecourses", "outputs"]:
                df = getattr(self,df_key)
                setattr(self, df_key, df[df.group_pk.isin(current_group_pks)])


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
            PKData._validate_df_key(key)
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


    @staticmethod
    def from_db(pkfilter: PKFilter = PKFilter(), page_size: int = 2000) -> "PKData":
        """ Create a PKDBData representation and gets the data for the provided filters.
        If no filters are given the complete data is retrieved.

        :param pkfilter: Filter object to select subset of data, if no Filter is provided the complete data is returned
        :param page_size: number of entries per query
        """
        pkdata = PKData._from_db(pkfilter, page_size)
        #pkdata._concise()
        #pkdata = pkdata._from_db_missing()
        return pkdata


    def filter_by_f_idx(self,df_key,f_idx, concise=True):
        """

        :param key:
        :param f_idx:
        :return:
        """

        PKData._validate_df_key(df_key)
        pk_key = PKData.PK_COLUMNS[df_key]
        pkdata = deepcopy(self)

        df = getattr(pkdata,df_key)
        df_pks = df[f_idx][pk_key].unique()
        df_filtered = df[df[pk_key].isin(df_pks)]
        setattr(pkdata,df_key,df_filtered)
        if concise:
            pkdata._concise()
        return pkdata



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
        for key in ["interventions", "individuals", "groups", "outputs", "timecourses"]:
            logging.warning(key)
            df = getattr(self, key).df
            store[key] = df
        store.close()

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
        """Gets data from a paginated rest API."""
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
                df[column] = df[column].replace({pd.np.nan:-1}).astype(int)

        return df


if __name__ == "__main__":
    from pathlib import Path
    data = PKData.from_db()
    h5_path = Path("../results/") / "test.h5"

    data.to_hdf5(h5_path)
    data2 = PKData.from_hdf5(h5_path)
