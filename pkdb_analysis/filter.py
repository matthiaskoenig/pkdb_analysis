""" Defines frequently used filters for the PKData instances."""
from pkdb_analysis.data import PKData

TEST_STUDY_NAMES = ["Test1", "Test2", "Test3", "Test4"]
import collections

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


def pk_info(d, measurement_type, columns, suffix=None):
    if suffix is None:
        suffix_text = f"_{measurement_type}"
    else:
        suffix_text = suffix

    columns = [d.pk, *columns]
    return d[d["measurement_type"] == measurement_type][columns].set_index(d.pk).add_suffix(suffix_text).reset_index()

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
    return f_substance(d, substance) & (d["measurement_type"] == "dosing")


def f_mt_substance(d, measurement_type:str , substance:str):
    """filtering index for PKData for measurement_type with substance

    :param d: PKDataFrame or pandas.DataFrame
    :param measurement_type:
    :param substance:
    :return:
    """
    return f_mt(d,measurement_type) & f_substance(d, substance)


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

