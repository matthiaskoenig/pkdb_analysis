"""Regression coverage for unit correctness and bounded statistical memory."""

import numpy as np
import pytest

from pkpdutils.stats import (
    ParameterSample,
    compare,
    effect_size,
    effects_from_arrays,
    fixed_effect,
    heterogeneity,
    hodges_lehmann,
    moments_from_lognormal,
    multiple_comparison,
    random_effects,
    ratio,
    summarize,
    tost,
)
from pkpdutils.stats import tests as statistical_tests


@pytest.mark.parametrize("summary", [False, True])
def test_equivalent_units_match_preconverted_statistics(summary):
    if summary:
        a = ParameterSample(mean=2, sd=1, n=10, unit="mg/L")
        b = ParameterSample(mean=2000, sd=1000, n=10, unit="ug/L")
    else:
        a = ParameterSample(values=np.array([1, 2, 3]), unit="mg/L")
        b = ParameterSample(values=np.array([1000, 2000, 3000]), unit="ug/L")
    assert ratio(a, b).gmr == pytest.approx(1)
    assert tost(a, b).gmr == pytest.approx(1)
    assert effect_size(a, b, "mean_diff").estimate == pytest.approx(0)
    result = compare(a, b, scale="linear")
    assert result.effect == pytest.approx(0)
    assert result.p_value == pytest.approx(1)
    if not summary:
        assert hodges_lehmann(a, b).effect == pytest.approx(0)


@pytest.mark.parametrize(
    "function", [ratio, compare, hodges_lehmann, tost, effect_size]
)
def test_incompatible_sample_units_raise(function):
    a = ParameterSample(values=np.array([1, 2, 3]), unit="mg/L")
    b = ParameterSample(values=np.array([1, 2, 3]), unit="hour")
    with pytest.raises(ValueError, match="Cannot compare units"):
        function(a, b)


def test_geometric_summary_conversion_retains_relative_variability():
    a = ParameterSample(geomean=2, geocv=0.3, n=10, unit="mg/L")
    b = ParameterSample(geomean=2000, geocv=0.3, n=10, unit="ug/L")
    actual, expected = ratio(a, b), ratio(a, a)
    assert actual.gmr == pytest.approx(expected.gmr)
    assert actual.ci_low == pytest.approx(expected.ci_low)
    assert actual.ci_high == pytest.approx(expected.ci_high)


@pytest.mark.parametrize("method", ["bh", "holm", "bonferroni"])
def test_missing_pvalues_do_not_poison_adjustments(method):
    actual = multiple_comparison([0.01, np.nan, 0.02], method=method)
    assert actual[[0, 2]] == pytest.approx(
        multiple_comparison([0.01, 0.02], method=method)
    )
    assert np.isnan(actual[1])


@pytest.mark.parametrize("paired", [True, False])
def test_hodges_lehmann_large_path_matches_materialized(monkeypatch, paired):
    a = ParameterSample(values=np.array([1.0, 2.0, 2.0, 4.0, 9.0, 15.0]))
    b = ParameterSample(values=np.array([2.0, 3.0, 3.0, 4.0, 6.0, 11.0]))
    expected = hodges_lehmann(a, b, paired=paired)
    monkeypatch.setattr(statistical_tests, "HL_MATERIALIZE_PAIRS", 0)
    actual = hodges_lehmann(a, b, paired=paired)
    np.testing.assert_equal(actual.to_dict(), expected.to_dict())


@pytest.mark.parametrize("paired", [True, False])
def test_pair_selector_every_order_statistic_with_ties_and_rounding(paired):
    rng = np.random.default_rng(42)
    for x, y in [
        (np.array([1.0, 2.0, 2.0, 3.0]), np.array([1.0, 1.0, 2.0, 4.0])),
        (rng.normal(size=9), rng.normal(size=7)),
        (np.array([1.0, np.nextafter(1.0, 2.0), 2.0]), np.array([1.0, 2.0])),
    ]:
        selector = statistical_tests._PairOrderStatistics(x, None if paired else y)
        expected = (
            statistical_tests._walsh_averages(x)
            if paired
            else np.sort((x[:, None] - y).ravel())
        )
        assert np.array([selector[i] for i in range(selector.size)]) == pytest.approx(
            expected, abs=0, rel=0
        )


