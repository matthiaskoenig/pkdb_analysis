"""
This module creates a summary table from an pkdata instance
"""
from copy import copy
from dataclasses import dataclass
import numpy as np
from pkdb_analysis.data import PKData
from pathlib import Path
import pandas as pd
from typing import Dict, Union, List, Sequence


@dataclass
class Parameter:
    measurement_types: Union[str, List]
    value_field: Sequence
    substance: str = "any"
    values: Sequence = ("any",)
    only_group: bool = False
    only_individual: bool = False

def all_size(study, pkdata):
    all_groups = pkdata.groups_core[pkdata.groups_core["group_name"] == "all"]

    group = all_groups[(all_groups["study_name"] == study.name)]

    assert len(group) == 1, (len(group), study.name, group)
    study["Subject size"] = group["group_count"]
    return study


def _has_info(df: pd.DataFrame, instance_id: str, parameter: Parameter, Subjects_groups: int=0 , Subjects_individual: int=0):
    has_info = []
    compare_length = 0
    if parameter.substance != "any":
        df = df[df["substance"] == parameter.substance]
        
    if parameter.only_group:
        df = df[df["individual_pk"] == -1]
        instance_id = "group_pk"
        compare_length = Subjects_groups
        
    if parameter.only_individual:

        df = df[df["group_pk"] == -1]
        instance_id = "individual_pk"
        compare_length = Subjects_individual
        

    if len(df) == 0:
        return None

    for _ , instance in df.groupby(instance_id):
        if parameter.measurement_types == "any":
            specific_info = instance
        else:
            specific_info = instance[instance["measurement_type"].isin(parameter.measurement_types)]
            

        value_types = specific_info[parameter.value_field].applymap(type).stack().unique()

        has_array = False
        for value in value_types:
            if value is np.ndarray:
              
                has_array = True
                choices = {True}
        
        if not has_array:
            this_series = specific_info[parameter.value_field].max(axis=1)
            choices = set([i for i in this_series.dropna() if i is not None])
            
        if "any" not in parameter.values:
            print(choices)
            choices = choices & set(parameter.values)
            print(choices)
            print(set(parameter.values))


        if len(choices) == 0:
            has_info.append(False)
        elif "NR" in set(choices):
            has_info.append(False)
        else:
            has_info.append(True)

    if not any(has_info) or len(has_info) == 0:
        return " "
    
    elif all(has_info):
        if compare_length > 0:
            if len(has_info) == compare_length:
                return "✓"
        else:
            return "✓"
    return "⅟"


def _add_information(study, pkdata, measurement_types: Dict, table: str):

    additional_dict = {}

    used_pkdata = pkdata.filter_study(lambda x: x["sid"] == study.sid)
    this_table = getattr(used_pkdata, table)
    has_info_kwargs = {"df":this_table.df, "instance_id":this_table.pk}
    group_df_df = pkdata.groups.df
    study_group_df = group_df_df[group_df_df["study_sid"] == study.sid]
    all_group = study_group_df[study_group_df["group_name"] == "all"]
    subject_size = all_group.group_count.unique()[0]
    has_info_kwargs["Subjects_individual"] = subject_size
    has_info_kwargs["Subjects_groups"] = len(used_pkdata.groups.pks)

    if table == "groups":
        additional_dict["Subjects_individual"] =  has_info_kwargs["Subjects_individual"]
        additional_dict["Subjects_groups"] = has_info_kwargs["Subjects_groups"]




    additional_dict = {**{key: _has_info(parameter=parameter,**has_info_kwargs) for key, parameter in
                       measurement_types.items()}, **additional_dict}




    return study.append(pd.Series(additional_dict))

def strict_and_logic(series):
    elements = set(series.dropna().values)
    if len(elements) == 1:
        return list(elements)[0]
    else:
        return " "

def and_logic(series):
    elements = set(series.dropna().values)
    if len(elements) == 1:
        return list(elements)[0]
    else:
        return "⅟"


def any_logic(series):
    elements = set([values for values in series.values if values is not None])
    if "✓" in elements:
        return "✓"
    else:
        return " "




def _combine(df1, df2):
    merged = pd.merge(df1, df2, on="sid")

    for column in [c for c in df2.columns if c != "sid"]:
        keys = [f'{column}_x', f'{column}_y']
        merged[column] = merged[keys].apply(and_logic, axis=1)

    return merged[df1.columns]
def extend_study_keys(study_keys):
    return  study_keys.extend(["PKDB identifier",
                             "Name",
                             "PMID",
                             "publication date",
                             "Subjects_individual",
                             "Subjects_groups"])


