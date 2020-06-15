"""
Functions for working with PKDB data.

* FIXME: specify which methods modify or copy data frames
"""
import logging
from pathlib import Path
from abc import ABC
from collections import OrderedDict
from copy import copy
from typing import List, Callable

import numpy as np
import pandas as pd
import warnings
from pandas.errors import PerformanceWarning
from IPython.display import display

warnings.simplefilter(action='ignore', category=PerformanceWarning)
logger = logging.getLogger(__name__)


class PKDataFrame(pd.DataFrame, ABC):
    """
    Extended DataFrame which support customized filter operations.
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
        """

        :param data:
        :param pk:
        :param index:
        :param columns:
        :param dtype:
        :param copy:
        """
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

    def pk_filter(self, f_idx: Callable, **kwargs) -> 'PKDataFrame':
        """

        :param f_idx: function, index, list
        :return:
        """

        def ff_idx(d):
            return f_idx(d, **kwargs)

        if isinstance(f_idx, list):

            pk_df = self
            for f_idx_single in f_idx:
                pk_df = pk_df.pk_filter(f_idx_single, **kwargs)
            return pk_df

        df_pks = self[ff_idx][self.pk].unique()
        df_filtered = self[self[self.pk].isin(df_pks)]
        return PKDataFrame(df_filtered, pk=self.pk)

    def pk_exclude(self, f_idx: Callable, **kwargs) -> 'PKDataFrame':

        def ff_idx(d):
            return f_idx(d, **kwargs)

        if isinstance(f_idx, list):
            pk_df = self
            for f_idx_single in f_idx:
                pk_df = pk_df.pk_exclude(f_idx_single, **kwargs)
            return pk_df

        df_pks = self[ff_idx][self.pk].unique()
        df_excluded = self[~self[self.pk].isin(df_pks)]
        return PKDataFrame(df_excluded, pk=self.pk)

    @property
    def pk_column(self):
        return self[self.pk]

    @property
    def pks(self) -> set:
        """ Set of pks."""
        if self.pk in self.df.columns:
            return set(self[self.pk].unique())
        else:
            return set()

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
        study_sids =  set([])
        if "study_sid" in self.df.columns:
            study_sids = set(self.study_sid.unique())
        return study_sids

    def _emptify(self) -> 'PKDataFrame':
        empty_df = pd.DataFrame([], columns=self.columns)
        return PKDataFrame(empty_df, pk=self.pk)

    def __str__(self):
        return self.df.__str__()

    def __repr__(self):
        return self.df.__repr__()

    def _repr_html_(self):
        return display(self.df)

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
    KEYS = ["studies", "groups", "individuals", "interventions", "outputs", "timecourses"]
    PK_COLUMNS = {key: f"{key[:-1]}_pk" for key in KEYS}

    def __init__(self,
                 interventions: pd.DataFrame = None,
                 groups: pd.DataFrame = None,
                 individuals: pd.DataFrame = None,
                 outputs: pd.DataFrame = None,
                 timecourses: pd.DataFrame = None,
                 studies: pd.DataFrame = None

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
        self.studies = PKDataFrame(studies, pk="sid")

        if not self.individuals.empty:
            self.individuals.substance = self.individuals.substance.astype(str)
        if not self.groups.empty:
            self.groups.substance = self.groups.substance.astype(str)

        #self.choices = self.get_choices() #TODO:not working with studies. Is this still important?

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

        param other: other PKData instance
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
    def from_hdf5(path: Path) -> 'PKData':
        """ Load data from HDF5 serialization.

        :param path: path to HDF5.
        :type path: str
        :return: PKData loaded from HDF5.
        :rtype: PKData
        """
        store = pd.HDFStore(path)
        data_dict = {}
        for key in store.keys():
            # ugly bugfix due to hdf5 key mutation (key -> /key on storage)
            data_dict[key[1:]] = store[key]
        store.close()

        return PKData(**data_dict)

    def to_hdf5(self, path: Path) -> None:
        """ Saves data HDF5

        :param path: path to HDF5.
        :type path: str
        """
        store = pd.HDFStore(path)
        for key in ["studies", "interventions", "individuals", "groups", "outputs", "timecourses"]:
            df = getattr(self, key).df
            store[key] = df
        store.close()

    @property
    def study_sids(self) -> set:
        """ Set of study sids contained in this PKData instance.

        :return: Study sids contained in this PKData instance.
        :rtype: set
        """
        study_sids = set()
        for df_key in PKData.KEYS:
            pk_df = getattr(self, df_key)
            study_sids = study_sids.union(pk_df.study_sids)

        return study_sids

    @property
    def groups_count(self) -> int:
        """ Number of groups contained in this PKData instance.

        :return: Number of groups contained in this PKData instance.
        :rtype: int
        """
        return self.groups.pk_len

    @property
    def individuals_count(self) -> int:
        """ Number of individuals contained in this PKData instance.

                :return: Number of individuals contained in this PKData instance.
                :rtype: int
        """
        return self.individuals.pk_len

    @property
    def interventions_count(self) -> int:
        """ Number of interventions contained in this PKData instance.

        :return: Number of interventions contained in this PKData instance.
        :rtype: int
        """
        return self.interventions.pk_len

    @property
    def outputs_count(self) -> int:
        """ Number of outputs contained in this PKData instance.

        :return: Number of outputs contained in this PKData instance.
        :rtype: int
        """
        return self.outputs.pk_len

    @property
    def timecourses_count(self) -> int:
        """ Number of timecourses contained in this PKData instance.

        :return: Number of timecourses contained in this PKData instance.
        :rtype: int
        """
        return self.timecourses.pk_len

    def _df_mi(self, field: str, index_fields: List[str]) -> pd.DataFrame:
        """ Create multi-index DataFrame

        :param field:  #fixme rename to df_key?
        :param index_fields:
        :return: Multi-indexed Dataframe
        :rtype: pd.DataFrame
        """
        df = getattr(self, field)
        if df.empty:
            return pd.DataFrame()  # new empty DataFrame
        # create multi-index DataFrame
        df_mi = df.sort_values(index_fields, ascending=True, inplace=False)
        df_mi.set_index(index_fields, inplace=True)
        return df_mi

    def _df_core(self, field: str, core_fields: List[str]) -> PKDataFrame:
        """  Core group information with unique pk per row
        """

        pk_df = getattr(self, field)
        return pk_df.pivot_table(index=pk_df.pk, values=core_fields, aggfunc=lambda x: x.iloc[0]).reset_index()



    @property
    def groups_mi(self) -> pd.DataFrame:
        """Multi-index DataFrame of groups contained in this PKData instance.

        :return: Multi-indexed DataFrame of groups contained in this PKData instance.
        :rtype: pd.DataFrame
        """
        return self._df_mi('groups', ['group_pk', 'characteristica_pk'])



    @property
    def groups_core(self) -> PKDataFrame:
        """  Core group information with unique pk per row

        :return: PKDataFrame of groups contained in this PKData instance .
        :rtype: PKDataFrame
        """
        return self._df_core("groups", core_fields=["study_name","group_name", "group_count"])

    @property
    def individuals_mi(self) -> pd.DataFrame:
        """Multi-index DataFrame of individuals contained in this PKData instance.

        :return: Multi-indexed DataFrame of individuals contained in this PKData instance.
        :rtype: pd.DataFrame
        """
        return self._df_mi('individuals', ['individual_pk', 'individual_name', 'characteristica_pk'])

    @property
    def individuals_core(self) -> PKDataFrame:
        """  Core individual information with unique pk per row

        :return: PKDataFrame of individuals contained in this PKData instance .
        :rtype: PKDataFrame
        """
        return self._df_core("individuals", core_fields=["study_name","individual_name"])

    @property
    def interventions_mi(self) -> pd.DataFrame:
        """Multi-index DataFrame of interventions contained in this PKData instance.

        :return: Multi-indexed DataFrame of interventions contained in this PKData instance.
        :rtype: pd.DataFrame
        """
        return self._df_mi('interventions', ['intervention_pk'])

    @property
    def interventions_core(self) -> PKDataFrame:
        """  Core group information with unique pk per row

        :return: PKDataFrame of groups contained in this PKData instance .
        :rtype: PKDataFrame
        """
        return self._df_core("interventions", core_fields=["study_name", "name"])


    @property
    def outputs_mi(self) -> pd.DataFrame:
        """Multi-index DataFrame of outputs contained in this PKData instance.

        :return: Multi-indexed DataFrame of outputs contained in this PKData instance.
        :rtype: pd.DataFrame
        """
        return self._df_mi('outputs',
                           ['output_pk', 'intervention_pk', 'group_pk', 'individual_pk'])

    @property
    def timecourses_mi(self) -> pd.DataFrame:
        """Multi-index DataFrame of timecourses contained in this PKData instance.

        :return: Multi-indexed DataFrame of timecourses contained in this PKData instance.
        :rtype: pd.DataFrame
        """
        return self._df_mi('timecourses',
                           ['timecourse_pk', 'intervention_pk', 'group_pk', 'individual_pk'])

    @property
    def timecourses_extended(self) -> pd.DataFrame:
        """ extends the timecourse df with the core information from interventions, individuals and groups"""

        timecourses = self.timecourses.df.merge(self.interventions_core,
                                                how="left",
                                                on="intervention_pk",
                                                suffixes=("","interventions"))
        timecourses = timecourses.merge(self.individuals_core,
                                        how="left",
                                        on="individual_pk",
                                        suffixes=("","individuals"))
        timecourses = timecourses.merge(self.groups_core,
                                        how="left",
                                        on="group_pk",
                                        suffixes=("","groups"))
        return timecourses
    # --- filter and exclude ---

    def _pk_filter(self, df_key:str, f_idx, concise:bool, *args, **kwargs) -> 'PKData':
        """ Helper class for filtering of PKData instances.
        :param df_key: DataFrame on which the filter (f_idx) shall be applied.
        :type df_key: str
        :param concise:
        :return:
        """
        dict_pkdata = self.as_dict()
        dict_pkdata[df_key] = getattr(self, df_key).pk_filter(f_idx, **kwargs)

        pkdata = PKData(**dict_pkdata)
        if concise:
            pkdata._concise()
        return pkdata

    def _pk_exclude(self, df_k, f_idx, concise, **kwargs) -> 'PKData':

        dict_pkdata = self.as_dict()
        dict_pkdata[df_k] = getattr(self, df_k).pk_exclude(f_idx, **kwargs)

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

    def filter_study(self, f_idx, concise=True, **kwargs) -> 'PKData':
        """ Filter groups. """
        return self._pk_filter("studies", f_idx, concise, **kwargs)

    def filter_intervention(self, f_idx, concise=True, *args, **kwargs) -> 'PKData':
        """Filter interventions.

        :param f_idx: Is a filter by index of the DataFrame selected by the df_key. A similar notation as the filtering
            of pd.DataFrames can be used. This mostly are (lambda) functions. Further a list of (lambda) function are allowed
            as input. The list of functions are executed successively, which is identical to an intersection of all filters
            applied separately.

            Pitfalls
                - Don't use the invert operator `~` but use the exclude_*() functions.
                - #todo: add no invert operator to Validation rule
        :type f_idx: function, list


        :param concise: concises the returned PKData instance.

        :return: Filter PKData instance
        :rtype: PKData
        """

        return self._pk_filter("interventions", f_idx, concise, **kwargs)

    def filter_group(self, f_idx, concise=True, **kwargs) -> 'PKData':
        """ Filter groups. """
        return self._pk_filter("groups", f_idx, concise, **kwargs)

    def filter_individual(self, f_idx, concise=True, **kwargs) -> 'PKData':

        """ Filter individuals. """
        return self._pk_filter("individuals", f_idx, concise, **kwargs)

    def filter_subject(self, f_idx, concise=True, **kwargs) -> 'PKData':
        """ Filter group or individual. """
        pkdata = self.filter_group(f_idx, concise=False, **kwargs)
        pkdata = pkdata.filter_individual(f_idx, concise=False, **kwargs)
        if concise:
            pkdata._concise()
        return pkdata

    def filter_output(self, f_idx, concise=True, **kwargs) -> 'PKData':
        """ Filter outputs. """
        return self._pk_filter("outputs", f_idx, concise, **kwargs)

    def filter_timecourse(self, f_idx, concise=True, **kwargs) -> 'PKData':
        """ Filter timecourses. """
        return self._pk_filter("timecourses", f_idx, concise, **kwargs)

    def exclude_study(self, f_idx, concise=True, **kwargs) -> 'PKData':
        """ Filter groups. """
        return self._pk_exclude("studies", f_idx, concise, **kwargs)

    def exclude_intervention(self, f_idx, concise=True, **kwargs) -> 'PKData':
        return self._pk_exclude("interventions", f_idx, concise, **kwargs)

    def exclude_group(self, f_idx, concise=True, **kwargs) -> 'PKData':
        return self._pk_exclude("groups", f_idx, concise, **kwargs)

    def exclude_individual(self, f_idx, concise=True, **kwargs):
        return self._pk_exclude("individuals", f_idx, concise, **kwargs)

    def exclude_subject(self, f_idx, concise=True, **kwargs) -> 'PKData':
        pkdata = self.exclude_group(f_idx, concise=False, **kwargs)
        pkdata = pkdata.exclude_individual(f_idx, concise=False, **kwargs)
        if concise:
            pkdata._concise()
        return pkdata

    def exclude_output(self, f_idx, concise=True, **kwargs) -> 'PKData':
        return self._pk_exclude("outputs", f_idx, concise, **kwargs)

    def exclude_timecourse(self, f_idx, concise=True, **kwargs):

        return self._pk_exclude("timecourses", f_idx, concise, **kwargs)

    def delete_groups(self, concise=True) -> 'PKData':
        """
        Deletes outputs.
        :return:
        """
        return self._emptify("groups", concise=concise)

    def delete_individuals(self, concise=True) -> 'PKData':
        """
        Deletes outputs.
        :return:
        """
        return self._emptify("individuals", concise=concise)

    def delete_outputs(self, concise=True) -> 'PKData':
        """
        Deletes outputs.
        :return:
        """
        return self._emptify("outputs", concise=concise)


    def delete_timecourses(self, concise=True) -> 'PKData':
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

            # concise based on studies
            outputs_study_sids = set(self.outputs.study_sid)
            timecourses_study_sids = set(self.timecourses.study_sid)
            interventions_study_sids = set(self.interventions.study_sid)
            groups_study_sids = set(self.groups.study_sid)
            individuals_study_sids = set(self.individuals.study_sid)

            study_sid_sets = [outputs_study_sids, timecourses_study_sids, interventions_study_sids, groups_study_sids,individuals_study_sids]
            current_study_sid_sets = set().union(*study_sid_sets)
            self.studies =  self.studies[self.studies.sid.isin(current_study_sid_sets)]
            for df_key in ["interventions", "groups", "individuals", "timecourses", "outputs"]:
                df = getattr(self, df_key)
                setattr(self, df_key, df[df["study_sid"].isin(self.studies.pks)])


            # concise based on interventions
            outputs_intervention_pks = set(self.outputs.intervention_pk)
            timecourses_intervention_pks = set(self.timecourses.intervention_pk)

            current_intervention_pks = (self.interventions.pks.intersection(outputs_intervention_pks)).union(
                self.interventions.pks.intersection(timecourses_intervention_pks))

            self.interventions = self.interventions[self.interventions.intervention_pk.isin(current_intervention_pks)]
            self.timecourses = self.timecourses[self.timecourses.intervention_pk.isin(current_intervention_pks)]
            self.outputs = self.outputs[self.outputs.intervention_pk.isin(current_intervention_pks)]

            # concise based on individuals
            outputs_individual_pks = set(self.outputs.individual_pk)
            timecourses_individual_pks = set(self.timecourses.individual_pk)

            current_individual_pks = (self.individuals.pks.intersection(outputs_individual_pks)).union(
                                     self.individuals.pks.intersection(timecourses_individual_pks))
            current_individual_pks.add(-1)

            for df_key in ["individuals", "timecourses", "outputs"]:
                df = getattr(self, df_key)
                setattr(self, df_key, df[df["individual_pk"].isin(current_individual_pks)])

            # concise based on groups
            outputs_group_pks = set(self.outputs.group_pk)
            timecourses_group_pks = set(self.timecourses.group_pk)

            current_group_pks = (self.groups.pks.intersection(outputs_group_pks)).union(
                                self.groups.pks.intersection(timecourses_group_pks))

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
                    values = [c for c in set(df[key]) if c is not None]
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
