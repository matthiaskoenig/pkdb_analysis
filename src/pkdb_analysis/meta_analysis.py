import warnings
from typing import Dict, Set, Tuple

import numpy as np
import pandas as pd

from pkdb_analysis import PKData
from pkdb_analysis.deprecated.analysis import figure_category
from pkdb_analysis.filter import pk_info
from pkdb_analysis.inference.body_weight import infer_weight


INTERVENTION_FIELDS = ["substance", "value", "unit", "route", "form", "application"]
NUMERIC_FIELDS_NO_VALUE = ["mean", "min", "max", "median", "count", "sd", "se", "unit"]
NUMERIC_FIELDS = ["value"] + NUMERIC_FIELDS_NO_VALUE
MISSING_VALUE = "unknown"


def len1(d: pd.DataFrame) -> pd.DataFrame:
    """return DataFrame if length 1"""
    if len(d) == 1:
        return d


def validate_len1(d: pd.DataFrame) -> pd.DataFrame:
    """validates Dataframe has the length of 1."""
    assert 1 == len(d[d]), d
    return d


def data_type(d: pd.Series) -> str:
    """returns values for a new column called data_type."""
    if d["calculated"]:
        return "from timecourse"
    elif d["inferred"]:
        return "from bodyweight"
    else:
        return "publication"


def markers(d: pd.Series) -> str:
    """returns markers depending on data_type for plotting."""
    if d["calculated"]:
        return "s"
    elif d["inferred"]:
        return "v"
    else:
        return "o"


