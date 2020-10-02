import pandas as pd
import numpy as np

from pkdb_analysis.analysis import figure_category
from pkdb_analysis.filter import pk_info, f_healthy, f_n_healthy
from pkdb_analysis.inference.body_weight import infer_weight

INTERVENTION_FIELDS = ["substance", "value", "unit", "route", "form", "application"]
NUMERIC_FIELDS_NO_VALUE = ["mean", "min", "max", "median", "count", "sd", "se", "unit"]
NUMERIC_FIELDS = ["value"] + NUMERIC_FIELDS_NO_VALUE


def one_intervention(d):
    if len(d) == 1:
        return d



def validate_1len(d):
    assert 1 == len(d[d]), d
    return d


def markers(d):
    if d["calculated"]:
        return "s"
    elif d["inferred"]:
        return "v"
    else:
        return "o"


def data_type(d):
    if d["calculated"]:
        return "from timecourse"
    elif d["inferred"]:
        return "from bodyweight"
    else:
        return "publication"

class MetaAnalysis(object):

    def __init__(self, pkdata,intervention_substances, url):
        self.pkdata = pkdata
        self.results = None
        self.group_pk = pkdata.groups.pk
        self.individual_pk = pkdata.individuals.pk
        self.intervention_pk = pkdata.interventions.pk
        self.intervention_substances = intervention_substances
        self.url = url


    def _create_extra_table(self, table_name, substances):

        table = getattr(self.pkdata, table_name)
        _table = pd.DataFrame()
        for table_pk, df in table.df.groupby(table.pk):
            subset = df[df["substance"].isin(substances)]
            subset["number"] = len(df)
            if len(subset) == 1:
                subset = subset.iloc[0]
                subset["extra"] = df
                _table = _table.append(subset)
        return _table

    def _add(self,df, measurement_type):
        age_data = df.extra[df.extra["measurement_type"] == measurement_type]
        if len(age_data) == 1:
            return tuple(age_data.iloc[0][NUMERIC_FIELDS].values)
        else:
            return tuple([np.nan for _ in NUMERIC_FIELDS])


    @property
    def healthy_data(self):
        return self.pkdata.filter_subject(f_healthy).exclude_subject(f_n_healthy)

    def create_subject_table(self, subject, numeric_fields=("weight", "age"), catgorial_fields=("sex",),
                             add_healthy=True):

        subject_core = getattr(self.pkdata, f"{subject}_core")
        subject_df = getattr(self.pkdata, subject)

        if add_healthy:
            healthy_subjects_pks = getattr(self.healthy_data, subject).pks
            subject_core["healthy"] = subject_core[subject_df.pk].isin(healthy_subjects_pks)

        subject_numeric_extra = [pk_info(subject_df, numeric_field, NUMERIC_FIELDS) for numeric_field in
                                 numeric_fields]
        subject_categorials_extra = []
        for categorial_field in catgorial_fields:
            detail_info = pk_info(subject_df, categorial_field, ["choice"]).rename(
                columns={f"choice_{categorial_field}": categorial_field})
            subject_categorials_extra.append(detail_info)

        for individuals_info in [*subject_categorials_extra, *subject_numeric_extra]:
            subject_core = pd.merge(subject_core, individuals_info, on=subject_df.pk, how="left")

        for categorial_field in catgorial_fields:
            subject_core[categorial_field] = subject_core[categorial_field].fillna("unknown")

        pk = subject_df.pk
        subject_core["extra"] = getattr(subject_core,pk).apply(lambda x: subject_df[subject_df[pk] == x])
        for measurement_type in  ["age","weight"]:
            subject_extra = subject_core.apply(self._add, args=(measurement_type, ), axis=1, result_type="expand")
            if subject_extra.empty:
                subject_core[[f"{k}_{measurement_type}" for k in NUMERIC_FIELDS]] = tuple([np.nan for _ in NUMERIC_FIELDS])
            else:
                subject_core[[f"{k}_{measurement_type}" for k in NUMERIC_FIELDS]] = subject_extra

        return subject_core

    def add_extra_info(self, replacements):
        self.results["unit_category"] = self.results[["per_bw", "intervention_per_bw"]].apply(
            figure_category, axis=1)
        self.results["y"] = self.results[["mean", "median", "value"]].max(axis=1)
        self.results["y_min"] = self.results["y"] - self.results["sd"]
        self.results["y_max"] = self.results["y"] + self.results["sd"]

        self.results["weight"] = self.results[["mean_weight", "median_weight", "value_weight"]].max(axis=1)
        self.results["min_sd_weight"] = self.results["weight"] - self.results["sd_weight"]
        self.results["max_sd_weight"] = self.results["weight"] + self.results["sd_weight"]

        self.results["age"] = self.results[["mean_age", "median_age", "value_age"]].max(axis=1)
        self.results["min_sd_age"] = self.results["age"] - self.results["sd_age"]
        self.results["max_sd_age"] = self.results["age"] + self.results["sd_age"]

        self.results["subject_count"] = self.results["group_count"].fillna(1)

        self.results["url"] = self.results["study_sid"].apply(lambda x: f"{self.url}/studies/{x}")
        #self.results = self.results.replace({"NR", "not reported"}, regex=True)

        for column, replace_dict in replacements.items():
            self.results[column] = self.results[column].replace(replace_dict)

    def create_results_base(self):
        results = self.pkdata.outputs.copy()
        results["per_bw"] = results.unit.str.endswith("/ kilogram")
        results["inferred"] = False
        self.results = results

    def add_intervention_info(self):
        intervention_table = self._create_extra_table("interventions", self.intervention_substances)
        intervention_table["per_bw"] = intervention_table.unit.str.endswith("/ kilogram")
        intervention_table = intervention_table.rename(columns={"intervention_pk":"pk"})
        self.results = pd.merge(self.results, intervention_table.add_prefix('intervention_'), on=self.intervention_pk,
                                how="inner")

    def individual_results(self):
        individual = "individuals"
        individual_table = self.create_subject_table(individual)
        individual_results = self.results[self.results.group_pk == -1]
        unique_individual_columns = set(individual_table.columns).difference(individual_results.columns)

        unique_individual_columns = [*unique_individual_columns,self.individual_pk]

        return pd.merge(individual_results, individual_table[unique_individual_columns], on=self.individual_pk, how="left")

    def group_results(self):
        group = "groups"
        group_table = self.create_subject_table(group)
        group_results = self.results[self.results.group_pk != -1]
        unique_group_columns = set(group_table.columns).difference(group_results.columns)
        unique_group_columns = [*unique_group_columns,self.group_pk]
        return pd.merge(group_results, group_table[unique_group_columns], on=self.group_pk, how="left")

    def add_subject_info(self):

        self.results = self.individual_results().df.append(self.group_results())

    def infer_from_body_weight(self,  by_intervention=True, by_output=True):
        results_inferred = infer_weight(self.results, by_intervention, by_output)
        results_inferred["marker"] = results_inferred.apply(markers, axis=1)
        results_inferred["data_type"] = results_inferred.apply(data_type, axis=1)
        self.results = results_inferred

    def create_results(self):
        self.create_results_base()
        self.add_intervention_info()
        self.add_subject_info()


