"""
This module creates a summary table from an pkdata instance
"""
from dataclasses import dataclass

from pkdb_analysis.data import PKData
from pathlib import Path
import pandas as pd
from typing import Dict, Union, List


@dataclass
class Parameter:
    measurement_types: List[str]
    value_field: str


def all_size(study, pkdata):
    all_groups = pkdata.groups_core[pkdata.groups_core["group_name"] == "all"]

    group = all_groups[(all_groups["study_name"] == study.name)]

    assert len(group) == 1, (len(group), study.name, group)
    study["Subject size"] = group["group_count"]
    return study


def _has_info(df: pd.DataFrame, instance_id: str, measurement_type: Union[str, List, Parameter], on):
    has_info = []
    if len(df) == 0:
        return None
    for group, instance in df.groupby(instance_id):
        if isinstance(measurement_type,str):
            specific_info = instance[instance["measurement_type"] == measurement_type]
            choices = set(specific_info[on])

        elif isinstance(measurement_type, Parameter):
            if measurement_type.measurement_types == "any":
                specific_info = instance
            else:
                specific_info = instance[instance["measurement_type"].isin(measurement_type.measurement_types)]
            choices = set(specific_info[measurement_type.value_field])
        else:
            raise TypeError("The measurement:type parameter should be either a string or a Parameter")


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


def logic(series):
    elements = set([values for values in series.values if values is not None])
    if len(elements) == 1:
        return list(elements)[0]
    else:
        return "0"


def _combine(df1, df2):
    merged = pd.merge(df1, df2, on="sid")

    for column in [c for c in df2.columns if c != "sid"]:
        keys = [f'{column}_x', f'{column}_y']
        merged[column] = merged[keys].apply(logic, axis=1)

    return merged[df1.columns]


def summary(pkdata: PKData, path: Path):
    """ creates a summary table from a pkdata objects  and saves it to path
    :param pkdata:
    :return:
    """
    # rename
    studies = pkdata.studies
    studies["PMID"] = studies.reference.apply(lambda x: x["sid"])
    subject_measurement_dict = {
        "sex": "sex",
        "age": "age",
        "weight": "weight",
        "height": "height",
        "body mass index": "bmi",
        "ethnicity": "ethnicity",
        "CYP1A2 genotype": "CYP1A2 genotype",

        # pk effecting factors
        "healthy": "healthy",
        "medication": "medication",
        "smoking": "smoking",
        "oral contraceptives": "oral contraceptives",
        "overnight fast": "overnight fast",
        "abstinence alcohol": "abstinence alcohol"
    }

    intervention_measurement = {
        "dosing amount": Parameter(measurement_types=["dosing", "qualitative dosing"], value_field="value"),
        "dosing route": Parameter(measurement_types=["dosing", "qualitative dosing"], value_field="route"),
        "dosing form": Parameter(measurement_types=["dosing", "qualitative dosing"], value_field="form"),
    }

    studies_interventions = studies.df.apply(_add_information, args=(pkdata, intervention_measurement, "interventions"), axis=1)


    studies_group = studies.df.apply(_add_information, args=(pkdata, subject_measurement_dict, "groups"), axis=1)
    studies_individuals = studies.df.apply(_add_information, args=(pkdata, subject_measurement_dict, "individuals"),
                                           axis=1)
    s_keys = list(subject_measurement_dict.keys())
    s_keys.append("sid")

    studies = pd.merge(studies, _combine(studies_group[[*s_keys, "Subject size"]], studies_individuals[s_keys]),
                       on="sid")


    i_keys = list(intervention_measurement.keys())
    i_keys.append("sid")

    studies = pd.merge(studies, studies_interventions[i_keys], on="sid")

    outputs_info = {
        "quantification method": Parameter(measurement_types="any", value_field="method"),
    }
    o_keys = list(outputs_info.keys())
    o_keys.append("sid")

    studies_outputs = studies.df.apply(_add_information, args=(pkdata, outputs_info, "outputs"), axis=1)
    studies_timecourses = studies.df.apply(_add_information, args=(pkdata, outputs_info, "timecourses"), axis=1)
    print(studies_timecourses)
    studies = pd.merge(studies, _combine(studies_outputs[o_keys], studies_timecourses[o_keys]))


    studies = studies.rename(columns={"sid": "PKDB identifier", "name": "Name", "reference_date":"publication date"})

    studies.sort_values(by="publication date", inplace=True)
    #studies.sort_values(by="PKDB identifier", inplace=True)


    studies[["Name",
             "PKDB identifier",
             "PMID",
             "publication date",
             "Subject size",
             *subject_measurement_dict.keys(),
             *intervention_measurement.keys(),
             *outputs_info.keys()]].to_excel(path)
