"""
Functions for working with PKDB data.

* TODO: consistent naming of endpoints
* FIXME: unclear what is modifying and what is copying the data frames
"""

import numpy as np
import pandas as pd

from copy import copy
import logging
from collections import OrderedDict
from typing import List

logger = logging.getLogger(__name__)


class PKDataFrame(pd.DataFrame):
    """
    Extended Dataframe which support customized filter operations.
    Used to encode groups, individuals, interventions, outputs, timecourses on PKData.
    """
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

    @staticmethod
    def _validate_not_in_columns(columns):
        if columns:
            assert 'pk' in columns

    def pk_filter(self, f_idx) -> 'PKDataFrame':
        """

        :param f_idx: function, index, list
        :return:
        """
        if isinstance(f_idx, list):
            pk_df = self
            for f_idx_single in f_idx:
                pk_df = pk_df.pk_filter(f_idx_single)
            return pk_df

        df_pks = self[f_idx][self.pk].unique()
        df_filtered = self[self[self.pk].isin(df_pks)]
        return PKDataFrame(df_filtered, pk=self.pk)

    def pk_exclude(self, f_idx) -> 'PKDataFrame':
        if isinstance(f_idx, list):
            pk_df = self
            for f_idx_single in f_idx:
                pk_df = pk_df.pk_exclude(f_idx_single)
            return pk_df

        df_pks = self[f_idx][self.pk].unique()
        df_excluded = self[~self[self.pk].isin(df_pks)]
        return PKDataFrame(df_excluded, pk=self.pk)

    @property
    def pk_column(self):
        return self[self.pk]

    @property
    def pks(self) -> set:
        """ Set of pks."""
        return set(self[self.pk].unique())

    @property
    def pk_len(self) -> int:
        return len(self.pks)

    @property
    def df(self) -> pd.DataFrame:
        """ Returns a copied DataFrame."""
        df = self.copy()
        del df.pk
        return pd.DataFrame(self)

    @property
    def study_sids(self) -> set:
        """ Set of study_sids."""
        return set(self.study_sid.unique())

    def _emptify(self) -> 'PKDataFrame':
        empty_df = pd.DataFrame([], columns=self.columns)
        return PKDataFrame(empty_df, pk=self.pk)


