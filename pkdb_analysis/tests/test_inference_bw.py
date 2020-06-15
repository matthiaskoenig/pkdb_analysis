from pathlib import Path

import pandas as pd
import numpy as np
from pkdb_analysis.data import PKData
from pkdb_analysis.inference.body_weight import infer_output, ureg, infer_intervention, infer_weight
from pkdb_analysis.meta_analysis import MetaAnalysis
from pkdb_analysis.tests.data.group_data import INDIVIDUAL_OUTPUT, GROUP_OUTPUT, INDIVIDUAL_NO_BODYWEIGHT_OUTPUT

from pkdb_analysis.tests import TEST_HDF5


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
    test_data = PKData.from_hdf5(TEST_HDF5)
    ma = MetaAnalysis(test_data, ["caffeine"], "test/url/")
    ma.create_results()
    results_inferred = infer_weight(ma.results)
    assert len(results_inferred) > len(ma.results)
