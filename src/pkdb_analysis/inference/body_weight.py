"""
Helper functions for body weight inferences.
Takes PKData instance and  calculates  additional outputs based on body weights of subjects.
"""
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from pint import Quantity, UnitRegistry

from pkdb_analysis.units import ureg


Q_ = ureg.Quantity


class InferWeight(object):
    """
    A helper class for inference of results from body weights of subjects.
    """

    def __init__(self, series: pd.Series, ureg: UnitRegistry):
        self.series = series
        self.ureg = ureg
        self.weight, self.weight_field = self.get_weight()

    def per_bw(self, unit_field):
        return self.series[unit_field].endswith("/ kilogram")

    @staticmethod
    def per_bw_exp(per_bw) -> float:
        if per_bw:
            return 1
        else:
            return -1

    def get_weight(
        self,
        weight_fields=("value_weight", "mean_weight", "median_weight"),
        weight_unit_field="unit_weight",
    ) -> Tuple[Optional[Quantity], Optional[str]]:
        """helper function to get the weight of a subject or group"""
        for weight_field in weight_fields:
            if weight_field in self.series:
                this_value = self.series[weight_field]
                this_unit = self.series[weight_unit_field]
                if this_value is not None:
                    if not np.isnan(this_value):
                        return Q_(this_value, this_unit), weight_field

        return None, None

    def bw_infer(
        self,
        unit_field="unit",
        infer_fields=("value", "mean", "median", "min", "max", "sd", "se"),
        per_bw_field="per_bw",
    ) -> pd.Series:
        """helper function to infer values from the weight of a subject or group"""
        if self.weight is not None and self.series[unit_field] is not None:
            per_bw = self.per_bw(unit_field)
            per_bw_exp = self.per_bw_exp(per_bw)
            series = self.series.copy()
            unit = self.ureg(series[unit_field])
            factor = unit * self.weight ** per_bw_exp
            for infer_field in infer_fields:
                if isinstance(series[infer_field], (float, np.ndarray)):
                    series[infer_field] = factor.m * series[infer_field]

            series[unit_field] = str(factor.u)
            series["inferred"] = True
            series[per_bw_field] = not per_bw

            return series

        return pd.Series(None, index=self.series.index)


def infer_output(series: pd.Series):
    return InferWeight(series, ureg).bw_infer()


def infer_intervention(series: pd.Series):
    return InferWeight(series, ureg).bw_infer(
        unit_field="intervention_unit",
        infer_fields=("intervention_value",),
        per_bw_field="intervention_per_bw",
    )


def infer_weight(df: pd.DataFrame, by_intervention=True, by_output=True):
    result_infer = df.dropna(subset=["unit_weight"])
    result_no_bodyweight = df[df["unit_weight"].isnull()]
    if by_output:
        result_infer_outputs = result_infer.apply(infer_output, axis="columns").dropna(
            how="all"
        )
        result_infer = result_infer.append(result_infer_outputs, ignore_index=True)
    if by_intervention:
        result_infer_outputs = result_infer.apply(
            infer_intervention, axis="columns"
        ).dropna(how="all")
        result_infer = result_infer.append(result_infer_outputs, ignore_index=True)
    result_infer = result_infer.append(result_no_bodyweight, ignore_index=True)
    return result_infer
