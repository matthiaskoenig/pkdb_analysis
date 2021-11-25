"""
Functions for working with PKDB data.

* FIXME: specify which methods modify or copy data frames
"""
import logging
import os
import tempfile
import zipfile
from abc import ABC
from ast import literal_eval
from collections import OrderedDict
from io import BytesIO
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Union

import numpy as np
import pandas as pd
import requests
from IPython.display import display

from pkdb_analysis.filter import f_healthy, f_n_healthy, filter_factory
from pkdb_analysis.units import ureg
from pkdb_analysis.utils import create_parent


# from pandas.errors import PerformanceWarning
# This is not fixing anything, but just ignoring the problem !!!
# warnings.simplefilter(action="ignore", category=PerformanceWarning)

logger = logging.getLogger(__name__)


class PKDataFrame(pd.DataFrame, ABC):
    """
    Extended DataFrame which support customized filter operations.
    Used to encode groups, individuals, interventions, outputs, data on PKData.
    """

    @property
    def _constructor(self):
        """Internal function need for inheritances from pd.DataFrame."""
        return PKDataFrame._internal_ctor

    _metadata = ["pk"]

    @classmethod
    def _internal_ctor(cls, *args, **kwargs):
        """Internal function need for inheritances from pd.DataFrame."""
        kwargs["pk"] = None
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

        super(PKDataFrame, self).__init__(
            data=data, index=index, columns=columns, dtype=dtype, copy=copy
        )
        self.pk = pk

    @staticmethod
    def _validate_not_in_columns(columns: Iterable[str]):
        """ """
        if columns:
            assert "pk" in columns

    def pk_filter(self, f_idx: Callable, **kwargs) -> "PKDataFrame":
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

    def pk_exclude(self, f_idx: Callable, **kwargs) -> "PKDataFrame":
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

    @staticmethod
    def _change_unit(sd, unit):
        infer_fields = ["value", "mean", "median", "min", "max", "sd", "se"]
        return PKDataFrame._change_unit_generic(
            sd=sd, unit=unit, infer_fields=infer_fields, unit_field="unit"
        )

    @staticmethod
    def _change_unit_generic(sd, unit: str, infer_fields: List[str], unit_field: str):
        if isinstance(sd[unit_field], str):
            if ureg(sd[unit_field]).check(unit):
                factor = ureg(sd[unit_field]).to(unit).m
                sd[infer_fields] = sd[infer_fields] * factor
                sd[unit_field] = unit
        return sd

    @staticmethod
    def _change_time_unit(sd, unit):
        infer_fields = ["time"]
        unit_field = "time_unit"
        return PKDataFrame._change_unit_generic(
            sd=sd, unit=unit, infer_fields=infer_fields, unit_field=unit_field
        )

    def change_unit(self, unit):
        df = self.df.apply(self._change_unit, unit=unit, axis=1)
        return PKDataFrame(df, pk=self.pk)

    def change_time_unit(self, unit):
        df = self.df.apply(self._change_time_unit, unit=unit, axis=1)
        return PKDataFrame(df, pk=self.pk)

    @property
    def pk_column(self):
        """Returns the column containing the primary value of this table"""
        return self[self.pk]

    @property
    def pks(self) -> set:
        """Set of pks."""
        if self.pk in self.df.columns:
            return set(self[self.pk].unique())
        else:
            return set()

    @property
    def pk_len(self) -> int:
        """returns number of unique identifiers within the table. This value can be smaller than the number
        of rows. Since multiple rows can represent one instances."""
        return len(self.pks)

    @property
    def df(self) -> pd.DataFrame:
        """Returns a copied DataFrame."""
        df = self.copy()
        del df.pk
        return pd.DataFrame(self)

    @property
    def study_sids(self) -> set:
        """Set of study_sids."""
        study_sids = set([])
        if "study_sid" in self.df.columns:
            study_sids = set(self.study_sid.unique())
        return study_sids

    def _emptify(self) -> "PKDataFrame":
        """Removes all entries from table."""
        empty_df = pd.DataFrame([], columns=self.columns)
        return PKDataFrame(empty_df, pk=self.pk)

    def __str__(self):
        return self.df.__str__()

    def __repr__(self):
        return self.df.__repr__()

    def _repr_html_(self):
        return display(self.df)


