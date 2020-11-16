""" Defines frequently used filters for the PKData instances."""
from typing import Iterable, List
import numpy as np
import pandas as pd


def filter_single_intervention(pkdata: 'PKData') -> 'PKData':
    """Returns modified copy"""
    pkdata = pkdata.copy()
    single_interventions = []
    for pk, co_interventions in pkdata.interventions.groupby(
            pkdata.interventions.pk):
        if len(co_interventions) == 1:
            single_interventions.append(pk)

    return pkdata.filter_intervention(
        lambda d: d[pkdata.interventions.pk].isin(single_interventions)
    )


def filter_healthy(pkdata: 'PKData') -> 'PKData':
    """Returns modified copy"""
    pkdata = pkdata.copy()
    return pkdata.filter_subject(
        f_healthy, concise=False
    ).exclude_subject(f_n_healthy)


def exclude_tests(data: 'PKData'):
    """Exclude data for test studies."""
    return data.exclude_intervention(lambda d: d["study_name"].isin(
        ["Test1", "Test2", "Test3", "Test4"]
    ))


def combine(args):
    args = sorted(set([str(arg) for arg in args]))
    str_value = " || ".join(args)
    if str_value == "nan":
        return np.NAN
    try:
        return pd.to_numeric(str_value)
    # FIXME TOO BROAD EXCEPTION, use the correct error (TypeError?)
    except:
        return str_value


def pk_info(d, measurement_type, columns, suffix=None, concise=True, aggfunc=combine):
    """FIXME: Document me? What is this

    """
    if suffix is None:
        suffix_text = f"_{measurement_type}"
    else:
        suffix_text = suffix

    columns = [d.pk, *columns]
    df = (
        d[d["measurement_type"] == measurement_type][columns]
            .set_index(d.pk)
            .add_suffix(suffix_text)
            .reset_index()
    )
    if len(df) == 0:
        return df
    if concise:
        return df.pivot_table(index=d.pk, aggfunc=aggfunc, dropna=False).reset_index()
    return df


def f_unit(d, unit: str):
    """ FIXME: DOCUMENT ME

    :param d: PKDataFrame or pandas.DataFrame
    :param unit:
    :return:
    """
    return d["unit"] == unit


def f_measurement_type(d, measurement_type: str) -> bool:
    """ FIXME: DOCUMENT ME

    :param d: PKDataFrame or pandas.DataFrame
    :param measurement_type:
    :return:
    """
    return d["measurement_type"] == measurement_type


def f_substance(d, substance: str) -> bool:
    """ FIXME: DOCUMENT ME """
    return d["substance"] == substance


def f_substance_in(d, substances: Iterable[str]):
    """ FIXME: DOCUMENT ME """
    return d["substance"].isin(substances)


def f_dosing(d, substance: str) -> bool:
    """ FIXME: DOCUMENT ME """
    return f_substance(d, substance) & f_measurement_type(d, "dosing")


def f_dosing_in(d, substances: List[str]) -> bool:
    """ FIXME: DOCUMENT ME """
    return d["substance"].isin(substances) & f_measurement_type(d, "dosing")


def f_mt_substance(d, measurement_type: str, substance: str):
    """ FIXME: DOCUMENT ME """
    """filtering index for PKData for measurement_type with substance

    :param d: PKDataFrame or pandas.DataFrame
    :param measurement_type:
    :param substance:
    :return:
    """
    return f_measurement_type(d, measurement_type) & f_substance(d, substance)


def f_mt_in_substance_in(d, measurement_types: str, substances: str):
    """ FIXME: DOCUMENT ME """
    """filtering index for PKData for measurement_type with substance

    :param d: PKDataFrame or pandas.DataFrame
    :param measurement_type:
    :param substance:
    :return:
    """
    return d["measurement_type"].isin(measurement_types) & d["substance"].isin(
        substances
    )


def f_choice(d, choice):
    """ FIXME: DOCUMENT ME """
    return d["choice"] == choice


def f_smoking(d):
    """ FIXME: DOCUMENT ME """
    return f_measurement_type(d, "smoking") & f_choice(d, "Y")


def f_n_smoking(d):
    """ FIXME: DOCUMENT ME """
    return f_measurement_type(d, "smoking") & f_choice(d, "N")


def f_oc(d):
    """ FIXME: DOCUMENT ME """
    return f_measurement_type(d, "oral contraceptives") & f_choice(d, "Y")


def f_n_oc(d):
    """ FIXME: DOCUMENT ME """
    return f_measurement_type(d, "oral contraceptives") & f_choice(d, "N")


def f_male(d):
    """ FIXME: DOCUMENT ME """
    return f_measurement_type(d, "sex") & f_choice(d, "M")


def f_female(d):
    """ FIXME: DOCUMENT ME """
    return f_measurement_type(d, "sex") & f_choice(d, "F")


def f_effective_n_oc(d):
    """ FIXME: DOCUMENT ME """
    return (f_n_oc(d)) | (f_male(d))


def f_healthy(d):
    """ FIXME: DOCUMENT ME """
    return f_measurement_type(d, "healthy") & f_choice(d, "Y")


def f_n_healthy(d):
    """ FIXME: DOCUMENT ME """
    return f_measurement_type(d, "healthy") & f_choice(d, "N")
