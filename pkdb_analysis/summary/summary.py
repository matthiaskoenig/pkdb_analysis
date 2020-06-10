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
from gspread_pandas import Spread


@dataclass
class Parameter:
    measurement_types: Union[str, List] = "any"
    value_field: Sequence = "choice"
    substance: str = "any"
    values: Sequence = ("any",)
    only_group: bool = False
    only_individual: bool = False
    groupby: bool = True

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
        
    if not parameter.groupby:
        instance_id = "study_name"
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
            choices = choices & set(parameter.values)
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

def basics_table(studies, substances, pkdata, study_keys):

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

        intervention_info = {
            "dosing amount": Parameter(measurement_types=["dosing", "qualitative dosing"], value_field=["value"]),
            "dosing route": Parameter(measurement_types=["dosing", "qualitative dosing"], value_field=["route"]),
            "dosing form": Parameter(measurement_types=["dosing", "qualitative dosing"], value_field=["form"]),
        }

        outputs_info = {
            "quantification method": Parameter(measurement_types="any", value_field=["method"]),
        }

        s_keys = list(subject_info.keys())
        i_keys = list(intervention_info.keys())
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
        return studies, study_keys

def timecourses_table(studies, substances, pkdata, study_keys):
    timecourse_fields = {
        "individual": {"value_field": ["value"], "only_individual": True},
        "group": {"value_field": ["mean", "median"], "only_group": True},
        "error": {"value_field": ["sd", "se", "cv"], "only_group": True},
        "plasma/blood": {"value_field": ["tissue"], "values": ["plasma", "blood", "serum"], "groupby": False},
        "urine": {"value_field": ["tissue"], "values": ["urine"], "groupby": False},
        "saliva": {"value_field": ["tissue"], "values": ["saliva"], "groupby": False},
    }
    timecourse_info = {}
    for substance in substances:
        for key, p_kwargs in timecourse_fields.items():
            this_key = f"{substance}_timecourses_{key}"
            timecourse_info[this_key] = Parameter(measurement_types="any", substance=substance, **p_kwargs)
            study_keys.append(this_key)

    studies = studies.df.apply(_add_information, args=(pkdata, timecourse_info, "timecourses"), axis=1)
    studies = studies.fillna(" ")

    return studies, study_keys