class PKData(object):
    """Consistent set of data from PK-DB.set -a && source .env.local

    Information is stored as DataFrames.

    Handles:

    - groups
    - individuals
    - interventions
    - outputs
    - timecourses
    """

    PK_COLUMNS = {
        "studies": "study_pk",
        "groups": "group_pk",
        "individuals": "individual_pk",
        "interventions": "intervention_pk",
        "outputs": "output_pk",
        "timecourses": "subset_pk",
        "scatters": "subset_pk",
    }

    KEYS = [
        "studies",
        "groups",
        "individuals",
        "interventions",
        "outputs",
        "timecourses",
        "scatters",
    ]

    # PK_COLUMNS = {key: f"{key[:-1]}_pk" for key in KEYS}

    def __init__(
        self,
        studies: pd.DataFrame = None,
        interventions: pd.DataFrame = None,
        groups: pd.DataFrame = None,
        individuals: pd.DataFrame = None,
        outputs: pd.DataFrame = None,
        timecourses: pd.DataFrame = None,
        scatters: pd.DataFrame = None,
    ):
        """Creates PKDB data object from given DataFrames.

        :param interventions:
        :param individuals:
        :param groups:
        :param outputs:
        :param timecourses:
        :param scatters:


        """
        self.studies = PKDataFrame(studies, pk="sid")

        self.groups = PKDataFrame(groups, pk="group_pk")
        self.individuals = PKDataFrame(individuals, pk="individual_pk")
        self.interventions = PKDataFrame(interventions, pk="intervention_pk").replace(
            {np.nan: None}
        )
        self.outputs = PKDataFrame(outputs, pk="output_pk")
        self.timecourses = PKDataFrame(timecourses, pk="subset_pk")
        self.scatters = PKDataFrame(scatters, pk="subset_pk")

        if not self.individuals.empty:
            self.individuals.substance = self.individuals.substance.astype(str)
        if not self.groups.empty:
            self.groups.substance = self.groups.substance.astype(str)

        def _transform_strings_tuple(value):
            if isinstance(value, str):
                if value.startswith("[") or value.startswith("("):
                    return tuple(np.fromstring(value[1:-1], sep=", "))
                    # return tuple([z for z in value[1:-1].split(",")])
            return value

        if not self.timecourses.empty:
            self.timecourses[
                [
                    "output_pk",
                    "intervention_pk",
                    "mean",
                    "value",
                    "sd",
                    "se",
                    "min",
                    "max",
                ]
            ] = self.timecourses[
                [
                    "output_pk",
                    "intervention_pk",
                    "mean",
                    "value",
                    "sd",
                    "se",
                    "min",
                    "max",
                ]
            ].df.applymap(
                _transform_strings_tuple
            )

    def __dict___(self):
        """serialises pkdata instance to a dict."""
        return {df_key: getattr(self, df_key).df for df_key in PKData.KEYS}

    def as_dict(self):
        """serialises pkdata instance to a dict."""
        return self.__dict___()

    def copy(self):
        """creates a copy of the pkdata instance."""
        return PKData(**self.as_dict())

    def __str__(self):
        """Overview of content.

        :return:
        """
        lines = [
            "-" * 30,
            f"{self.__class__.__name__} ({id(self)})",
            "-" * 30,
        ]

        for key in self.KEYS:
            if key != "data":
                df = getattr(self, key)
                nrows = len(df)
                count = df.pk_len
                lines.append(f"{key:<15} {count:>5}  ({nrows:>5})")
            else:
                lines.append(
                    f"{key:<12} tc:{self.timecourses_count:>5}  sc:{self.scatter_count:>3}"
                )

        lines.append("-" * 30)
        return "\n".join(lines)

    def __or__(self, other: "PKData") -> "PKData":
        """combines two PKData instances
        :param other: other PkData instance
        :return: PKData
        """

        resulting_kwargs = dict()

        for df_key in self.KEYS:
            df = getattr(self, df_key)
            other_df = getattr(other, df_key)
            resulting_df = df.append(other_df)
            resulting_df = resulting_df.loc[
                ~resulting_df.index.duplicated(keep="first")
            ]

            resulting_kwargs[df_key] = resulting_df

        return PKData(**resulting_kwargs)

    def __and__(self, other: "PKData") -> "PKData":
        """combines instances were instances have to

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
            resulting_df = resulting_df.loc[
                ~resulting_df.index.duplicated(keep="first")
            ]
            resulting_kwargs[df_key] = resulting_df

        return PKData(**resulting_kwargs)

    @classmethod
    def from_download(cls, path: Union[BytesIO, os.PathLike]) -> "PKData":
        """Load data from downloaded zip archive."""
        pkdata = cls.from_archive(path=path)
        # fix the intervention keys due to different serialization format
        pkdata = cls._intervention_pk_update(pkdata)
        return pkdata

    @classmethod
    def from_archive(cls, path: Union[BytesIO, os.PathLike]) -> "PKData":
        """Load data from serialized archive."""
        data_dict = {}
        with zipfile.ZipFile(path, "r") as archive:
            for key in PKData.KEYS:
                df = pd.read_csv(archive.open(f"{key}.csv", "r"), low_memory=False)
                data_dict[key] = PKData._clean_types(
                    df, is_array=key in ["timecourses", "scatters"]
                )
        # create data from data frames
        return PKData(**data_dict)

    def to_archive(self, path: Path) -> None:
        """Saves data to zip archive"""
        create_parent(path)
        with zipfile.ZipFile(path, "w") as archive:
            for key in PKData.KEYS:
                df = getattr(self, key)  # type: pd.DataFrame
                with tempfile.NamedTemporaryFile() as fp:
                    df.to_csv(fp.name)
                    archive.write(filename=fp.name, arcname=f"{key}.csv")

    @staticmethod
    def from_hdf5(path: Path) -> "PKData":
        """Load data from an archive as returned from the download in pk-db.com.

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
        """Saves data HDF5."""
        create_parent(path)
        store = pd.HDFStore(path)
        for key in [
            "studies",
            "interventions",
            "individuals",
            "groups",
            "outputs",
            "timecourses",
        ]:
            df = getattr(self, key).df
            store[key] = df
        store.close()

    @property
    def study_sids(self) -> set:
        """Set of study sids contained in this PKData instance.

        :return: Study sids contained in this PKData instance.
        :rtype: set
        """
        study_sids = set()
        for df_key in PKData.KEYS:
            pk_df = getattr(self, df_key)
            study_sids = study_sids.union(pk_df.study_sids)

        return study_sids

    def healthy(self):
        """subset of healthy data."""
        return self.filter_subject(f_healthy, concise=False).exclude_subject(
            f_n_healthy
        )

    @property
    def groups_count(self) -> int:
        """Number of groups contained in this PKData instance.

        :return: Number of groups contained in this PKData instance.
        :rtype: int
        """
        return self.groups.pk_len

    @property
    def individuals_count(self) -> int:
        """Number of individuals contained in this PKData instance.

        :return: Number of individuals contained in this PKData instance.
        :rtype: int
        """
        return self.individuals.pk_len

    @property
    def interventions_count(self) -> int:
        """Number of interventions contained in this PKData instance.

        :return: Number of interventions contained in this PKData instance.
        :rtype: int
        """
        return self.interventions.pk_len

    @property
    def outputs_count(self) -> int:
        """Number of outputs contained in this PKData instance.

        :return: Number of outputs contained in this PKData instance.
        :rtype: int
        """
        return self.outputs.pk_len

    @property
    def timecourses_count(self) -> int:
        """Number of timecourses contained in this PKData instance.

        :return: Number of timecourses contained in this PKData instance.
        :rtype: int
        """
        return self.timecourses.pk_len

    @property
    def scatter_count(self) -> int:
        """Number of timecourses contained in this PKData instance.

        :return: Number of timecourses contained in this PKData instance.
        :rtype: int
        """
        return self.data[self.data.data_type == "scatter"].pk_len

    @property
    def timecourses_extended(self) -> pd.DataFrame:
        """extends the timecourse df with the core information from interventions, individuals and groups"""

        timecourses = self.timecourses.df.merge(
            self.interventions_core,
            how="left",
            on="intervention_pk",
            suffixes=("", "interventions"),
        )
        timecourses = timecourses.merge(
            self.individuals_core,
            how="left",
            on="individual_pk",
            suffixes=("", "individuals"),
        )
        timecourses = timecourses.merge(
            self.groups_core, how="left", on="group_pk", suffixes=("", "groups")
        )
        return timecourses

    def _df_mi(self, field: str, index_fields: List[str]) -> pd.DataFrame:
        """Create multi-index DataFrame

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
        """Core group information with unique pk per row"""

        pk_df = getattr(self, field)
        return pk_df.pivot_table(
            index=pk_df.pk, values=core_fields, aggfunc=lambda x: x.iloc[0]
        ).reset_index()

    @property
    def groups_mi(self) -> pd.DataFrame:
        """Multi-index DataFrame of groups contained in this PKData instance.

        :return: Multi-indexed DataFrame of groups contained in this PKData instance.
        :rtype: pd.DataFrame
        """
        return self._df_mi("groups", ["group_pk", "characteristica_pk"])

    @property
    def groups_core(self) -> PKDataFrame:
        """Core group information with unique pk per row

        :return: PKDataFrame of groups contained in this PKData instance .
        :rtype: PKDataFrame
        """
        return self._df_core(
            "groups", core_fields=["study_name", "group_name", "group_count"]
        )

    @property
    def individuals_mi(self) -> pd.DataFrame:
        """Multi-index DataFrame of individuals contained in this PKData instance.

        :return: Multi-indexed DataFrame of individuals contained in this PKData instance.
        :rtype: pd.DataFrame
        """
        return self._df_mi(
            "individuals", ["individual_pk", "individual_name", "characteristica_pk"]
        )

    @property
    def individuals_core(self) -> PKDataFrame:
        """Core individual information with unique pk per row

        :return: PKDataFrame of individuals contained in this PKData instance .
        :rtype: PKDataFrame
        """
        return self._df_core(
            "individuals", core_fields=["study_name", "individual_name"]
        )

    @property
    def interventions_mi(self) -> pd.DataFrame:
        """Multi-index DataFrame of interventions contained in this PKData instance.

        :return: Multi-indexed DataFrame of interventions contained in this PKData instance.
        :rtype: pd.DataFrame
        """
        return self._df_mi("interventions", ["intervention_pk"])

    @property
    def interventions_core(self) -> PKDataFrame:
        """Core group information with unique pk per row

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
        return self._df_mi(
            "outputs", ["output_pk", "intervention_pk", "group_pk", "individual_pk"]
        )

    @property
    def timecourses_mi(self) -> pd.DataFrame:
        """Multi-index DataFrame of timecourses contained in this PKData instance.

        :return: Multi-indexed DataFrame of timecourses contained in this PKData instance.
        :rtype: pd.DataFrame
        """
        return self._df_mi(
            "timecourses", ["subset_pk", "intervention_pk", "group_pk", "individual_pk"]
        )

    # --- filter and exclude ---
    def _pk_filter(
        self, df_key: str, f_idx, concise: bool, *args, **kwargs
    ) -> "PKData":
        """Helper class for filtering of PKData instances.
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

    def _pk_exclude(self, df_k, f_idx, concise, **kwargs) -> "PKData":
        """Generic function to exclude data selected by the table key (df_k) and filtered by f_idx."""

        dict_pkdata = self.as_dict()
        dict_pkdata[df_k] = getattr(self, df_k).pk_exclude(f_idx, **kwargs)
        pkdata = PKData(**dict_pkdata)
        if concise:
            pkdata._concise()
        return pkdata

    def _emptify(self, df_key, concise=True) -> "PKData":
        """generic function to emptify a table selected by the key."""
        self._validate_df_key(df_key)

        dict_pkdata = self.as_dict()
        dict_pkdata[df_key] = getattr(self, df_key)._emptify()

        pkdata = PKData(**dict_pkdata)
        if concise:
            pkdata._concise()
        return pkdata

    @staticmethod
    def _validate_df_key(df_key):
        """correct key validations function"""
        if df_key not in PKData.KEYS:
            raise ValueError(
                f"Unsupported key '{df_key}', key must be in '{PKData.KEYS}'"
            )

    def filter_study(self, f_idx, concise=True, **kwargs) -> "PKData":
        """Filter studies by filter function."""
        return self._pk_filter("studies", f_idx, concise, **kwargs)

    def filter_intervention(self, f_idx, concise=True, *args, **kwargs) -> "PKData":
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

    def filter_group(self, f_idx, concise=True, **kwargs) -> "PKData":
        """Filter groups."""

        return self._pk_filter("groups", f_idx, concise, **kwargs)

    def filter_individual(self, f_idx, concise=True, **kwargs) -> "PKData":
        """Filter individuals."""

        return self._pk_filter("individuals", f_idx, concise, **kwargs)

    def filter_subject(self, f_idx, concise=True, **kwargs) -> "PKData":
        """Filter group or individual."""
        pkdata = self.filter_group(f_idx, concise=False, **kwargs)
        pkdata = pkdata.filter_individual(f_idx, concise=False, **kwargs)
        if concise:
            pkdata._concise()
        return pkdata

    def filter_output(self, f_idx, concise=True, **kwargs) -> "PKData":
        """Filter outputs."""
        return self._pk_filter("outputs", f_idx, concise, **kwargs)

    def filter_timecourse(self, f_idx, concise=True, **kwargs) -> "PKData":
        """Filter timecourses."""
        return self._pk_filter("timecourses", f_idx, concise, **kwargs)

    def filter(self, filter_dict: Dict) -> "PKData":
        pkdata = self.copy()
        filter_functions = [
            "groups",
            "individuals",
            "interventions",
            "outputs",
        ]
        for key in filter_functions:
            # filter each table separately by dedicated function
            table_filter_definitions = filter_dict.get(key, None)
            if table_filter_definitions:
                table_filters = filter_factory(table_filter_definitions)
                pkdata = pkdata._pk_filter(key, f_idx=table_filters, concise=False)
        pkdata._concise()
        return pkdata

    def exclude_study(self, f_idx, concise=True, **kwargs) -> "PKData":
        """Excludes studies which cann be selected by a filter (idx)."""

        return self._pk_exclude("studies", f_idx, concise, **kwargs)

    def exclude_intervention(self, f_idx, concise=True, **kwargs) -> "PKData":
        """Excludes interventions which cann be selected by a filter (idx)."""

        return self._pk_exclude("interventions", f_idx, concise, **kwargs)

    def exclude_group(self, f_idx, concise=True, **kwargs) -> "PKData":
        """Excludes groups which cann be selected by a filter (idx)."""

        return self._pk_exclude("groups", f_idx, concise, **kwargs)

    def exclude_individual(self, f_idx, concise=True, **kwargs):
        """Excludes individuals which cann be selected by a filter (idx)."""

        return self._pk_exclude("individuals", f_idx, concise, **kwargs)

    def exclude_subject(self, f_idx, concise=True, **kwargs) -> "PKData":
        """Excludes groups and individuals which cann be selected by a filter (idx).

        :param f_idx:
        :param concise:
        :param kwargs:
        :return:
        """
        pkdata = self.exclude_group(f_idx, concise=False, **kwargs)
        pkdata = pkdata.exclude_individual(f_idx, concise=False, **kwargs)
        if concise:
            pkdata._concise()
        return pkdata

    def exclude_output(self, f_idx, concise=True, **kwargs) -> "PKData":
        return self._pk_exclude("outputs", f_idx, concise, **kwargs)

    def exclude_timecourse(self, f_idx, concise=True, **kwargs):

        return self._pk_exclude("timecourses", f_idx, concise, **kwargs)

    def delete_groups(self, concise=True) -> "PKData":
        """
        Deletes outputs.
        :return:
        """
        return self._emptify("groups", concise=concise)

    def delete_individuals(self, concise=True) -> "PKData":
        """
        Deletes outputs.
        :return:
        """
        return self._emptify("individuals", concise=concise)

    def delete_outputs(self, concise=True) -> "PKData":
        """
        Deletes outputs.
        :return:
        """
        return self._emptify("outputs", concise=concise)

    def delete_timecourses(self, concise=True) -> "PKData":
        """Deletes timecourses."""
        return self._emptify("timecourses", concise=concise)

    @property
    def ids(self):
        """unique ids of all tables within a pkdata instance."""
        return {
            "studies": list(self.studies.pks),
            "groups": list(self.groups.pks),
            "individuals": list(self.individuals.pks),
            "interventions": list(self.interventions.pks),
            "outputs": list(self.outputs.pks),
            "timecourses": list(self.timecourses.pks),
            # "scatters": list(self.scatters.pks),
        }

    def _concise(self) -> None:
        """Reduces the current PKData to a consistent subset.
        Modifies the DataFrame in place.
        :return:
        """
        # FIXME: scatters are not concised !!!

        self.outputs = self.outputs[
            self.outputs["group_pk"].isin(self.ids["groups"])
            | self.outputs["individual_pk"].isin(self.ids["individuals"])
        ]
        self.outputs = self.outputs[
            self.outputs["intervention_pk"].isin(self.ids["interventions"])
        ]

        concised_ids = {
            "studies": list(self.outputs.study_sid.unique()),
            "groups": list(self.outputs.group_pk.unique()),
            "individuals": list(self.outputs.individual_pk.unique()),
            "interventions": list(self.outputs.intervention_pk.unique()),
            "outputs": list(self.outputs.pks),
            "timecourses": list(self.timecourses.pks),
            # "scatters": list(self.scatters.pks),
        }

        self.studies = self.studies[self.studies["sid"].isin(concised_ids["studies"])]
        self.interventions = self.interventions[
            self.interventions["intervention_pk"].isin(concised_ids["interventions"])
        ]
        self.groups = self.groups[self.groups["group_pk"].isin(concised_ids["groups"])]
        self.individuals = self.individuals[
            self.individuals["individual_pk"].isin(concised_ids["individuals"])
        ]

        if not self.timecourses.empty:
            _timecourses = pd.DataFrame(
                {
                    "subset_pk": np.repeat(
                        self.timecourses.subset_pk.values,
                        self.timecourses.output_pk.str.len(),
                    ),
                    "output_pk": np.concatenate(self.timecourses.output_pk.values),
                }
            )
            _timecourses["output_pk"] = _timecourses["output_pk"].astype(int)

            _timecourses = _timecourses[
                _timecourses["output_pk"].isin(concised_ids["outputs"])
            ]
            self.timecourses = self.timecourses[
                self.timecourses["subset_pk"].isin(_timecourses.subset_pk.unique())
            ]

    @property
    def _len_total(self):
        """The sum of all entries in all tables."""
        return sum([len(getattr(self, df_key)) for df_key in PKData.KEYS])

    def get_choices(self):
        """This is experimental.
        returns choices

        :return:
        """
        all_choices = OrderedDict()
        for df_key in self.KEYS:
            df = getattr(self, df_key)
            choices = OrderedDict()
            for key in df.columns:
                if df[key].dtype in ["bool", "object"]:
                    # remove None so sorting is working
                    values = [c for c in set(df[key]) if c is not None]
                    choices[key] = sorted(values)

            all_choices[df_key] = choices
        return all_choices

    def print_choices(self, key=None, field=None):
        """Prints the choices

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
                    raise ValueError(
                        f"Unsupported field '{field}', field must be in '{choices.keys()}'"
                    )
                fields = [field]
            else:
                fields = choices.keys()

            for field in fields:
                print(f"*** {field} ***")
                print(choices[field])

    def _map_intervention_pks(self):
        """Helper Function for the transformation of intervention_pk in outputs and timecourses.
        returns a mapping of old intervetions_pks with new intervetion_pks
        """
        interventions_output = pd.DataFrame()

        if not self.outputs.empty:
            interventions_output = self.outputs.df.pivot_table(
                values="intervention_pk",
                index="output_pk",
                aggfunc=lambda x: frozenset(x),
            )

        interventions = interventions_output.drop_duplicates(
            "intervention_pk"
        ).reset_index()
        interventions.index = interventions.index.set_names(["intervention_pk_updated"])
        return interventions["intervention_pk"].reset_index()

    def _update_interventions(self, mapping_int_pks):
        """Updates intervention_pk based on if they are beeing used in the outputs. Multiple interventions can have the same
        intervention_pk. After the transformation each (output) row in the outputs links only to one intervention_pk."""
        """FIXME: document me"""
        mapping_int_pks = mapping_int_pks.copy()
        mapping_int_pks["intervention_pk"] = mapping_int_pks.intervention_pk.apply(
            lambda x: list(x)
        )
        mapping_int_pks = (
            mapping_int_pks.intervention_pk.apply(pd.Series)
            .stack()
            .reset_index(level=-1, drop=True)
            .astype(int)
            .reset_index()
        )
        mapping_int_pks = mapping_int_pks.rename(
            columns={"index": "intervention_pk_updated", 0: "intervention_pk"}
        )
        return (
            pd.merge(mapping_int_pks, self.interventions, on="intervention_pk")
            .drop(columns=["intervention_pk"])
            .rename(columns={"intervention_pk_updated": "intervention_pk"})
        )

    def _update_outputs(self, mapping_int_pks):
        """Dates up all intervention_pk in outputs table. Thereby each row becomes a unique output."""
        mapping_int_pks = mapping_int_pks.copy()

        interventions_output = self.outputs.df.pivot_table(
            values="intervention_pk", index="output_pk", aggfunc=lambda x: frozenset(x)
        )
        mapping_int_pks = pd.merge(
            interventions_output.reset_index(),
            mapping_int_pks,
            on="intervention_pk",
            how="left",
        )[["output_pk", "intervention_pk_updated"]]

        return (
            pd.merge(
                mapping_int_pks,
                self.outputs.df.drop_duplicates(subset="output_pk"),
                how="left",
            )
            .drop(columns=["intervention_pk"])
            .rename(columns={"intervention_pk_updated": "intervention_pk"})
        )

    def get_updated_intervention_pk(self, frozenset_intervention_pks):
        """return new set"""

    def _update_timecourses(self, mapping_int_pks):
        """Dates up all intervention_pk in timecourses table."""
        mapping_dict = (
            mapping_int_pks.copy()
            .set_index("intervention_pk")["intervention_pk_updated"]
            .to_dict()
        )
        self.timecourses["intervention_pk"] = self.timecourses["intervention_pk"].apply(
            lambda x: mapping_dict.get(frozenset(x))
        )

        return self.timecourses

    def _update_scatters(self, mapping_int_pks):
        """Dates up all intervention_pk in scatters table."""
        mapping_dict = (
            mapping_int_pks.copy()
            .set_index("intervention_pk")["intervention_pk_updated"]
            .to_dict()
        )

        self.scatters["x_intervention_pk"] = self.scatters["x_intervention_pk"].apply(
            frozenset
        )
        self.scatters["y_intervention_pk"] = self.scatters["y_intervention_pk"].apply(
            frozenset
        )

        self.scatters["x_intervention_pk"] = self.scatters["x_intervention_pk"].apply(
            lambda x: mapping_dict.get(frozenset(x))
        )

        self.scatters["y_intervention_pk"] = self.scatters["y_intervention_pk"].apply(
            lambda x: mapping_dict.get(frozenset(x))
        )

    def _intervention_pk_update(self):
        """Performs all three function necessary to update the
        intervention pks in all three tables where they are contained (interventions, output, timecourses)."""
        if self.outputs.empty:
            return self
        else:
            mapping_int_pks = self._map_intervention_pks()
            data_dict = self.as_dict()
            data_dict["interventions"] = self._update_interventions(mapping_int_pks)
            if not self.outputs.empty:
                data_dict["outputs"] = self._update_outputs(mapping_int_pks)
            if not self.timecourses.empty:
                data_dict["timecourses"] = self._update_timecourses(mapping_int_pks)
            # if not self.scatters.empty:
            #    data_dict["scatters"] = self._update_scatters(mapping_int_pks)
            return PKData(**data_dict)

    @staticmethod
    def _clean_types(df: pd.DataFrame, is_array):
        """Sets the correct datatypes for each column in the table (df)."""
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
            # "time",
        ]
        # convert columns to int columns
        int_columns = [
            "subset_pk",
            "group_pk",
            "individual_pk",
            "group_parent_pk",
            "raw_pk",
        ]

        if not is_array:
            int_columns.append("intervention_pk")
            for column in float_columns:
                if column in df.columns:
                    df[column] = df[column].astype(float)

        for column in int_columns:
            if column in df.columns:
                df[column] = df[column].replace({np.nan: -1}).astype(int)

        return df

    def to_medline(self, path: Path):
        """create a bibtex file."""

        create_parent(path)
        reference_pmids = [str(int(s)) for s in self.studies.reference_pmid if s]
        reference_pmids_str = "%2C".join(reference_pmids)
        url = (
            "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/?format=medline&id="
            + reference_pmids_str
            + "&download=y"
        )
        with requests.get(url) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                f.write(r.content)
