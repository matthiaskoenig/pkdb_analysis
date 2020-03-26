""" Defines frequently used filters for the PKData instances."""
from pkdb_analysis.data import PKData
from typing import List

TEST_STUDY_NAMES = ["Test1", "Test2", "Test3", "Test4"]
import collections
import pandas as pd
import numpy as np
import warnings

PlottingParameter = collections.namedtuple('PlottingParameter',
                                           ['measurement_type',
                                            'units_rm'])


# add group_columns,
# add individual_columns,
# add intervention_columns,
# add output_columns,
# add timecourse_columns


def exclude_tests(data: PKData):
    return data.exclude_intervention(lambda d: d["study_name"].isin(TEST_STUDY_NAMES))

def combine(args):
    args = sorted(set([str(arg) for arg in args]))
    str_value = " || ".join(args)
    if str_value == "nan":
        return np.NAN
    try:
        return pd.to_numeric(str_value)

    except:
        return str_value



def pk_info(d, measurement_type, columns, suffix=None, concise=True, aggfunc=combine):
    if suffix is None:
        suffix_text = f"_{measurement_type}"
    else:
        suffix_text = suffix

    columns = [d.pk, *columns]
    df = d[d["measurement_type"] == measurement_type][columns].set_index(d.pk).add_suffix(suffix_text).reset_index()
    if len(df) == 0:
        return df
    if concise:
        return df.pivot_table(index=d.pk, aggfunc=aggfunc,dropna=False).reset_index()
    return df







def f_unit(d, unit: str):
    """

    :param d: PKDataFrame or pandas.DataFrame
    :param unit:
    :return:
    """
    return d["unit"] == unit


def f_mt(d, measurement_type: str):
    """

    :param d: PKDataFrame or pandas.DataFrame
    :param measurement_type:
    :return:
    """
    return (d["measurement_type"] == measurement_type)


def f_substance(d, substance: str):
    """

    :param d: PKDataFrame or pandas.DataFrame
    :param substance:
    :return:
    """
    return d["substance"] == substance

def f_dosing(d, substance:str):
    """filtering index for PKData for dosing with substance

    :param d: PKDataFrame or pandas.DataFrame
    :param substance:
    :return:
    """
    return f_substance(d, substance) & f_mt(d, "dosing")

def f_dosing_in(d, substances:List[str]):
    """filtering index for PKData for dosing with substance

    :param d: PKDataFrame or pandas.DataFrame
    :param substance:
    :return:
    """
    d["substance"].isin(substances)
    return d["substance"].isin(substances) & f_mt(d, "dosing")

def f_mt_substance(d, measurement_type:str , substance:str):
    """filtering index for PKData for measurement_type with substance

    :param d: PKDataFrame or pandas.DataFrame
    :param measurement_type:
    :param substance:
    :return:
    """
    return f_mt(d,measurement_type) & f_substance(d, substance)

def f_mt_in_substance_in(d, measurement_types:str , substances:str):
    """filtering index for PKData for measurement_type with substance

    :param d: PKDataFrame or pandas.DataFrame
    :param measurement_type:
    :param substance:
    :return:
    """
    return d["measurement_type"].isin(measurement_types) & d["substance"].isin(substances)


def f_choice(d, choice):
    return d["choice"] == choice


def f_smoking(d):
    return f_mt(d, "smoking") & f_choice(d, "Y")


def f_n_smoking(d):
    return f_mt(d, "smoking") & f_choice(d, "N")


def f_oc(d):
    return f_mt(d, "oral contraceptives") & f_choice(d, "Y")


def f_n_oc(d):
    return f_mt(d, "oral contraceptives") & f_choice(d, "N")


def f_male(d):
    return f_mt(d, "sex") & f_choice(d, "M")


def f_female(d):
    return f_mt(d, "sex") & f_choice(d, "F")


def f_effective_n_oc(d):
    return (f_n_oc(d)) | (f_male(d))


def f_healthy(d):
    return f_mt(d, "healthy") & f_choice(d, "Y")


def f_n_healthy(d):
    return f_mt(d, "healthy") & f_choice(d, "N")