def pks_table(studies, substances, pkdata, study_keys):
    pks_info = {}
    for substance in substances:
        pks_info_substance = {
            f"caffeine_plasma/blood": Parameter(substance="caffeine", value_field=["tissue"],values=["plasma", "blood", "serum"], groupby= False),
            f"{substance}_urine": Parameter(substance=f"{substance}", value_field=["tissue"],values=["urine"], groupby= False),
            f"{substance}_saliva": Parameter(substance=f"{substance}", value_field=["tissue"],values=["saliva"], groupby= False),
            f"{substance}_vd_individual": Parameter(measurement_types=["vd"], substance=f"{substance}", value_field=["value"], only_individual=True),
            f"{substance}_vd_group": Parameter(measurement_types=["vd"], substance=f"{substance}", value_field=["mean", "median"], only_group=True),
            f"{substance}_vd_error": Parameter(measurement_types=["vd"], substance=f"{substance}", value_field=["sd", "se", "cv"], only_group=True),
            f"{substance}_clearance_individual": Parameter(measurement_types=["clearance"], substance=f"{substance}", value_field=["value"], only_individual=True),
            f"{substance}_clearance_group": Parameter(measurement_types=["clearance"], substance=f"{substance}", value_field=["mean", "median"],only_group=True),
            f"{substance}_clearance_error": Parameter(measurement_types=["clearance"], substance=f"{substance}", value_field=["sd", "se", "cv"], only_group=True),
            f"{substance}_auc_individual": Parameter(measurement_types=["auc_end", "auc_inf"], substance=f"{substance}",value_field=["value"], only_individual=True),
            f"{substance}_auc_group": Parameter(measurement_types=["auc_end", "auc_inf"], substance=f"{substance}", value_field=["mean", "median"], only_group=True),
            f"{substance}_auc_error": Parameter(measurement_types=["auc_end", "auc_inf"], substance=f"{substance}",value_field=["sd", "se", "cv"], only_group=True),
            f"{substance}_thalf_individual": Parameter(measurement_types=["thalf"], substance=f"{substance}", value_field=["value"], only_individual=True),
            f"{substance}_thalf_group": Parameter(measurement_types=["thalf"], substance=f"{substance}",value_field=["mean", "median"], only_group=True),
            f"{substance}_thalf_error": Parameter(measurement_types=["thalf"], substance=f"{substance}",value_field=["sd", "se", "cv"], only_group=True),
            f"{substance}_cmax_individual": Parameter(measurement_types=["cmax"], substance=f"{substance}", value_field=["value"],only_individual=True),
            f"{substance}_cmax_group": Parameter(measurement_types=["cmax"], substance=f"{substance}",value_field=["mean", "median"], only_group=True),
            f"{substance}_cmax_error": Parameter(measurement_types=["cmax"], substance=f"{substance}",value_field=["sd", "se", "cv"], only_group=True),
            f"{substance}_tmax_individual": Parameter(measurement_types=["tmax"], substance=f"{substance}", value_field=["value"],only_individual=True),
            f"{substance}_tmax_group": Parameter(measurement_types=["tmax"], substance=f"{substance}", value_field=["mean", "median"], only_group=True),
            f"{substance}_tmax_error": Parameter(measurement_types=["tmax"], substance=f"{substance}",value_field=["sd", "se", "cv"], only_group=True),
            f"{substance}_kel_individual": Parameter(measurement_types=["kel"], substance=f"{substance}", value_field=["value"],only_individual=True),
            f"{substance}_kel_group": Parameter(measurement_types=["kel"], substance=f"{substance}",value_field=["mean", "median"], only_group=True),
            f"{substance}_kel_error": Parameter(measurement_types=["kel"], substance=f"{substance}",value_field=["sd", "se", "cv"], only_group=True)
        }
        pks_info = {**pks_info, **pks_info_substance}

    """  
        pks_info = { 
        "caffeine_plasma/blood": Parameter(substance="caffeine", value_field=["tissue"],values=["plasma", "blood", "serum"], groupby= False),
        "caffeine_urine": Parameter(substance="caffeine", value_field=["tissue"],values=["urine"], groupby= False),
        "caffeine_saliva": Parameter(substance="caffeine", value_field=["tissue"],values=["saliva"], groupby= False),
        "caffeine_vd_individual": Parameter(measurement_types=["vd"], substance="caffeine", value_field=["value"], only_individual=True),
        "caffeine_vd_group": Parameter(measurement_types=["vd"], substance="caffeine", value_field=["mean", "median"], only_group=True),
        "caffeine_vd_error": Parameter(measurement_types=["vd"], substance="caffeine", value_field=["sd", "se", "cv"], only_group=True),
        "caffeine_clearance_individual": Parameter(measurement_types=["clearance"], substance="caffeine", value_field=["value"], only_individual=True),
        "caffeine_clearance_group": Parameter(measurement_types=["clearance"], substance="caffeine", value_field=["mean", "median"],only_group=True),
        "caffeine_clearance_error": Parameter(measurement_types=["clearance"], substance="caffeine", value_field=["sd", "se", "cv"], only_group=True),
        "caffeine_auc_individual": Parameter(measurement_types=["auc_end", "auc_inf"], substance="caffeine",value_field=["value"], only_individual=True),
        "caffeine_auc_group": Parameter(measurement_types=["auc_end", "auc_inf"], substance="caffeine", value_field=["mean", "median"], only_group=True),
        "caffeine_auc_error": Parameter(measurement_types=["auc_end", "auc_inf"], substance="caffeine",value_field=["sd", "se", "cv"], only_group=True),
        "caffeine_thalf_individual": Parameter(measurement_types=["thalf"], substance="caffeine", value_field=["value"], only_individual=True),
        "caffeine_thalf_group": Parameter(measurement_types=["thalf"], substance="caffeine",value_field=["mean", "median"], only_group=True),
        "caffeine_thalf_error": Parameter(measurement_types=["thalf"], substance="caffeine",value_field=["sd", "se", "cv"], only_group=True),
        "caffeine_cmax_individual": Parameter(measurement_types=["cmax"], substance="caffeine", value_field=["value"],only_individual=True),
        "caffeine_cmax_group": Parameter(measurement_types=["cmax"], substance="caffeine",value_field=["mean", "median"], only_group=True),
        "caffeine_cmax_error": Parameter(measurement_types=["cmax"], substance="caffeine",value_field=["sd", "se", "cv"], only_group=True),
        "caffeine_tmax_individual": Parameter(measurement_types=["tmax"], substance="caffeine", value_field=["value"],only_individual=True),
        "caffeine_tmax_group": Parameter(measurement_types=["tmax"], substance="caffeine", value_field=["mean", "median"], only_group=True),
        "caffeine_tmax_error": Parameter(measurement_types=["tmax"], substance="caffeine",value_field=["sd", "se", "cv"], only_group=True),
        "caffeine_kel_individual": Parameter(measurement_types=["kel"], substance="caffeine", value_field=["value"],only_individual=True),
        "caffeine_kel_group": Parameter(measurement_types=["kel"], substance="caffeine",value_field=["mean", "median"], only_group=True),
        "caffeine_kel_error": Parameter(measurement_types=["kel"], substance="caffeine",value_field=["sd", "se", "cv"], only_group=True),


        #paraxanthine
        "paraxanthine_plasma/blood": Parameter(substance="paraxanthine", value_field=["tissue"],values=["plasma", "blood", "serum"], groupby=False),
        "paraxanthine_urine": Parameter(substance="paraxanthine", value_field=["tissue"], values=["urine"], groupby=False),
        "paraxanthine_saliva": Parameter(substance="paraxanthine", value_field=["tissue"], values=["saliva"], groupby=False),
        "paraxanthine_vd_individual": Parameter(measurement_types=["vd"], substance="paraxanthine", value_field=["value"],only_individual=True),
        "paraxanthine_vd_group": Parameter(measurement_types=["vd"], substance="paraxanthine", value_field=["mean", "median"],only_group=True),
        "paraxanthine_vd_error": Parameter(measurement_types=["vd"], substance="paraxanthine", value_field=["sd", "se", "cv"], only_group=True),
        "paraxanthine_clearance_individual": Parameter(measurement_types=["clearance"], substance="paraxanthine", value_field=["value"], only_individual=True),
        "paraxanthine_clearance_group": Parameter(measurement_types=["clearance"], substance="paraxanthine", value_field=["mean", "median"], only_group=True),
        "paraxanthine_clearance_error": Parameter(measurement_types=["clearance"], substance="paraxanthine", value_field=["sd", "se", "cv"], only_group=True),
        "paraxanthine_auc_individual": Parameter(measurement_types=["auc_end", "auc_inf"], substance="paraxanthine", value_field=["value"], only_individual=True),
        "paraxanthine_auc_group": Parameter(measurement_types=["auc_end", "auc_inf"], substance="paraxanthine",value_field=["mean", "median"], only_group=True),
        "paraxanthine_auc_error": Parameter(measurement_types=["auc_end", "auc_inf"], substance="paraxanthine",value_field=["sd", "se", "cv"], only_group=True),
        "paraxanthine_thalf_individual": Parameter(measurement_types=["thalf"], substance="paraxanthine", value_field=["value"],only_individual=True),
        "paraxanthine_thalf_group": Parameter(measurement_types=["thalf"], substance="paraxanthine", value_field=["mean", "median"], only_group=True),
        "paraxanthine_thalf_error": Parameter(measurement_types=["thalf"], substance="paraxanthine",value_field=["sd", "se", "cv"], only_group=True),
        "paraxanthine_cmax_individual": Parameter(measurement_types=["cmax"], substance="paraxanthine", value_field=["value"],only_individual=True),
        "paraxanthine_cmax_group": Parameter(measurement_types=["cmax"], substance="paraxanthine",value_field=["mean", "median"], only_group=True),
        "paraxanthine_cmax_error": Parameter(measurement_types=["cmax"], substance="paraxanthine",value_field=["sd", "se", "cv"], only_group=True),
        "paraxanthine_tmax_individual": Parameter(measurement_types=["tmax"], substance="paraxanthine", value_field=["value"], only_individual=True),
        "paraxanthine_tmax_group": Parameter(measurement_types=["tmax"], substance="paraxanthine",value_field=["mean", "median"], only_group=True),
        "paraxanthine_tmax_error": Parameter(measurement_types=["tmax"], substance="paraxanthine",value_field=["sd", "se", "cv"], only_group=True),
        "paraxanthine_kel_individual": Parameter(measurement_types=["kel"], substance="paraxanthine", value_field=["value"], only_individual=True),
        "paraxanthine_kel_group": Parameter(measurement_types=["kel"], substance="paraxanthine", value_field=["mean", "median"],only_group=True),
        "paraxanthine_kel_error": Parameter(measurement_types=["kel"], substance="paraxanthine", value_field=["sd", "se", "cv"],only_group=True),

        # theophylline
        "theophylline_plasma/blood": Parameter(substance="theophylline", value_field=["tissue"],
                                               values=["plasma", "blood", "serum"], groupby=False),
        "theophylline_urine": Parameter(substance="theophylline", value_field=["tissue"], values=["urine"],
                                        groupby=False),
        "theophylline_saliva": Parameter(substance="theophylline", value_field=["tissue"], values=["saliva"],
                                         groupby=False),
        "theophylline_vd_individual": Parameter(measurement_types=["vd"], substance="theophylline",
                                                value_field=["value"], only_individual=True),
        "theophylline_vd_group": Parameter(measurement_types=["vd"], substance="theophylline",
                                           value_field=["mean", "median"], only_group=True),
        "theophylline_vd_error": Parameter(measurement_types=["vd"], substance="theophylline",
                                           value_field=["sd", "se", "cv"], only_group=True),
        "theophylline_clearance_individual": Parameter(measurement_types=["clearance"], substance="theophylline",
                                                       value_field=["value"], only_individual=True),
        "theophylline_clearance_group": Parameter(measurement_types=["clearance"], substance="theophylline",
                                                  value_field=["mean", "median"], only_group=True),
        "theophylline_clearance_error": Parameter(measurement_types=["clearance"], substance="theophylline",
                                                  value_field=["sd", "se", "cv"], only_group=True),
        "theophylline_auc_individual": Parameter(measurement_types=["auc_end", "auc_inf"], substance="theophylline",
                                                 value_field=["value"], only_individual=True),
        "theophylline_auc_group": Parameter(measurement_types=["auc_end", "auc_inf"], substance="theophylline",
                                            value_field=["mean", "median"], only_group=True),
        "theophylline_auc_error": Parameter(measurement_types=["auc_end", "auc_inf"], substance="theophylline",
                                            value_field=["sd", "se", "cv"], only_group=True),
        "theophylline_thalf_individual": Parameter(measurement_types=["thalf"], substance="theophylline",
                                                   value_field=["value"], only_individual=True),
        "theophylline_thalf_group": Parameter(measurement_types=["thalf"], substance="theophylline",
                                              value_field=["mean", "median"], only_group=True),
        "theophylline_thalf_error": Parameter(measurement_types=["thalf"], substance="theophylline",
                                              value_field=["sd", "se", "cv"], only_group=True),
        "theophylline_cmax_individual": Parameter(measurement_types=["cmax"], substance="theophylline",
                                                  value_field=["value"], only_individual=True),
        "theophylline_cmax_group": Parameter(measurement_types=["cmax"], substance="theophylline",
                                             value_field=["mean", "median"], only_group=True),
        "theophylline_cmax_error": Parameter(measurement_types=["cmax"], substance="theophylline",
                                             value_field=["sd", "se", "cv"], only_group=True),
        "theophylline_tmax_individual": Parameter(measurement_types=["tmax"], substance="theophylline",
                                                  value_field=["value"], only_individual=True),
        "theophylline_tmax_group": Parameter(measurement_types=["tmax"], substance="theophylline",
                                             value_field=["mean", "median"], only_group=True),
        "theophylline_tmax_error": Parameter(measurement_types=["tmax"], substance="theophylline",
                                             value_field=["sd", "se", "cv"], only_group=True),
        "theophylline_kel_individual": Parameter(measurement_types=["kel"], substance="theophylline",
                                                 value_field=["value"], only_individual=True),
        "theophylline_kel_group": Parameter(measurement_types=["kel"], substance="theophylline",
                                            value_field=["mean", "median"], only_group=True),
        "theophylline_kel_error": Parameter(measurement_types=["kel"], substance="theophylline",
                                            value_field=["sd", "se", "cv"], only_group=True),

        # theobromine
        "theobromine_plasma/blood": Parameter(substance="theobromine", value_field=["tissue"],
                                              values=["plasma", "blood", "serum"], groupby=False),
        "theobromine_urine": Parameter(substance="theobromine", value_field=["tissue"], values=["urine"],
                                       groupby=False),
        "theobromine_saliva": Parameter(substance="theobromine", value_field=["tissue"], values=["saliva"],
                                        groupby=False),
        "theobromine_vd_individual": Parameter(measurement_types=["vd"], substance="theobromine",
                                               value_field=["value"], only_individual=True),
        "theobromine_vd_group": Parameter(measurement_types=["vd"], substance="theobromine",
                                          value_field=["mean", "median"], only_group=True),
        "theobromine_vd_error": Parameter(measurement_types=["vd"], substance="theobromine",
                                          value_field=["sd", "se", "cv"], only_group=True),
        "theobromine_clearance_individual": Parameter(measurement_types=["clearance"], substance="theobromine",
                                                      value_field=["value"], only_individual=True),
        "theobromine_clearance_group": Parameter(measurement_types=["clearance"], substance="theobromine",
                                                 value_field=["mean", "median"], only_group=True),
        "theobromine_clearance_error": Parameter(measurement_types=["clearance"], substance="theobromine",
                                                 value_field=["sd", "se", "cv"], only_group=True),
        "theobromine_auc_individual": Parameter(measurement_types=["auc_end", "auc_inf"], substance="theobromine",
                                                value_field=["value"], only_individual=True),
        "theobromine_auc_group": Parameter(measurement_types=["auc_end", "auc_inf"], substance="theobromine",
                                           value_field=["mean", "median"], only_group=True),
        "theobromine_auc_error": Parameter(measurement_types=["auc_end", "auc_inf"], substance="theobromine",
                                           value_field=["sd", "se", "cv"], only_group=True),
        "theobromine_thalf_individual": Parameter(measurement_types=["thalf"], substance="theobromine",
                                                  value_field=["value"], only_individual=True),
        "theobromine_thalf_group": Parameter(measurement_types=["thalf"], substance="theobromine",
                                             value_field=["mean", "median"], only_group=True),
        "theobromine_thalf_error": Parameter(measurement_types=["thalf"], substance="theobromine",
                                             value_field=["sd", "se", "cv"], only_group=True),
        "theobromine_cmax_individual": Parameter(measurement_types=["cmax"], substance="theobromine",
                                                 value_field=["value"], only_individual=True),
        "theobromine_cmax_group": Parameter(measurement_types=["cmax"], substance="theobromine",
                                            value_field=["mean", "median"], only_group=True),
        "theobromine_cmax_error": Parameter(measurement_types=["cmax"], substance="theobromine",
                                            value_field=["sd", "se", "cv"], only_group=True),
        "theobromine_tmax_individual": Parameter(measurement_types=["tmax"], substance="theobromine",
                                                 value_field=["value"], only_individual=True),
        "theobromine_tmax_group": Parameter(measurement_types=["tmax"], substance="theobromine",
                                            value_field=["mean", "median"], only_group=True),
        "theobromine_tmax_error": Parameter(measurement_types=["tmax"], substance="theobromine",
                                            value_field=["sd", "se", "cv"], only_group=True),
        "theobromine_kel_individual": Parameter(measurement_types=["kel"], substance="theobromine",
                                                value_field=["value"], only_individual=True),
        "theobromine_kel_group": Parameter(measurement_types=["kel"], substance="theobromine",
                                           value_field=["mean", "median"], only_group=True),
        "theobromine_kel_error": Parameter(measurement_types=["kel"], substance="theobromine",
                                           value_field=["sd", "se", "cv"], only_group=True),

    }
    """
    studies = studies.df.apply(_add_information, args=(pkdata, pks_info, "outputs"), axis=1)
    study_keys.extend(pks_info.keys())
    studies = studies.fillna(" ")
    return studies, study_keys