def test_permutation_batch_preserves_seeded_results():
    a = ParameterSample(values=np.array([1, 2, 4, 8, 16]))
    b = ParameterSample(values=np.array([2, 3, 5, 10, 18]))
    small = compare(
        a,
        b,
        permutation_batch=7,
        test="permutation",
        scale="linear",
        n_perm=99,
        seed=42,
    )
    large = compare(
        a,
        b,
        permutation_batch=99,
        test="permutation",
        scale="linear",
        n_perm=99,
        seed=42,
    )
    assert small.p_value == large.p_value
    assert small.statistic == large.statistic


def test_offset_units_are_explicitly_rejected():
    a = ParameterSample(values=np.array([1.0, 2.0, 3.0]), unit="degC")
    b = ParameterSample(values=np.array([274.15, 275.15, 276.15]), unit="kelvin")
    with pytest.raises(ValueError, match="multiplicative"):
        ratio(a, b)


@pytest.mark.parametrize("values", [[-0.1, 0.1], [1.1, 0.1], [float("inf"), 0.1]])
def test_invalid_pvalues_are_rejected(values):
    with pytest.raises(ValueError, match="p values"):
        multiple_comparison(values)


def test_mann_whitney_distribution_at_exact_limit_preserves_combinatorics():
    from math import comb

    counts = statistical_tests._mann_whitney_counts(50, 50)
    assert counts[0] == counts[-1] == 1
    assert np.all(counts >= 0)
    np.testing.assert_array_equal(counts, counts[::-1])
    assert counts.sum() == pytest.approx(comb(100, 50), rel=2e-16)
    probabilities = counts / counts.sum()
    assert probabilities.sum() == pytest.approx(1)
    assert np.all(np.diff(np.cumsum(probabilities)) >= 0)


@pytest.mark.parametrize("size", [40, 50])
@pytest.mark.parametrize("level", [0.999999999999, np.nextafter(1.0, 0.0)])
def test_hodges_lehmann_extreme_interval_has_conservative_coverage(size, level):
    # Finite, distinct observations; no tie correction clouds the exact null.
    a = ParameterSample(values=np.arange(size, dtype=float))
    b = ParameterSample(values=np.arange(size, dtype=float) + 0.5)
    result = hodges_lehmann(a, b, paired=False, ci_level=level)
    assert result.ci_low <= result.effect <= result.ci_high
    assert np.isfinite(result.ci_low) and np.isfinite(result.ci_high)
    assert level <= result.ci_level <= 1
    assert result.ci_low == -result.ci_high - 1


@pytest.mark.parametrize("paired", [True, False])
def test_large_finite_pair_values_and_median_do_not_overflow(paired):
    x = np.array([1e308, 1.2e308, 1.1e308])
    y = None if paired else np.zeros(2)
    selector = statistical_tests._PairOrderStatistics(x, y)
    expected = (
        statistical_tests._walsh_averages(x) if paired else np.sort(np.repeat(x, 2))
    )
    with np.errstate(over="raise", invalid="raise"):
        actual = np.array([selector[i] for i in range(selector.size)])
        np.testing.assert_array_equal(actual, expected)
        assert selector.median() == pytest.approx(1.1e308)


@pytest.mark.parametrize("paired", [True, False])
def test_large_finite_hodges_lehmann_matches_both_memory_paths(monkeypatch, paired):
    a = ParameterSample(values=np.array([1e308, 1.2e308, 1.1e308]))
    b = ParameterSample(values=np.zeros(3))
    # Variance/effect-size moments can overflow independently of the finite
    # location estimate, so suppress their floating warnings in this test.
    with np.errstate(over="ignore", invalid="ignore"):
        expected = hodges_lehmann(a, b, paired=paired)
        monkeypatch.setattr(statistical_tests, "HL_MATERIALIZE_PAIRS", 0)
        actual = hodges_lehmann(a, b, paired=paired)
    assert actual.effect == expected.effect == pytest.approx(1.1e308)
    assert (actual.ci_low, actual.ci_high) == (expected.ci_low, expected.ci_high)


def test_pair_midpoint_preserves_subnormal_and_cancellation_precision():
    small = np.nextafter(0.0, 1.0)
    largest = np.finfo(float).max
    a = np.array([small, largest, largest, 1.0])
    b = np.array([small, largest, -largest, np.nextafter(1.0, 2.0)])
    with np.errstate(over="raise", invalid="raise"):
        actual = statistical_tests._midpoint(a, b)
    np.testing.assert_array_equal(actual, [small, largest, 0.0, 1.0])


