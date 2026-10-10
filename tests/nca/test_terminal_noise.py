"""Public regressions for terminal fits at simulated integrator noise levels."""

import numpy as np
import pytest
import xarray as xr

from pkpdutils import (
    BLQAction,
    BLQRules,
    NCAOptions,
    TerminalMethod,
    TerminalPhase,
    Timecourse,
    Timecourses,
    nca,
    nca_single,
)
from pkpdutils.nca.options import NCAFlag, deserialize_nca_options


def noisy_curve(scale: float = 1.0) -> Timecourse:
    """A genuine decay followed by a smoother, slower numerical tail."""
    time = np.arange(0.0, 1001.0, 10.0)
    value = np.exp(-0.1 * time)
    tail = time >= 400
    value[tail] = 1e-18 * np.exp(-0.02 * (time[tail] - 400))
    return Timecourse(time=time, value=scale * value, time_unit="min", unit="mg/l")


def test_default_warns_without_changing_terminal_fit(
    caplog: pytest.LogCaptureFixture,
) -> None:
    curve = noisy_curve()
    with caplog.at_level("WARNING", logger="pkpdutils.nca.nca"):
        result = nca_single(curve)
    assert result["thalf"].item() == pytest.approx(np.log(2) / 0.02)
    assert "TERMINAL_LOW_CONCENTRATION" in result.flags()
    assert "1 curve(s)" in caplog.text
    assert "lloq_relative=1e-8" in caplog.text
    assert result["lambda_z_t_first"].item() == 400
    assert result["lambda_z_t_last"].item() == 1000


@pytest.mark.parametrize("scale", [1e-200, 1e-6, 1.0, 1e6, 1e200])
def test_relative_cutoff_recovers_true_decay_independently_of_scale(
    scale: float,
) -> None:
    curve = noisy_curve(scale)
    original = curve.value.copy()
    result = nca_single(curve, options=NCAOptions(lloq_relative=1e-8))
    reference = nca_single(curve, options=NCAOptions(lloq=1e-8 * scale))
    xr.testing.assert_allclose(result.ds, reference.ds)
    assert result["thalf"].item() == pytest.approx(np.log(2) / 0.1)
    assert result["lambda_z_t_last"].item() == 180
    assert "BLQ_TRUNCATED" in result.flags()
    assert "TERMINAL_LOW_CONCENTRATION" not in result.flags()
    np.testing.assert_array_equal(curve.value, original)


def test_cutoff_is_resolved_per_sample_and_absolute_limit_is_respected() -> None:
    curves = [noisy_curve(), noisy_curve(1e-4)]
    curves[1] = curves[1].model_copy(update={"lloq": 1e-8})
    batch = Timecourses.from_timecourses(curves)
    result = nca(batch, options=NCAOptions(lloq_relative=1e-8))
    for index, limit in enumerate([1e-8, 1e-8]):
        reference = nca_single(curves[index], options=NCAOptions(lloq=limit))
        assert (
            result["lambda_z_t_last"].values[index]
            == reference["lambda_z_t_last"].item()
        )
    # An analysis-wide absolute limit overrides the sample assay limit,
    # then combines with the relative floor independently for each sample.
    override = nca(batch, options=NCAOptions(lloq=1e-10, lloq_relative=1e-8))
    assert override["lambda_z_t_last"].values.tolist() == [180.0, 130.0]


def test_warning_can_be_disabled_without_changing_results(
    caplog: pytest.LogCaptureFixture,
) -> None:
    result = nca_single(
        noisy_curve(), options=NCAOptions(terminal=TerminalPhase(relative_warning=None))
    )
    assert result["thalf"].item() == pytest.approx(np.log(2) / 0.02)
    assert "TERMINAL_LOW_CONCENTRATION" not in result.flags()
    assert "numerical noise" not in caplog.text


def test_warning_checks_only_selected_manual_points() -> None:
    curve = Timecourse(
        time=[0, 1, 2, 3, 4],
        value=[1, np.exp(-1), 1e-20, np.exp(-3), np.exp(-4)],
        time_unit="h",
        unit="mg/l",
    )
    result = nca_single(
        curve,
        options=NCAOptions(
            terminal=TerminalPhase(method=TerminalMethod.MANUAL, points=(1, 3, 4))
        ),
    )
    assert result["lambda_z"].item() == pytest.approx(1.0)
    assert "TERMINAL_LOW_CONCENTRATION" not in result.flags()