def format(studies, study_keys):
    studies = studies.rename(columns={"reference_date": "publication date"})
    studies["PKDB identifier"] = studies["sid"].apply(lambda x: f'=HYPERLINK("https://develop.pk-db.com/{x}/";"{x}")')
    studies["PMID"] = studies["sid"].apply(lambda x: f'=HYPERLINK("https://www.ncbi.nlm.nih.gov/pubmed/{x}";"{x}")')
    study_keys = ["PKDB identifier", "name", "PMID", "publication date", ] + study_keys
    studies.sort_values(by="publication date", inplace=True)
    return studies, study_keys
def clear_sheat(spread, header_size, column_length):
    spread.update_cells(
        start=(1, header_size),
        end=(1, 1),
        vals=["" for i in range(0, column_length * 1)],
    )

def reporting_summary(pkdata: PKData, path: Path, google_sheets:str, report_type="Studies", substances=[]):
    """ creates a summary table from a pkdata objects  and saves it to path.
    :param google_sheets:
        The admin needs to create a excel sheet in his google drive. The name of the excel sheet has to be entered as
        the google_sheets argument.
        IMPORTANT:
            For google sheets to work, ask admin for the google_secret.json and copy it in the config folder.
            cp  ~/.config/gspread_pandas/google_secret.json
        FOR ADMIN:

            1. Go to the Google APIs Console -> https://console.developers.google.com/
            2. Create a new project.
            3. Click Enable API and Services. Search for and enable the Google Drive API.
               Click Enable API and Services. Search for and enable the Google Sheets API.
            4. Create credentials for a Web Server to access Application Data.
            5. Name the service account and grant it a Project Role of Editor.
            6. Download the JSON file.
            7. Copy the JSON file to your code directory and rename it to google_secret.json


google_sheets
    :param pkdata:
    :return:
    """
    studies = pkdata.studies
    study_keys = []

    if report_type == "Studies":
        studies, study_keys = basics_table(studies, substances, pkdata, study_keys)
        header_start = 'A4'
        header_size = 4

    elif report_type == "Timecourses":
        studies, study_keys = timecourses_table(studies, substances, pkdata, study_keys)
        header_start = 'A4'
        header_size = 4

    elif report_type == "Pharmacokinetics":
        studies, study_keys = pks_table(studies, substances, pkdata, study_keys)
        header_start = 'A5'
        header_size = 5

    else:
        raise ValueError("reporting_type has to be one of the following: ['Studies', 'Timecourses', 'Pharmacokinetics']")

    studies, study_keys = format(studies, study_keys)

    if google_sheets is not None:
        spread = Spread(google_sheets)
        sheet = spread.find_sheet(report_type)
        sheet.resize(header_size, len(study_keys))
        spread.df_to_sheet(studies[study_keys], index=False, headers=False, sheet=report_type, start=header_start, replace=False)

    if str(path).endswith(".xlsx"):
        studies[study_keys].to_excel(path)

    elif str(path).endswith(".tsv"):
        studies[study_keys].to_csv(path, sep='\t')

    else:
        raise AssertionError("wrong path ending (tsv and xlsx are supported")