@pytest.mark.parametrize("ci_level", [0, 1, -0.1, 1.1, np.nan, np.inf])
@pytest.mark.parametrize(
    "function", [ratio, tost, compare, hodges_lehmann, effect_size]
)
def test_invalid_confidence_level_rejected_consistently(function, ci_level):
    sample = ParameterSample(values=np.array([1, 2, 3]))
    with pytest.raises(ValueError, match="ci_level"):
        function(sample, sample, ci_level=ci_level)


@pytest.mark.parametrize("ci_level", [0, 1, np.nan])
def test_invalid_confidence_level_rejected_without_estimable_interval(ci_level):
    with pytest.raises(ValueError, match="ci_level"):
        summarize([1], ci_level=ci_level)
    with pytest.raises(ValueError, match="ci_level"):
        effects_from_arrays([], [], ci_level=ci_level)
    effects = effects_from_arrays([1], [1])
    for pool in (fixed_effect, random_effects):
        with pytest.raises(ValueError, match="ci_level"):
            pool(effects, ci_level=ci_level)


def test_confidence_level_just_below_one_has_finite_bounds():
    level = np.nextafter(1.0, 0.0)
    sample = ParameterSample(values=np.array([1, 2, 3, 4]))
    effect = effect_size(sample, sample, ci_level=level)
    assert np.isfinite(effect.ci_low) and np.isfinite(effect.ci_high)
    summary = summarize(sample, scale="linear", ci_level=level)
    assert np.isfinite(summary.ci_low) and np.isfinite(summary.ci_high)


@pytest.mark.filterwarnings("error")
@pytest.mark.parametrize("pool", [fixed_effect, random_effects])
@pytest.mark.parametrize("variance", [1e-310, np.nextafter(0.0, 1.0)])
def test_pooling_tiny_positive_variances_preserves_standard_error(pool, variance):
    result = pool(effects_from_arrays([1, 1], [variance, 2 * variance]))
    assert result.estimate == pytest.approx(1)
    assert result.weights == pytest.approx([2 / 3, 1 / 3])
    assert result.se > 0
    assert result.se / np.sqrt(variance) == pytest.approx(np.sqrt(2 / 3))
    assert result.tau2 == 0


@pytest.mark.filterwarnings("error")
def test_random_pooling_keeps_finite_tau_when_q_exceeds_float_range():
    effects = effects_from_arrays([1, 2], [1e-310, 2e-310])
    het = heterogeneity(effects)
    assert het.q == np.inf
    assert het.i2 == 100
    assert het.tau2 == pytest.approx(0.5)
    result = random_effects(effects)
    assert result.estimate == pytest.approx(1.5)
    assert result.se == pytest.approx(0.5)
    assert result.weights == pytest.approx([0.5, 0.5])


@pytest.mark.filterwarnings("error")
def test_log_moments_of_large_finite_summary_do_not_overflow():
    geometric = ParameterSample(geomean=1, geocv=1e200, n=10)
    mu, sigma = geometric.log_moments()
    assert mu == 0
    assert sigma == pytest.approx(np.sqrt(400 * np.log(10)))
    arithmetic = ParameterSample(mean=1e-200, sd=1e200, n=10)
    mu, sigma = arithmetic.log_moments()
    assert mu == pytest.approx(-600 * np.log(10))
    assert sigma == pytest.approx(np.sqrt(800 * np.log(10)))
    assert ratio(arithmetic, arithmetic).gmr == pytest.approx(1)


@pytest.mark.filterwarnings("error")
@pytest.mark.parametrize("mean,sd", [(1e-200, 1), (1e-200, 1e200), (1, 0)])
def test_large_log_variance_round_trip_retains_finite_arithmetic_moments(mean, sd):
    arithmetic = ParameterSample(mean=mean, sd=sd, n=10)
    restored_mean, restored_sd = moments_from_lognormal(*arithmetic.log_moments())
    assert restored_mean / mean == pytest.approx(1)
    if sd:
        assert restored_sd / sd == pytest.approx(1)
    else:
        assert restored_sd == 0


@pytest.mark.filterwarnings("error")
def test_geometric_summary_retains_large_finite_cv():
    result = summarize(ParameterSample(geomean=1, geocv=1e200, n=10))
    assert result.geocv / 1e200 == pytest.approx(1)


@pytest.mark.filterwarnings("error")
def test_dominant_inverse_variance_weight_keeps_between_study_variance():
    result = heterogeneity(effects_from_arrays([1, 3], [1e-20, 1]))
    assert result.q == pytest.approx(4)
    assert result.tau2 == pytest.approx(1.5)