class PKData(object):
    """ Consistent set of data from PK-DB.

    Information is stored as DataFrames.

    Handles:

    - groups
    - individuals
    - interventions
    - outputs
    - timecourses
    """
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
        return {df_key: getattr(self, df_key).df for df_key in PKData.KEYS}

    def as_dict(self):
        return self.__dict___()

    def copy(self):
        return PKData(**self.as_dict())

    def __str__(self):
        """ Overview of content.

        :return:
        """
        lines = [
            "-" * 30, f"{self.__class__.__name__} ({id(self)})",
            "-" * 30,
            f"{'studies':<15} {len(self.study_sids):>5} "
        ]

        for key in self.KEYS:
            df = getattr(self, key)
            nrows = len(df)
            count = df.pk_len

            lines.append(f"{key:<15} {count:>5}  ({nrows:>5})")
        lines.append("-" * 30)
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
    def from_hdf5(path):
        """ Load data from HDF5 serialization.

        :param path:
        :return:
        """
        store = pd.HDFStore(path)
        data_dict = {}
        for key in store.keys():
            # ugly bugfix due to hdf5 key mutation (key -> /key on storage)
            data_dict[key[1:]] = store[key]
        store.close()

        return PKData(**data_dict)

    def to_hdf5(self, path):
        """ Store data as HDF5 serialization. """
        store = pd.HDFStore(path)
        for key in ["interventions", "individuals", "groups", "outputs", "timecourses"]:
            df = getattr(self, key).df
            store[key] = df
        store.close()

    @property
    def study_sids(self) -> set:
        """Set of study_sids used in data."""
        study_sids = set()
        for df_key in PKData.KEYS:
            pk_df = getattr(self, df_key)
            study_sids = study_sids.union(pk_df.study_sids)

        return study_sids

    @property
    def groups_count(self) -> int:
        """Number of groups."""
        return self.groups.pk_len

    @property
    def individuals_count(self) -> int:
        """Number of individuals."""
        return self.individuals.pk_len

    @property
    def interventions_count(self) -> int:
        """Number of interventions."""
        return self.interventions.pk_len

    @property
    def outputs_count(self) -> int:
        """Number of outputs."""
        return self.outputs.pk_len

    @property
    def timecourses_count(self) -> int:
        """Number of timecourses."""
        return self.timecourses.pk_len

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

    # --- filter and exclude ---

    def _pk_filter(self, df_k, f_idx, concise):
        dict_pkdata = self.as_dict()
        dict_pkdata[df_k] = getattr(self, df_k).pk_filter(f_idx)

        pkdata = PKData(**dict_pkdata)
        if concise:
            pkdata._concise()
        return pkdata

    def _pk_exclude(self, df_k, f_idx, concise):
        dict_pkdata = self.as_dict()
        dict_pkdata[df_k] = getattr(self, df_k).pk_exclude(f_idx)

        pkdata = PKData(**dict_pkdata)
        if concise:
            pkdata._concise()
        return pkdata

    def _emptify(self, df_key, concise=True) -> 'PKData':
        self._validate_df_key(df_key)

        dict_pkdata = self.as_dict()
        dict_pkdata[df_key] = getattr(self, df_key)._emptify()

        pkdata = PKData(**dict_pkdata)
        if concise:
            pkdata._concise()
        return pkdata

    @staticmethod
    def _validate_df_key(df_key):
        if df_key not in PKData.KEYS:
            raise ValueError(f"Unsupported key '{df_key}', key must be in '{PKData.KEYS}'")

    def filter_intervention(self, f_idx, concise=True):
        """ Filter interventions. """
        return self._pk_filter("interventions", f_idx, concise)

    def filter_group(self, f_idx, concise=True):
        """ Filter groups. """
        return self._pk_filter("groups", f_idx, concise)

    def filter_individual(self, f_idx, concise=True):
        """ Filter individuals. """
        return self._pk_filter("individuals", f_idx, concise)

    def filter_subject(self, f_idx, concise=True):
        """ Filter group or individual. """
        pkdata = self.filter_group(f_idx, concise=False)
        pkdata.filter_individual(f_idx, concise=False)
        if concise:
            pkdata._concise()
        return pkdata

    def filter_output(self, f_idx, concise=True):
        """ Filter outputs. """
        return self._pk_filter("outputs", f_idx, concise)

    def filter_timecourse(self, f_idx, concise=True):
        """ Filter timecourses. """
        return self._pk_filter("timecourses", f_idx, concise)

    def exclude_intervention(self, f_idx, concise=True):
        return self._pk_exclude("interventions", f_idx, concise)

    def exclude_group(self, f_idx, concise=True):
        return self._pk_exclude("groups", f_idx, concise)

    def exclude_individual(self, f_idx, concise=True):
        return self._pk_exclude("individuals", f_idx, concise)

    def exclude_subject(self, f_idx, concise=True):
        pkdata = self.exclude_group(f_idx, concise=False)
        pkdata = pkdata.exclude_individual(f_idx, concise=False)
        if concise:
            pkdata._concise()
        return pkdata

    def exclude_output(self, f_idx, concise=True):
        return self._pk_exclude("outputs", f_idx, concise)

    def exclude_timecourse(self, f_idx, concise=True):
        return self._pk_exclude("timecourses", f_idx, concise)

    def delete_outputs(self, concise=True):
        """Deletes outputs."""
        return self._emptify("outputs", concise=concise)

    def delete_timecourses(self, concise=True):
        """Deletes timecourses."""
        return self._emptify("timecourses", concise=concise)

    def _concise(self) -> None:
        """ Reduces the current PKData to a consistent subset.
        Modifies the DataFrame in place.
        :return:
        """
        previous_len = np.inf
        logger.warning("Concise DataFrames")
        while previous_len > self._len_total:
            previous_len = copy(self._len_total)

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
                df = getattr(self, df_key)
                setattr(self, df_key, df[df["individual_pk"].isin(current_individual_pks)])

            # concise based on groups
            outputs_group_pks = set(self.outputs.group_pk)
            timecourses_group_pks = set(self.timecourses.group_pk)

            current_group_pks = (self.groups.pks.intersection(outputs_group_pks)) or \
                                (self.groups.pks.intersection(timecourses_group_pks))

            current_group_pks.add(-1)

            for df_key in ["groups", "timecourses", "outputs"]:
                df = getattr(self, df_key)
                setattr(self, df_key, df[df.group_pk.isin(current_group_pks)])

    @property
    def _len_total(self):
        return sum([len(getattr(self, df_key)) for df_key in PKData.KEYS])


    def get_choices(self):
        """ This is experimental.
        returns choices

        :return:
        """
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
        if key is None:
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