class MetaAnalysis(object):
    """Main class for meta analysis. Main functionality of the class is to merge the tables of an PKData objet into
    one Dataframe (self.results). The result is used for interactive plots, static plots, and table reports."""

    def __init__(
        self,
        pkdata: PKData,
        intervention_substances: Set[str] = None,
        url: str = "",
        first_intervention: bool = False,
    ):
        self.pkdata = pkdata
        self.results = None
        self.group_pk = pkdata.groups.pk
        self.individual_pk = pkdata.individuals.pk
        self.intervention_pk = pkdata.interventions.pk
        self.intervention_substances = intervention_substances
        self.url = url
        self.first_intervention = first_intervention

    def create_intervention_extra(self):
        """Returns the 'intervention_extra' column with complete information on intervention."""
        table = self.pkdata.interventions
        _table = pd.DataFrame()
        for table_pk, df in table.df.groupby(table.pk):
            if self.intervention_substances:
                subset = df[df["substance"].isin(self.intervention_substances)].copy()
            else:
                subset = df.copy()
            subset["number"] = len(df)
            if len(subset) == 1:
                subset = subset.iloc[0]
                subset["extra"] = df
                _table = _table.append(subset)
            else:
                if self.first_intervention:
                    subset = subset.sort_values("time").iloc[0]
                    subset["extra"] = df
                    _table = _table.append(subset)
                else:
                    ds = df.iloc[0]
                    warnings.warn(
                        f"Outputs with interventions <{list(subset['name'])}> in study <{ds['study_name']}> are "
                        f"removed from the plots. Due to the administration of one of the "
                        f"substances <{self.intervention_substances}> multiple times. It is not clear how to "
                        f"calculated the dosage and compare to a single dose application."
                    )
        return _table

    @staticmethod
    def subject_numeric_info(df: pd.DataFrame, measurement_type: str) -> Tuple:
        """Returns values for a numeric measurement type (e.g weight , height, age)"""
        measurement_data = df.extra[df.extra["measurement_type"] == measurement_type]
        if len(measurement_data) == 1:
            return tuple(measurement_data.iloc[0][NUMERIC_FIELDS].values)
        else:
            return tuple([np.nan for _ in NUMERIC_FIELDS])

    def create_subject_table(
        self,
        subject: str,
        numeric_fields: Tuple[str] = ("weight", "age"),
        categorical_fields: Tuple[str] = ("sex",),
        add_healthy: bool = True,
    ) -> pd.DataFrame:
        """Creates a table with subject information compatible with outputs table."""

        subject_core = getattr(self.pkdata, f"{subject}_core")
        subject_df = getattr(self.pkdata, subject)

        if add_healthy:
            healthy_subjects_pks = getattr(self.pkdata.healthy(), subject).pks
            subject_core["healthy"] = subject_core[subject_df.pk].isin(
                healthy_subjects_pks
            )

        subject_numeric_extra = [
            pk_info(subject_df, numeric_field, NUMERIC_FIELDS)
            for numeric_field in numeric_fields
        ]
        subject_categorical_extra = []
        for categorical_field in categorical_fields:
            detail_info = pk_info(subject_df, categorical_field, ["choice"]).rename(
                columns={f"choice_{categorical_field}": categorical_field}
            )
            subject_categorical_extra.append(detail_info)

        for individuals_info in [*subject_categorical_extra, *subject_numeric_extra]:
            subject_core = pd.merge(
                subject_core, individuals_info, on=subject_df.pk, how="left"
            )

        for categorical_field in categorical_fields:
            subject_core[categorical_field] = subject_core[categorical_field].fillna(
                MISSING_VALUE
            )

        pk = subject_df.pk

        subject_core["extra"] = getattr(subject_core, pk).apply(
            lambda x: subject_df[subject_df[pk] == x]
        )
        for measurement_type in ["age", "weight"]:
            subject_extra = subject_core.apply(
                self.subject_numeric_info,
                args=(measurement_type,),
                axis=1,
                result_type="expand",
            )
            if subject_extra.empty:
                subject_core[
                    [f"{k}_{measurement_type}" for k in NUMERIC_FIELDS]
                ] = tuple([np.nan for _ in NUMERIC_FIELDS])
            else:
                subject_core[
                    [f"{k}_{measurement_type}" for k in NUMERIC_FIELDS]
                ] = subject_extra
        return subject_core

    def add_extra_info(self, replacements: Dict[str, Dict[str, str]]):
        """a generic function to"""
        self.results["unit_category"] = self.results[
            ["per_bw", "intervention_per_bw"]
        ].apply(figure_category, axis=1)
        self.results["y"] = self.results[["mean", "median", "value"]].max(axis=1)
        self.results["y_min"] = self.results["y"] - self.results["sd"]
        self.results["y_max"] = self.results["y"] + self.results["sd"]

        self.results["weight"] = self.results[
            ["mean_weight", "median_weight", "value_weight"]
        ].max(axis=1)
        self.results["min_sd_weight"] = (
            self.results["weight"] - self.results["sd_weight"]
        )
        self.results["max_sd_weight"] = (
            self.results["weight"] + self.results["sd_weight"]
        )

        self.results["age"] = self.results[["mean_age", "median_age", "value_age"]].max(
            axis=1
        )
        self.results["min_sd_age"] = self.results["age"] - self.results["sd_age"]
        self.results["max_sd_age"] = self.results["age"] + self.results["sd_age"]
        if "group_count" in self.results:
            self.results["subject_count"] = self.results["group_count"].fillna(1)
        else:
            self.results["subject_count"] = 1

        self.results["url"] = self.results["study_sid"].apply(
            lambda x: f"{self.url}/data/{x}"
        )
        # self.results = self.results.replace({"NR", "not reported"}, regex=True)

        for column, replace_dict in replacements.items():
            self.results[column] = self.results[column].replace(replace_dict)

    def create_results_base(self):
        results = self.pkdata.outputs.copy()
        # FIXME: solve na values more generically
        results["method"] = results["method"].fillna(MISSING_VALUE)
        results["tissue"] = results["tissue"].fillna(MISSING_VALUE)

        results["per_bw"] = results.unit.str.endswith("/ kilogram")
        results["inferred"] = False
        self.results = results

    def add_intervention_info(self):
        intervention_table = self.create_intervention_extra()
        print(intervention_table)
        # intervention_table.unit = intervention_table.unit.astype(str)
        intervention_table["per_bw"] = intervention_table.unit.str.endswith(
            "/ kilogram"
        )
        intervention_table = intervention_table.rename(
            columns={"intervention_pk": "pk"}
        )
        self.results = pd.merge(
            self.results,
            intervention_table.add_prefix("intervention_"),
            on=self.intervention_pk,
            how="inner",
        )

    def individual_results(self):
        individual = "individuals"
        individual_table = self.create_subject_table(individual)
        individual_results = self.results[self.results.group_pk == -1]
        unique_individual_columns = set(individual_table.columns).difference(
            individual_results.columns
        )

        unique_individual_columns = [*unique_individual_columns, self.individual_pk]

        return pd.merge(
            individual_results,
            individual_table[unique_individual_columns],
            on=self.individual_pk,
            how="left",
        )

    def group_results(self):
        group = "groups"
        group_table = self.create_subject_table(group)
        group_results = self.results[self.results.individual_pk == -1]
        unique_group_columns = set(group_table.columns).difference(
            group_results.columns
        )
        unique_group_columns = [*unique_group_columns, self.group_pk]
        return pd.merge(
            group_results,
            group_table[unique_group_columns],
            on=self.group_pk,
            how="left",
        )

    def beautiful_units(self):
        raise NotImplementedError

    def add_subject_info(self):
        self.results = self.individual_results().df.append(self.group_results())

    def infer_from_body_weight(self, by_intervention=True, by_output=True):
        results_inferred = infer_weight(self.results, by_intervention, by_output)
        results_inferred["marker"] = results_inferred.apply(markers, axis=1)
        results_inferred["data_type"] = results_inferred.apply(data_type, axis=1)
        self.results = results_inferred

    def create_results(self):
        self.create_results_base()
        self.add_intervention_info()
        self.add_subject_info()
