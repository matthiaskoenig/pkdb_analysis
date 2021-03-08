import pandas as pd
import pytest

from pkdb_analysis.reports.effect_analysis import (
    OutputPair,
    fixed_effect,
    random_effects,
)


def test_esc_mean_sd():
    """From https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/a.html
    ##     Effect Size:  -0.7082
    ##  Standard Error:   0.1916
    ##        Variance:   0.0367
    ##        Lower CI:  -1.0837
    ##        Upper CI:  -0.3326
    ##          Weight:   27.2374
    """

    grp1m = 12.3
    grp1sd = 3.1
    grp1n = 56

    grp2m = 10.3
    grp2sd = 2.5
    grp2n = 60
    result = OutputPair.esc_mean_sd(grp1n, grp2n, grp1m, grp2m, grp1sd, grp2sd)

    assert result["hedges_g"] == pytest.approx(-0.7082, rel=0.01)
    assert result["se"] == pytest.approx(0.1916, rel=0.01)
    assert result["variance"] == pytest.approx(0.0367, rel=0.01)
    assert result["weight"] == pytest.approx(27.2374, rel=0.01)


def test_fixed_effect():
    """
    from https://www.meta-analysis.com/downloads/M-a_f_e_v_r_e_sv.pdf

    """
    data = {
        "study": ["Caroll", "Grant", "Peck", "Donat", "Stewart", "Young"],
        "hedges_g": [0.1, 0.3, 0.35, 0.65, 0.45, 0.15],
        "standard_error": [0.173, 0.173, 0.224, 0.1, 0.224, 0.141],
        "variance": [0.03, 0.03, 0.05, 0.01, 0.05, 0.02],
    }
    df = pd.DataFrame(data)

    result = fixed_effect(df, effect_size="hedges_g", variance="variance")

    assert result["fixed_effect_weighted_mean"] == pytest.approx(0.3968, rel=0.01)
    assert result["fixed_effect_variance"] == pytest.approx(0.0039, rel=0.01)
    assert result["fixed_effect_se"] == pytest.approx(0.0624, rel=0.01)


def test_random_effects():
    """
    from https://www.meta-analysis.com/downloads/M-a_f_e_v_r_e_sv.pdf

    """
    data = {
        "study": ["Caroll", "Grant", "Peck", "Donat", "Stewart", "Young"],
        "hedges_g": [0.1, 0.3, 0.35, 0.65, 0.45, 0.15],
        "standard_error": [0.173, 0.173, 0.224, 0.1, 0.224, 0.141],
        "variance": [0.03, 0.03, 0.05, 0.01, 0.05, 0.02],
    }
    df = pd.DataFrame(data)

    result = random_effects(df, effect_size="hedges_g", variance="variance")

    assert result["random_effects_weighted_mean"] == pytest.approx(0.3442, rel=0.01)
    assert result["random_effects_variance"] == pytest.approx(0.0114, rel=0.01)
    assert result["random_effects_sd"] == pytest.approx(0.1068, rel=0.01)
