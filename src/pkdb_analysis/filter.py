""" Defines frequently used filters for the PKData instances."""
from typing import Callable, Dict, Iterable

import numpy as np
import pandas as pd


def filter_factory(filter_dict: Dict):
    """generic filter factory"""
    f_idx = []
    for key, value in filter_dict.items():

        def constructor(key, value):
            def _f1(d):
                return d[key].isin(value)

            def _f2(d):
                return d[key] == value

            if isinstance(value, list):
                return _f1
            else:
                return _f2

        f_idx.append(constructor(key, value))
    return f_idx


def filter_single_intervention(pkdata: "PKData") -> "PKData":
    """PKData filter returning a concise PKData instance containing only outputs where one intervention was applied."""
    pkdata = pkdata.copy()
    single_interventions = []
    for pk, co_interventions in pkdata.interventions.groupby(pkdata.interventions.pk):
        if len(co_interventions) == 1:
            single_interventions.append(pk)
    return pkdata.filter_intervention(
        lambda d: d[pkdata.interventions.pk].isin(single_interventions)
    )


def filter_healthy(pkdata: "PKData") -> "PKData":
    """PKData filter returning a concise PKData instance containing only healthy subjects."""
    pkdata = pkdata.copy()
    return pkdata.filter_subject(f_healthy, concise=False).exclude_subject(f_n_healthy)


def exclude_tests(data: "PKData") -> "PKData":
    """Exclude data for test studies."""
    return data.exclude_intervention(
        lambda d: d["study_name"].isin(["Test1", "Test2", "Test3", "Test4"])
    )


def combine(args: Iterable):
    """Helper function join values. This function designed to be used in df.pivot_table as aggfunc."""
    args = sorted(set([str(arg) for arg in args]))
    str_value = " || ".join(args)
    if str_value == "nan":
        return np.NAN
    try:
        return pd.to_numeric(str_value)
    except ValueError:
        return str_value


def pk_info(
    d: pd.DataFrame,
    measurement_type: str,
    columns: Iterable[str],
    suffix: str = None,
    concise: bool = True,
    aggfunc: Callable = combine,
):
    """Pivots a pd.Dataframe to get a single rows for a measurement_type on a selected column.
    If multiple values exists such configuration (e.g. df=pkdata.groups, measurement_type=sex, column=choice,
    can contain males and females). The argument: aggfunc is applied to combine theses values.
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


def f_unit(d: pd.DataFrame, unit: str) -> pd.Series:
    """Filter for units."""
    return d["unit"] == unit


def f_measurement_type(d: pd.DataFrame, measurement_type: str) -> pd.Series:
    """Filter for measurement types."""
    return d["measurement_type"] == measurement_type


def f_substance(d: pd.DataFrame, substance: str) -> pd.Series:
    """Filter for one substance."""
    return d["substance"] == substance


def f_substance_in(d: pd.DataFrame, substances: Iterable[str]) -> pd.Series:
    """Filter for substances."""
    return d["substance"].isin(substances)


def f_dosing(d: pd.DataFrame, substance: str) -> pd.Series:
    """Filter for one substance which are applied as dosing.
    This filter is typically used in PKData.filter_interventions."""
    return f_substance(d, substance) & f_measurement_type(d, "dosing")


def f_dosing_in(d: pd.DataFrame, substances: Iterable[str]) -> pd.Series:
    """Filter for substances which are applied as dosing.
    This filter is typically used in PKData.filter_interventions."""
    return d["substance"].isin(substances) & f_measurement_type(d, "dosing")


def f_mt_substance(d: pd.DataFrame, measurement_type: str, substance: str) -> pd.Series:
    """Combined filter on one measurement_type  and one substance."""

    return f_measurement_type(d, measurement_type) & f_substance(d, substance)


def f_mt_in_substance_in(
    d: pd.DataFrame, measurement_types: Iterable[str], substances: Iterable[str]
) -> pd.Series:
    """Combined filter on  measurement_types and substances."""
    return d["measurement_type"].isin(measurement_types) & d["substance"].isin(
        substances
    )


def f_choice(d: pd.DataFrame, choice: str) -> pd.Series:
    """Generic filter on the choice field."""
    return d["choice"] == choice


def f_exclude_choice(d: pd.DataFrame, choice: str) -> pd.Series:
    """Generic filter on the choice field."""
    return d["choice"] != choice


def f_smoking(d: pd.DataFrame) -> pd.Series:
    """Filter for smoking subjects."""
    return f_measurement_type(d, "smoking") & f_choice(d, "Y")


def f_n_smoking(d: pd.DataFrame) -> pd.Series:
    """Filter for non smoking subjects."""
    return f_measurement_type(d, "smoking") & f_choice(d, "N")


def f_oc(d: pd.DataFrame) -> pd.Series:
    """Filter for subject taking oral contraceptives"""
    return f_measurement_type(d, "oral contraceptives") & f_choice(d, "Y")


def f_n_oc(d: pd.DataFrame) -> pd.Series:
    """Filter for subject not taking oral contraceptives."""
    return f_measurement_type(d, "oral contraceptives") & f_choice(d, "N")


def f_pregnant(d: pd.DataFrame) -> pd.Series:
    """Filter for subject pregnant"""
    return f_measurement_type(d, "pregnant") & f_choice(d, "Y")


def f_n_pregnant(d: pd.DataFrame) -> pd.Series:
    """Filter for subject not pregnant."""
    return f_measurement_type(d, "pregnant") & f_choice(d, "N")


def f_male(d: pd.DataFrame) -> pd.Series:
    """Filter for male subjects."""
    return f_measurement_type(d, "sex") & f_choice(d, "M")


def f_female(d: pd.DataFrame) -> pd.Series:
    """Filter for female subjects."""
    return f_measurement_type(d, "sex") & f_choice(d, "F")


def f_effective_n_oc(d: pd.DataFrame) -> pd.Series:
    """Filter for not taking oral contraceptives, assuming that men do not take
    oral contraceptives."""
    return (f_n_oc(d)) | (f_male(d))


def f_healthy(d: pd.DataFrame) -> pd.Series:
    """Filter for healthy subjects. CAUTION: This are not exclusively healthy subjects,."""
    return f_measurement_type(d, "healthy") & f_choice(d, "Y")


def f_n_healthy(d: pd.DataFrame) -> pd.Series:
    """Filter for non healthy subjects.. CAUTION: This are not exclusively non healthy subjects,."""
    return f_measurement_type(d, "healthy") & f_choice(d, "N")
