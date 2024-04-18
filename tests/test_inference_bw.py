from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from pkdb_analysis.data import PKData
from pkdb_analysis.inference.body_weight import (
    infer_intervention,
    infer_output,
    infer_weight,
    ureg,
)
from pkdb_analysis.meta_analysis import MetaAnalysis
from pkdb_analysis.test import TESTDATA_CONCISE_TRUE_ZIP


INDIVIDUAL_OUTPUT = {
    "value": 2.0,
    "mean": None,
    "median": None,
    "min": None,
    "max": None,
    "sd": None,
    "se": None,
    "cv": None,
    "unit": "ng",
    "value_weight": 80.0,
    "unit_weight": "kg",
    "intervention_value": 0.8,
    "intervention_unit": "ng",
}

INDIVIDUAL_NO_BODYWEIGHT_OUTPUT = {
    "value": 2.0,
    "mean": None,
    "median": None,
    "min": None,
    "max": None,
    "sd": None,
    "se": None,
    "cv": None,
    "unit": "ng",
    "value_weight": None,
    "unit_weight": None,
    "intervention_value": 0.8,
    "intervention_unit": "ng",
}

GROUP_OUTPUT = {
    "value": None,
    "mean": 4.5,
    "median": None,
    "min": None,
    "max": None,
    "sd": 4.6,
    "se": None,
    "cv": 0.4,
    "unit": "ng",
    "mean_weight": 80.0,
    "unit_weight": "kg",
    "intervention_value": 0.8,
    "intervention_unit": "ng",
}


def test_output_inference_by_body_weight1():
    series = pd.Series(INDIVIDUAL_OUTPUT)
    output = infer_output(series)
    assert output["per_bw"] is True
    assert output["inferred"] is True
    assert output.value == 2 / 80
    assert output["mean"] is None
    assert ureg(output.unit) == ureg("ng/kg")
    assert output.intervention_value == 0.8
    assert ureg(output.intervention_unit) == ureg("ng")


def test_output_inference_by_body_weight2():
    series = pd.Series(GROUP_OUTPUT)
    output = infer_output(series)
    assert output["inferred"] is True
    assert output["per_bw"] is True
    assert output["mean"] == 4.5 / 80
    assert output.cv == 0.4
    assert ureg(output.unit) == ureg("ng/kg")
    assert np.isclose(output.intervention_value, 0.8)
    assert ureg(output.intervention_unit) == ureg("ng")


def test_output_inference_by_body_weight3():
    series = pd.Series(INDIVIDUAL_NO_BODYWEIGHT_OUTPUT)
    output = infer_output(series)
    assert output.isna().all()


def test_intervention_inference_by_body_weight1():
    series = pd.Series(INDIVIDUAL_OUTPUT)
    output = infer_intervention(series)
    assert output["inferred"] is True
    assert output["intervention_per_bw"] is True
    assert output.value == 2
    assert output["mean"] is None
    assert ureg(output.unit) == ureg("ng")
    assert np.isclose(output.intervention_value, 0.8 / 80)
    assert ureg(output.intervention_unit) == ureg("ng/kg")


def test_inference_by_body_weight1():
    df = pd.DataFrame([INDIVIDUAL_OUTPUT])
    outputs = infer_weight(df)
    assert len(outputs) == 4
    for group, output_subset in outputs.groupby(["intervention_per_bw", "per_bw"]):
        assert len(output_subset) == 1


def test_inference_by_body_weight2():
    df = pd.DataFrame([INDIVIDUAL_OUTPUT, GROUP_OUTPUT])
    outputs = infer_weight(df)
    assert len(outputs) == 8
    for group, output_subset in outputs.groupby(["intervention_per_bw", "per_bw"]):
        assert len(output_subset) == 2


def test_inference_by_body_weight3():
    test_data = PKData.from_archive(TESTDATA_CONCISE_TRUE_ZIP)
    ma = MetaAnalysis(test_data, {"caf"}, "test/url/")
    ma.create_results()
    results_inferred = infer_weight(ma.results)
    assert len(results_inferred) > len(ma.results)
