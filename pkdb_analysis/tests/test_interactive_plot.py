from pathlib import Path

import pandas as pd
import numpy as np
from pkdb_analysis.data import PKData
from pkdb_analysis.inference.body_weight import infer_output, ureg, infer_intervention, infer_weight
from pkdb_analysis.meta_analysis import MetaAnalysis
from pkdb_analysis.tests.data.test_data import INDIVIDUAL_OUTPUT, GROUP_OUTPUT, INDIVIDUAL_NO_BODYWEIGHT_OUTPUT


def test_interactive_plot1():
    series = pd.Series(INDIVIDUAL_OUTPUT)
    raise NotImplementedError