def test_relative_limit_follows_blq_rules_without_regressing_kept_noise() -> None:
    rules = BLQRules(last=BLQAction.KEEP)
    result = nca_single(
        noisy_curve(), options=NCAOptions(lloq_relative=1e-8, blq=rules)
    )
    assert result["lambda_z_t_last"].item() == 180
    assert result["thalf"].item() == pytest.approx(np.log(2) / 0.1)
    assert "TERMINAL_LOW_CONCENTRATION" not in result.flags()
    assert result["auc_all"].item() > result["auc_last"].item()


def test_named_partial_areas_follow_relative_cutoff() -> None:
    curve = noisy_curve()
    relative = nca_single(
        curve, options=NCAOptions(lloq_relative=1e-8, partial_aucs={"late": (200, 500)})
    )
    absolute = nca_single(
        curve, options=NCAOptions(lloq=1e-8, partial_aucs={"late": (200, 500)})
    )
    xr.testing.assert_allclose(relative.ds, absolute.ds)
    assert np.isfinite(relative["late"].item())
    assert "PARTIAL_EXTRAPOLATED" in relative.flags()


def test_relative_cutoff_is_recorded_in_provenance() -> None:
    options = NCAOptions(
        lloq_relative=1e-8, terminal=TerminalPhase(relative_warning=1e-9)
    )
    result = nca_single(noisy_curve(), options=options)
    recorded = deserialize_nca_options(result.ds.attrs["nca_options"])
    assert recorded.lloq_relative == options.lloq_relative
    assert recorded.terminal == options.terminal


@pytest.mark.parametrize("method", ["bootstrap", "delta"])
def test_uncertainty_uses_relative_cutoff(method: str) -> None:
    curve = noisy_curve()
    group = Timecourse(
        time=curve.time,
        value=curve.value,
        time_unit=curve.time_unit,
        unit=curve.unit,
        sd=np.abs(curve.value) * 0.001,
        n=10,
    )
    common = NCAOptions(uncertainty=method, n_boot=12, seed=7, chunk_rows=20)
    relative = nca_single(
        group, options=common.model_copy(update={"lloq_relative": 1e-8})
    )
    absolute = nca_single(group, options=common.model_copy(update={"lloq": 1e-8}))
    xr.testing.assert_allclose(relative.ds, absolute.ds)
    assert relative["thalf"].item() == pytest.approx(np.log(2) / 0.1)
    assert 0 < relative["thalf_se"].item() < 1


def test_manual_window_is_also_diagnosed() -> None:
    result = nca_single(
        noisy_curve(),
        options=NCAOptions(terminal=TerminalPhase(windows={"*": (400, 1000)})),
    )
    assert "TERMINAL_LOW_CONCENTRATION" in result.flags()
    assert result["thalf"].item() == pytest.approx(np.log(2) / 0.02)


def test_all_after_tmax_uses_every_eligible_point() -> None:
    curve = Timecourse(
        time=[0, 1, 2, 3, 4, 5],
        value=np.exp([0, -1, -1.5, -2, -2.5, -3]),
        time_unit="min",
        unit="mg/l",
    )
    result = nca_single(
        curve, options=NCAOptions(terminal=TerminalPhase(method="all_after_tmax"))
    )
    assert result["lambda_z_n_points"].item() == 5
    assert result["lambda_z_t_first"].item() == 1
    assert result["lambda_z"].item() == pytest.approx(0.5)


@pytest.mark.parametrize("value", [0.0, -1.0, 1.0, np.nan, np.inf, -np.inf])
def test_invalid_relative_fractions_are_rejected(value: float) -> None:
    with pytest.raises(ValueError, match="lloq_relative"):
        NCAOptions(lloq_relative=value)
    with pytest.raises(ValueError, match="relative_warning"):
        TerminalPhase(relative_warning=value)


def test_effect_curves_reject_a_relative_concentration_limit() -> None:
    with pytest.raises(ValueError, match="concentration"):
        NCAOptions(kind="effect", lloq_relative=1e-8)


def test_missing_and_zero_curves_do_not_warn() -> None:
    batch = Timecourses.from_arrays(
        [0, 1, 2], [[np.nan] * 3, [0] * 3], time_unit="h", unit="mg/l"
    )
    result = nca(batch, options=NCAOptions(lloq_relative=1e-8))
    assert not (result["flags"].values & int(NCAFlag.TERMINAL_LOW_CONCENTRATION)).any()
