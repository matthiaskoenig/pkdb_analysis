"""Unit consistency at the public fitting boundaries."""

import numpy as np
import pytest
import xarray as xr

from pkpdutils.fit import FitOptions, Weighting, fit, fit_table
from pkpdutils.fit.model import Model, ModelParameter
from pkpdutils.fit.models import Linear
from pkpdutils.units import parse_unit


def _table() -> xr.Dataset:
    return xr.Dataset(
        {
            "x": ("point", np.arange(5.0), {"units": "hour"}),
            "y": ("point", [1.0, 2.0, 4.0, 4.0, 6.0], {"units": "mg/l"}),
            "sd": ("point", [1.0, 2.0, 1.0, 2.0, 1.0], {"units": "mg/l"}),
        }
    )


def test_fit_table_converts_sd_to_observation_units() -> None:
    """Equivalent SD units give identical fits, residuals and likelihood scores."""
    table = _table()
    options = FitOptions(weighting=Weighting.INV_SD)
    reference = fit_table(
        Linear(), table, "x", "y", dim="point", sd="sd", options=options
    )
    converted = table.copy(deep=True)
    converted["sd"] *= 1000
    converted["sd"].attrs["units"] = "ug/l"
    result = fit_table(
        Linear(), converted, "x", "y", dim="point", sd="sd", options=options
    )
    xr.testing.assert_allclose(result.ds, reference.ds)
    np.testing.assert_array_equal(converted["sd"], [1000, 2000, 1000, 2000, 1000])
    assert result.units("sd_data") == "mg/l"


def test_fit_table_sd_without_units_assumes_observation_units() -> None:
    table = _table()
    table["sd"].attrs.clear()
    result = fit_table(Linear(), table, "x", "y", dim="point", sd="sd")
    np.testing.assert_array_equal(result["sd_data"], table["sd"])
    assert result.units("sd_data") == "mg/l"


def test_fit_table_preserves_float64_input_views() -> None:
    """Stored float64 data retain views instead of allocating another batch."""
    table = _table()
    result = fit_table(Linear(), table, "x", "y", dim="point", sd="sd")
    for source, stored in (("x", "x_data"), ("y", "y_data"), ("sd", "sd_data")):
        assert np.shares_memory(table[source].to_numpy(), result[stored].to_numpy())


@pytest.mark.parametrize("weighting", [Weighting.NONE, Weighting.INV_SD])
def test_fit_table_rejects_incompatible_sd_units(weighting: Weighting) -> None:
    table = _table()
    table["sd"].attrs["units"] = "second"
    with pytest.raises(
        ValueError, match="Standard deviation 'sd' has incompatible units"
    ):
        fit_table(
            Linear(),
            table,
            "x",
            "y",
            dim="point",
            sd="sd",
            options=FitOptions(weighting=weighting),
        )


@pytest.mark.parametrize(
    ("weighting", "residual_unit"),
    [
        (Weighting.NONE, "mg/l"),
        (Weighting.INV_Y, "(mg/l)**0.5"),
        (Weighting.INV_Y2, "dimensionless"),
        (Weighting.INV_SD, "dimensionless"),
    ],
)
@pytest.mark.parametrize("loss", ["linear", "soft_l1", "huber", "cauchy", "arctan"])
def test_fit_reports_units_of_errors(
    weighting: Weighting, residual_unit: str, loss: str
) -> None:
    table = _table()
    result = fit(
        Linear(),
        table["x"],
        table["y"],
        sd=table["sd"],
        y_unit="mg/l",
        options=FitOptions(weighting=weighting, loss=loss),
    )
    assert parse_unit(result.units("rmse")) == parse_unit("mg/l")
    assert parse_unit(result.units("residuals")) == parse_unit(residual_unit)
    assert parse_unit(result.units("cost")) == parse_unit(f"({residual_unit})**2")


class _Flat(Model):
    parameters: tuple[ModelParameter, ...] = (
        ModelParameter("cost", "[y]", positive=False),
    )

    def predict(self, x: np.ndarray, p: np.ndarray) -> np.ndarray:
        return np.full_like(x, p[0])

    def initial_guess(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        raise AssertionError("Invalid model must be rejected before fitting")


@pytest.mark.parametrize(
    "name", ["cost", "rmse", "x_data", "flags", "parameter", "point"]
)
def test_fit_rejects_names_that_would_overwrite_parameters(name: str) -> None:
    model = _Flat()
    model.parameters = (ModelParameter(name, "[y]", positive=False),)
    with pytest.raises(ValueError, match="collides with a reserved result name"):
        fit(model, np.arange(4.0), np.full(4, 7.0))


@pytest.mark.parametrize("derived", [False, True])
def test_fit_rejects_duplicate_parameter_and_derived_names(derived: bool) -> None:
    parameter = ModelParameter("amplitude", "[y]", positive=False)
    model = type(
        "AmbiguousFlat",
        (_Flat,),
        {
            "parameters": (parameter,) if derived else (parameter, parameter),
            "derived_units": {"amplitude": "[y]"} if derived else {},
        },
    )()
    with pytest.raises(ValueError, match="must be unique"):
        fit(model, np.arange(4.0), np.full(4, 7.0))
