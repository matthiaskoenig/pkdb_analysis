"""
This module creates a summary table from an pkdata instance
"""

from pkdb_analysis.data import PKData
from pathlib import Path
import pandas as pd
from typing import Dict

def all_size(study, pkdata):
    all_groups = pkdata.groups_core[pkdata.groups_core["group_name"] == "all"]

    group =  all_groups[(all_groups["study_name"] == study.name) ]

    assert len(group) == 1, (len(group), study.name, group)
    study["Subject size"] = group["group_count"]
    return study


def has_info_categorial(df: pd.DataFrame, instance_id: str, measurement_type: str):
        instances = set(df[instance_id])
        has_info = []
        for group, instance in df.groupby(instance_id):
            specific_info =instance[instance["measurement_type"] == measurement_type]
            choices = set(specific_info["choice"])

            if len(choices) == 0:
                has_info.append(False)
            elif "NR" in set(choices):
                has_info.append(False)
            else:
                has_info.append(True)

        if all(has_info):
            return "✔️️"
        elif not any(has_info):
            return "-"
        else:
            return "0"

def _add_information(study, pkdata, measurement_types: Dict, table: str):

    this_table = getattr(pkdata, table)
    this_table_df = this_table.df

    study_this_table = this_table_df[this_table_df["study_sid"] == study.sid]


    additional_dict = {key: has_info_categorial(study_this_table, this_table.pk, name) for key, name in
                       measurement_types.items()}

    if table == "groups":
        all_group = study_this_table[study_this_table["group_name"] == "all"]
        subject_size = all_group.group_count.unique()
        additional_dict["Subject size"] = subject_size[0]

    return study.append(pd.Series(additional_dict))

def logic(series):
    elements = set(series.values)
    if len(elements) == 1:
        return list(elements)[0]
    else :
        return "0"


def _combine(df1, df2):
    df1.columns
    merged = pd.merge(df1, df2, on)
    for column in df1.columns:
        merged[column] = merged[[f'{column}_x', f'{column}_y']].apply(logic)

    return merged



def summary(pkdata: PKData, path: Path):
    """ creates a summary table from a pkdata objects  and saves it to path
    :param pkdata:
    :return:
    """
    #rename
    studies = pkdata.studies
    studies["PMID"] = studies.reference.apply(lambda x: x["sid"])
    subject_measurement_dict = {
        "healthy" : "healthy",
        "sex": "sex",
        "age": "age",
        "height": "height",
        "weight": "weight",
        "ethnicity": "ethnicity"
    }
    #print(pkdata.groups[pkdata.groups["study_name"] == "Abernethy1985"].group_name.unique())

    #all_group = pkdata.groups_core[pkdata.groups_core["group_name"] == "all"]
    #studies = studies.merge(all_group[["study_name", "group_count"]], "left", left_on="name", right_on="study_name")

    studies_group = studies.df.apply(_add_information, args=(pkdata, subject_measurement_dict, "groups"), axis=1)

    studies_individuals = studies.df.apply(_add_information, args=(pkdata, subject_measurement_dict, "individuals"), axis=1)
    s_keys = subject_measurement_dict.keys()


    studies[s_key] = _combine(studies_group[s_keys], studies_individuals[s_keys])
    studies["Subject size"] = studies_group["Subject size"]


    studies = studies.rename(columns={"sid": "PKDB identifier", "name":"Name"})# "group_count_y":"Subject size"})
    studies.sort_values(by="PKDB identifier", inplace=True)

    studies[["Name","PKDB identifier","PMID", "Subject size", *subject_measurement_dict.keys()]].to_excel(path)
