"""
This module creates a summary table from an pkdata instance
"""
from copy import copy
from dataclasses import dataclass
import numpy as np
from pkdb_analysis.data import PKData
from pathlib import Path
import pandas as pd
from typing import Dict, Union, List


@dataclass
class Parameter:
    measurement_types: Union[str, List]
    value_field: str = "choice"
    substance: str = "any"


def all_size(study, pkdata):
    all_groups = pkdata.groups_core[pkdata.groups_core["group_name"] == "all"]

    group = all_groups[(all_groups["study_name"] == study.name)]

    assert len(group) == 1, (len(group), study.name, group)
    study["Subject size"] = group["group_count"]
    return study


def _has_info(df: pd.DataFrame, instance_id: str, parameter: Parameter, on):
    has_info = []
    if len(df) == 0:
        return None

    for group, instance in df.groupby(instance_id):
        if parameter.measurement_types == "any":
            specific_info = instance
        else:
            specific_info = instance[instance["measurement_type"].isin(parameter.measurement_types)]

        value_types = specific_info[parameter.value_field].apply(type).unique()

        has_array = False
        for value in value_types:
            if value is np.ndarray:
                has_array = True
                choices = {True}
        if not has_array:
            choices = set([i for i in specific_info[parameter.value_field] if i is not None])


        if len(choices) == 0:
            has_info.append(False)
        elif "NR" in set(choices):
            has_info.append(False)
        else:
            has_info.append(True)

    if not any(has_info) or len(has_info) == 0:
        return "-"
    elif all(has_info):
        return "✔️️"
    else:
        return "0"


def _add_information(study, pkdata, measurement_types: Dict, table: str, on="choice"):
    this_table = getattr(pkdata, table)
    this_table_df = this_table.df


    study_this_table = this_table_df[this_table_df["study_sid"] == study.sid]

    additional_dict = {key: _has_info(study_this_table, this_table.pk, name, on) for key, name in
                       measurement_types.items()}

    if table == "groups":
        all_group = study_this_table[study_this_table["group_name"] == "all"]
        subject_size = all_group.group_count.unique()
        additional_dict["Subject size"] = subject_size[0]



    return study.append(pd.Series(additional_dict))


def and_logic(series):
    elements = set([values for values in series.values if values is not None])
    if len(elements) == 1:
        return list(elements)[0]
    else:
        return "0"


def any_logic(series):
    elements = set([values for values in series.values if values is not None])
    if "✔️️" in elements:
        return "✔️️"
    else:
        return "-"




def _combine(df1, df2):
    merged = pd.merge(df1, df2, on="sid")

    for column in [c for c in df2.columns if c != "sid"]:
        keys = [f'{column}_x', f'{column}_y']
        merged[column] = merged[keys].apply(and_logic, axis=1)

    return merged[df1.columns]


def reporting_summary(pkdata: PKData, path: Path, report_type="basic", substances=[]):
    """ creates a summary table from a pkdata objects  and saves it to path
    :param pkdata:
    :return:
    """
    # rename
    studies = pkdata.studies
    studies["PMID"] = studies.reference.apply(lambda x: x["sid"])
    studies_keys = []

    if report_type == "basic":
        if len(substances) != 0:
            raise AssertionError("substance are not allowed on basic reporting type")


        subject_info = {
            "sex": Parameter(measurement_types=["sex"]),
            "age":Parameter(measurement_types=["age"]),
            "weight":Parameter(measurement_types=["weight"]),
            "height":Parameter(measurement_types=["height"]),
            "body mass index":Parameter(measurement_types=[ "bmi"]),
            "ethnicity":Parameter(measurement_types=["ethnicity"]),
            "CYP1A2 genotype":Parameter(measurement_types=["CYP1A2 genotype"]),

            # pk effecting factors
            "healthy":Parameter(measurement_types=["healthy"]),
            "medication":Parameter(measurement_types=["medication"]),
            "smoking":Parameter(measurement_types=["smoking"]),
            "oral contraceptives":Parameter(measurement_types=["oral contraceptives"]),
            "overnight fast":Parameter(measurement_types=["overnight fast"]),
            "abstinence alcohol":Parameter(measurement_types=["abstinence alcohol"])
        }
        s_keys = list(subject_info.keys())



        intervention_info = {
            "dosing amount": Parameter(measurement_types=["dosing", "qualitative dosing"], value_field="value"),
            "dosing route": Parameter(measurement_types=["dosing", "qualitative dosing"], value_field="route"),
            "dosing form": Parameter(measurement_types=["dosing", "qualitative dosing"], value_field="form"),
        }
        i_keys = list(intervention_info.keys())

        outputs_info = {
            "quantification method": Parameter(measurement_types="any", value_field="method"),
        }
        o_keys = list(outputs_info.keys())

        studies_keys.extend(["Name",
                             "PKDB identifier",
                             "PMID",
                             "publication date",
                             "Subject size"])

        for keys in [s_keys, i_keys, o_keys]:
            studies_keys.extend(copy(keys))
            keys.append("sid")




        studies_interventions = studies.df.apply(_add_information, args=(pkdata, intervention_info, "interventions"), axis=1)
        studies_group = studies.df.apply(_add_information, args=(pkdata, subject_info, "groups"), axis=1)
        studies_individuals = studies.df.apply(_add_information, args=(pkdata, subject_info, "individuals"), axis=1)
        studies = pd.merge(studies, _combine(studies_group[[*s_keys, "Subject size"]], studies_individuals[s_keys]), on="sid")
        studies = pd.merge(studies, studies_interventions[i_keys], on="sid")
        studies_outputs = studies.df.apply(_add_information, args=(pkdata, outputs_info, "outputs"), axis=1)
        studies_timecourses = studies.df.apply(_add_information, args=(pkdata, outputs_info, "timecourses"), axis=1)
        studies = pd.merge(studies, _combine(studies_outputs[o_keys], studies_timecourses[o_keys]))
        studies = studies.rename(columns={"sid": "PKDB identifier", "name": "Name", "reference_date":"publication date"})
        studies.sort_values(by="publication date", inplace=True)



    elif report_type == "pk":

        timecourse_fields = ["value", "mean", "median", "sd", "se", "cv"]

        timecourse_info = {}
        for substance in substances:
            for t_field in timecourse_fields:
                timecourse_info[f"{substance}_timecourses_{t_field}"] =  Parameter(measurement_types="any",
                                                                                  substance=substance,
                                                                                  value_field=t_field)

        studies = studies.df.apply(_add_information, args=(pkdata, timecourse_info, "timecourses"), axis=1)
        studies = studies.rename(columns={"sid": "PKDB identifier", "name": "Name"})

        studies_keys.extend(["Name","PKDB identifier",*timecourse_info.keys()])
        studies = studies.fillna("-")


    studies[studies_keys].to_excel(path)







