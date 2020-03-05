import pandas as pd

from pkdb_analysis.analysis import figure_category
from pkdb_analysis.filter import pk_info, f_healthy, f_n_healthy
from pkdb_analysis.weight_inference import infer_weight

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
        return "from body weight"
    else:
        return "from publication"

class MetaAnalysis(object):

    def __init__(self, pkdata,intervention_substance):
        self.pkdata = pkdata
        self.results = None
        self.group_pk = pkdata.groups.pk
        self.individual_pk = pkdata.individuals.pk
        self.intervention_pk = pkdata.interventions.pk
        self.intervention_substance = intervention_substance

    def specific_intervention_info(self, d):
        print(d)
        subset = d[d["substance"] == self.intervention_substance]
        subset["intervention_number"] = len(d)
        extra_info = []
        for intervention in d.intervention.iterrows():
            if intervention["measurement_type"] == "dosing":
                extra_info.append(intervention[["value", "unit", "substance", "route"]])
        subset["intervention_extra"] = extra_info
        if len(subset) == 1:
            return subset

    def create_intervention_table(self):
        intervention_table = pd.DataFrame()
        for intervention_pk, df in self.pkdata.interventions.df.groupby(self.intervention_pk):
            subset = df[df["substance"] == self.intervention_substance]
            subset["number"] = len(df)

            if len(subset) == 1:
                if len(df) > 1:
                    extra_info = []
                    for r, intervention in df.iterrows():
                        if intervention["measurement_type"] == "dosing":
                            extra_info.append(intervention[["value", "unit", "substance", "route"]])
                    extra = pd.concat(extra_info, axis=1).T

                    subset = subset.iloc[0]
                    subset["extra"] = extra
                intervention_table = intervention_table.append(subset)
        intervention_table["per_bodyweight"] = intervention_table.unit.str.endswith("/ kilogram")
        intervention_table["pk"] = intervention_table[self.intervention_pk].astype("int")
        del intervention_table["intervention_pk"]
        return intervention_table

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
            detail_info[categorial_field] = detail_info[categorial_field].fillna("unknown")
            subject_categorials_extra.append(detail_info)

        for individuals_info in [*subject_categorials_extra, *subject_numeric_extra]:
            subject_core = pd.merge(subject_core, individuals_info, on=subject_df.pk, how="left")

        return subject_core

    def add_extra_info(self):
        self.results["unit_category"] = self.results[["per_bodyweight", "intervention_per_bodyweight"]].apply(
            figure_category, axis=1)
        self.results["y"] = self.results[["mean", "median", "value"]].max(axis=1)
        self.results["y_min"] = self.results["y"] - self.results["sd"]
        self.results["y_max"] = self.results["y"] + self.results["sd"]

        # self.results["x_min"] = self.results["value_intervention"]-self.results["se_intervention"]
        # self.results["x_max"] = self.results["value_intervention"]+self.results["se_intervention"]

        # self.results["p_unit"] = self.results["unit"].apply(lambda x: f'{ureg(x).u: ~P}')
        # self.results["p_unit_intervention"] = self.results["unit_intervention"].apply(lambda x: f'{ureg(x).u: ~P}')

        self.results["weight"] = self.results[["mean_weight", "median_weight", "value_weight"]].max(axis=1)
        self.results["min_sd_weight"] = self.results["weight"] - self.results["sd_weight"]
        self.results["max_sd_weight"] = self.results["weight"] + self.results["sd_weight"]

        self.results["age"] = self.results[["mean_age", "median_age", "value_age"]].max(axis=1)
        self.results["min_sd_age"] = self.results["age"] - self.results["sd_age"]
        self.results["max_sd_age"] = self.results["age"] + self.results["sd_age"]

        self.results["subject_count"] = self.results["group_count"].fillna(1)

        self.results["url"] = self.results["study_sid"].apply(lambda x: f"http://0.0.0.0:8081/studies/{x}")


    def create_results_base(self):
        results = self.pkdata.outputs.copy()
        results["per_bodyweight"] = results.unit.str.endswith("/ kilogram")
        results["inferred"] = False
        self.results = results

    def add_intervention_info(self):
        intervention_table = self.create_intervention_table()
        self.results = pd.merge(self.results, intervention_table.add_prefix('intervention_'), on=self.intervention_pk,
                                how="inner")

    def individual_results(self):
        individual = "individuals"
        individual_table = self.create_subject_table(individual)
        individual_results = self.results[self.results.group_pk == -1]
        return pd.merge(individual_results, individual_table, on=self.individual_pk, how="left")

    def group_results(self):
        group = "groups"
        group_table = self.create_subject_table(group)
        group_results = self.results[self.results.group_pk != -1]
        return pd.merge(group_results, group_table, on=self.group_pk, how="left")

    def add_subject_info(self):
        self.results = self.individual_results().df.append(self.group_results())

    def infer_from_body_weight(self):


        results_inferred = infer_weight(self.results)
        results_inferred["marker"] = results_inferred.apply(markers, axis=1)
        results_inferred["data_type"] = results_inferred.apply(data_type, axis=1)
        self.results = results_inferred

    def create_results(self):
        self.create_results_base()
        self.add_intervention_info()
        self.add_subject_info()