def reporting_summary(pkdata: PKData, path: Path, report_type="basic", substances=[]):
    """ creates a summary table from a pkdata objects  and saves it to path
    :param pkdata:
    :return:
    """
    # rename
    studies = pkdata.studies
    studies["PMID"] = studies.reference.apply(lambda x: x["sid"])
    study_keys = []
    study_keys.extend(["PKDB identifier",
                       "Name",
                       "PMID",
                       "publication date",])
    
    if report_type == "basic":
        if len(substances) != 0:
            raise AssertionError("substance are not allowed on basic reporting type")


        subject_info = {
            "sex": Parameter(measurement_types=["sex"],value_field=["choice"]),
            "age":Parameter(measurement_types=["age"], value_field=["mean","median","value"]),
            "weight":Parameter(measurement_types=["weight"], value_field=["mean","median","value"]),
            "height":Parameter(measurement_types=["height"], value_field=["mean","median","value"]),
            "body mass index":Parameter(measurement_types=[ "bmi"], value_field=["mean","median","value"]),
            "ethnicity":Parameter(measurement_types=["ethnicity"],value_field=["choice"]),

            # pk effecting factors
            "healthy":Parameter(measurement_types=["healthy"],value_field=["choice"]),
            "medication":Parameter(measurement_types=["medication"],value_field=["choice"]),
            "smoking":Parameter(measurement_types=["smoking"],value_field=["choice"]),
            "oral contraceptives":Parameter(measurement_types=["oral contraceptives"],value_field=["choice"]),
            "overnight fast":Parameter(measurement_types=["overnight fast"],value_field=["choice"]),
            "CYP1A2 genotype": Parameter(measurement_types=["CYP1A2 genotype"],value_field=["choice"]),
            "abstinence alcohol":Parameter(measurement_types=["abstinence alcohol"], value_field=["mean","median","value","min","max"])
        }
        s_keys = list(subject_info.keys())



        intervention_info = {
            "dosing amount": Parameter(measurement_types=["dosing", "qualitative dosing"], value_field=["value"]),
            "dosing route": Parameter(measurement_types=["dosing", "qualitative dosing"], value_field=["route"]),
            "dosing form": Parameter(measurement_types=["dosing", "qualitative dosing"], value_field=["form"]),
        }
        i_keys = list(intervention_info.keys())

        outputs_info = {
            "quantification method": Parameter(measurement_types="any", value_field=["method"]),
        }
        o_keys = list(outputs_info.keys())

        study_keys.extend(["Subjects_individual",
                             "Subjects_groups"])

        for keys in [s_keys, i_keys, o_keys]:
            study_keys.extend(copy(keys))
            keys.append("sid")




        studies_interventions = studies.df.apply(_add_information, args=(pkdata, intervention_info, "interventions"), axis=1)
        studies_group = studies.df.apply(_add_information, args=(pkdata, subject_info, "groups"), axis=1)
        studies_group[["Subjects_individual", "Subjects_groups"]] = studies_group[["Subjects_individual", "Subjects_groups"]].astype(int)
        studies_individuals = studies.df.apply(_add_information, args=(pkdata, subject_info, "individuals"), axis=1)
        studies = pd.merge(studies, _combine(studies_group[[*s_keys, "Subjects_individual", "Subjects_groups"]], studies_individuals[s_keys]), on="sid")
        studies = pd.merge(studies, studies_interventions[i_keys], on="sid")
        studies_outputs = studies.df.apply(_add_information, args=(pkdata, outputs_info, "outputs"), axis=1)
        studies_timecourses = studies.df.apply(_add_information, args=(pkdata, outputs_info, "timecourses"), axis=1)
        studies = pd.merge(studies, _combine(studies_outputs[o_keys], studies_timecourses[o_keys]))


        studies = studies.rename(columns={"sid": "PKDB identifier", "name": "Name", "reference_date":"publication date"})


 



    elif report_type == "timecourse":
        timecourse_fields = {
            "individual":{"value_field":["value"], "only_individual":True},
            "mean": {"value_field": [ "mean", "median"], "only_group": True },
            "error": {"value_field": ["sd", "se", "cv"], "only_group": True },
            "plasma/blood": {"value_field": ["tissue"], "values": ["plasma","blood","serum"]},
            "urine": {"value_field": ["tissue"], "values": ["urine"]},
            "saliva": {"value_field": ["tissue"], "values": ["saliva"]},
        }

        timecourse_info = {
            
            
            
        }
        keys = []
        for substance in substances:
            for key, p_kwargs in timecourse_fields.items():
                this_key = f"{substance}_timecourses_{key}"
                timecourse_info[this_key] =  Parameter(measurement_types="any", substance=substance, **p_kwargs)
                keys.append(this_key)

        studies = studies.df.apply(_add_information, args=(pkdata, timecourse_info, "timecourses"), axis=1)
        studies = studies.rename(columns={"sid": "PKDB identifier", "name": "Name"})
        study_keys.extend(keys)
        studies = studies.fillna(" ")
        
    studies = studies.rename(columns={"sid": "PKDB identifier", "name": "Name", "reference_date": "publication date"})

    studies["PKDB identifier"] = studies["PKDB identifier"].apply(
        lambda x: f'=HYPERLINK("https://develop.pk-db.com/{x}/";"{x}")')
    studies["PMID"] = studies["PMID"].apply(lambda x: f'=HYPERLINK("https://www.ncbi.nlm.nih.gov/pubmed/{x}";"{x}")')

    studies.sort_values(by="publication date", inplace=True)

    if str(path).endswith(".xlsx"):
        studies[study_keys].to_excel(path)

    elif str(path).endswith(".tsv"):
        studies[study_keys].to_csv(path, sep='\t')
    else:
        raise AssertionError("wrong path ending (tsv and xlsx are supported")





