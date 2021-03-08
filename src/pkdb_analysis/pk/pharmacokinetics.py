"""
Helper functions for pharmacokinetic analysis.

Takes concentration~time curves in plasma as input for analysis.
Pharmacokinetic parameters are than calculated and returned.
"""
import warnings
from dataclasses import dataclass
from typing import List

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import Figure
from pint import Quantity, UnitRegistry
from scipy import stats


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    Quantity([])


@dataclass
class PKParametersNoDosing:
    """Pharmacokinetics parameters without dose."""

    compound: str
    auc: Quantity
    aucinf: Quantity
    tmax: Quantity
    cmax: Quantity
    tmaxhalf: Quantity
    cmaxhalf: Quantity
    kel: Quantity
    thalf: Quantity
    slope: Quantity
    intercept: Quantity
    r_value: float
    p_value: float
    std_err: float
    max_idx: int

    @property
    def parameters(self) -> List[str]:
        """Get parameter ids."""
        return ["auc", "aucinf", "tmax", "cmax", "tmaxhalf", "cmaxhalf", "kel", "thalf"]

    @property
    def regression_parameters(self) -> List[str]:
        """Get regression parameter ids."""
        return ["slope", "intercept", "r_value", "p_value", "std_err", "max_idx"]

    def to_dict(self):
        """Convert to dictionary.

        Splits all quantities in magnitude and unit parts.
        """
        d = {
            "compound": self.compound,
        }
        for key in self.parameters:
            q = getattr(self, key)
            d[key] = q.magnitude
            d[f"{key}_unit"] = q.units

        for key in self.regression_parameters:
            d[key] = getattr(self, key)
        return d


@dataclass
class PKParameters(PKParametersNoDosing):
    """Pharmacokinetics parameters with dose."""

    dose: Quantity
    vd: Quantity
    vdss: Quantity
    cl: Quantity

    @property
    def parameters(self) -> List[str]:
        """Get parameter ids."""
        return super().parameters + ["dose", "vd", "vdss", "cl"]


class TimecoursePKNoDosing:
    """Class for pharmacokinetics from timecourses without dose information."""

    def __init__(
        self,
        time: Quantity,
        concentration: Quantity,
        ureg: UnitRegistry,
        substance: str = "substance",
        min_treshold=1e6,
        **kwargs,
    ):

        self._init(time, concentration, ureg, substance, min_treshold, **kwargs)
        self.pk = self._f_pk()

    def _init(
        self,
        time: Quantity,
        concentration: Quantity,
        ureg: UnitRegistry,
        substance: str = "substance",
        min_treshold=1e8,
        **kwargs,
    ):
        self.ureg = ureg
        self.Q_ = ureg.Quantity

        if not isinstance(time, Quantity):
            raise ValueError(f"'time' must be a pint Quantity: {type(time)}")
        if not isinstance(concentration, Quantity):
            raise ValueError(
                f"'concentration' must be a pint Quantity: {type(concentration)}"
            )

        # check concentration is fitting to time
        assert time.size == concentration.size

        # for numerical simulations problems in calculations can arise
        # if values are getting too small
        cmin = np.nanmin(
            concentration[np.nonzero(concentration)]
        )  # only take non-zero values
        cmax = np.nanmax(concentration)
        if (min_treshold * cmin) < cmax:
            warnings.warn("Very small concentrations values are set to NaN.")
            concentration[concentration * min_treshold < cmax] = np.nan

        self.t = time
        self.c = concentration
        self.substance = substance

    def _f_pk(self) -> PKParametersNoDosing:
        """Calculate all pk parameters.

        The returned data structure can be used to
        - create a report with pk_report
        - create a visualization with pk_figure
        """
        c = self.c
        t = self.t
        # simple pk
        auc = self._auc(t, c)
        tmax, cmax = self._max(t, c)
        tmaxhalf, cmaxhalf = self._max_half(t, c)
        [slope, intercept, r_value, p_value, std_err, max_idx] = self._ols_regression(
            t, c
        )
        kel = self._kel(slope=slope)
        thalf = self._thalf(kel=kel)
        aucinf = self._aucinf(t, c, slope=slope, auc=auc)

        return PKParametersNoDosing(
            compound=self.substance,
            auc=auc.to_reduced_units(),
            aucinf=aucinf.to_reduced_units(),
            tmax=tmax.to_reduced_units(),
            cmax=cmax.to_reduced_units(),
            tmaxhalf=tmaxhalf.to_reduced_units(),
            cmaxhalf=cmaxhalf.to_reduced_units(),
            kel=kel.to_reduced_units(),
            thalf=thalf.to_reduced_units(),
            slope=slope.to_reduced_units(),
            intercept=intercept.to_reduced_units(),
            r_value=r_value,
            p_value=p_value,
            std_err=std_err,
            max_idx=max_idx,
        )

    def _ols_regression(self, t, c):
        """Linear regression on the log timecourse after maximal value.

        No check is performed if already in equilibrium distribution !.
        The linear regression is calculated from all data points after the maximum.

        :return:
        """
        slope_units = self.ureg.Unit(f"1/{t.units}")
        intercept_units = self.ureg.Unit(c.units)

        max_index = np.nanargmax(c)
        # at least three data points after maximum are required for a regression

        # FIXME:
        if max_index > (len(c) - 4):
            warnings.warn(
                "Regression could not be calculated, "
                "at least 3 data points after maximum required."
            )
            return [self.Q_(np.nan, slope_units), self.Q_(np.nan, intercept_units)] + [
                np.nan
            ] * 4

        # linear regression start regression on data point after maximum
        x = t.magnitude[max_index + 1 :]
        y = np.log(c.magnitude[max_index + 1 :])

        # using mask to remove nan values
        mask = ~np.isnan(x) & ~np.isnan(y)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask], y[mask])

        # handle possible regression issues
        if np.isnan(slope) or np.isnan(intercept):
            warnings.warn("Regression could not be calculated on timecourse curve.")
        elif slope > 0.0:
            warnings.warn(
                "Regression gave a positive slope, "
                "resulting in a negative elimination rate. "
                "Slope is set to NaN."
            )
            slope = np.nan
            intercept = np.nan

        slope = self.Q_(slope, slope_units)
        intercept = self.Q_(intercept, intercept_units)

        return [slope, intercept, r_value, p_value, std_err, max_index]

    def _auc(self, t: np.ndarray, c: np.ndarray, rm_nan: bool = True):
        """Calculate the area under the curve (AUC) via trapezoid rule.

        :param t = time array
        :param c = concentration array
        :param rm_nan = remove nan values array
        """
        if rm_nan:
            idx = np.where(~np.isnan(c))
            t, c = t[idx], c[idx]
        auc = np.sum((t[1:] - t[0:-1]) * (c[1:] + c[0:-1]) / 2.0)
        return auc

    def _aucinf(self, t, c, slope=None, auc=None, rm_nan: bool = True):
        """Area under the curve extrapolated to infinity.

        Calculate the area under the curve (AUC) via trapezoid rule
        and extrapolated to infinity.
        """
        if rm_nan:
            idx = np.where(~np.isnan(c))
            t, c = t[idx], c[idx]
        if not auc:
            auc = self._auc(t, c)

        # by integrating from tend to infinity for c[-1]exp(slope * t) we get

        auc_d = -c[-1] / slope

        print()

        if auc_d > auc:
            warnings.warn("AUC(t-oo) > AUC(0-tend), no AUC(0-oo) calculated.")
            # return self.Q_(np.nan, auc.units)

        if auc_d > 0.25 * auc:
            # If the % extrapolated is greater than 20%, than the total AUC may be unreliable.
            # The unreliability of the data is not due to a calculation error. Instead it
            # indicates that more sampling is needed for an accurate estimate of the elimination
            # rate constant and the observed area under the curve.
            warnings.warn(
                f"AUC(t-oo) is >25% ({round((auc_d/auc*100).magnitude, 2)}%) of total AUC, "
                f"calculation may be unreliable."
            )

        return auc + auc_d

    def _max(self, t, c):
        """Return timepoint of maximal value and maximal value based on curve.

        The tmax depends on the value of both the absorption rate constant (ka)
        and the elimination rate constant (kel).

        :return: tuple (tmax, cmax)
        """
        idx = np.nanargmax(c)
        return t[idx], c[idx]

    def _max_half(self, t, c):
        """Calculate timepoint of half maximal value.

        The max half is the timepoint before reaching the maximal value.

        :return: tuple (tmax, cmax)
        """
        try:
            idx = np.nanargmax(c)
            if idx == len(c) - 1:
                warnings.warn("No MAXIMUM reached within time course, last value used.")
            if idx == 0:
                # no maximum in time course
                return self.Q_(np.nan, t.units), self.Q_(np.nan, c.units)

            cmax = c[idx]
            tnew = t[:idx]
            cnew = np.abs(c[:idx] - 0.5 * cmax)
            idx_half = np.nanargmin(cnew)
            return tnew[idx_half], c[idx_half]
        except ValueError:
            # often only NaN values before maximum (e.g., iv dosing)
            return self.Q_(np.nan, t.units), self.Q_(np.nan, c.units)

    def _kel(self, slope):
        """Elimination rate constant.

        Elimination half-life (t1/2) and elimination rate constant were
        computed by linear regression of the log plasma concentrations vs.
        time after the maximum.

        c(t) = c0 * exp(-kel*t)
        log(c(t)) = log(c0) - kel* t

        Elimination rate constant (kel): Fractional rate of drug removal from the body.
        This rate is constant in first-order kinetics and is independent of
        drug concentration in the body. kel is the slope of the plasma concentration-time
        line (on a logarithmic y scale).
        """
        return -slope

    def _kel_cv(self, std_err=None, slope=None):
        return std_err / slope

    def _thalf(self, kel):
        """Calculate the half-life using the elimination constant.

        Definition: Time it takes for the plasma concentration or the amount
        of drug in the body to be reduced by 50%.

        Half-life determines the length of the drug effect. It also indicates
        whether accumulation of the drug will occur under a multiple dosage regimen
        and it is essential to decide on the appropriate dosing interval.

        If no kel is provided t and c must be provided for calculation
        of the elimination constant.
        """
        # np.log is natural logarithm, i.e. ln(2)
        return np.log(2) / kel

    def _thalf_cv(self, kel_cv):
        return np.log(2) / kel_cv

    def info(self) -> str:
        """Information string for given pharmacokinetic information.

        :return:
        """
        lines = []
        lines.append("-" * 80)
        lines.append(self.pk.compound)
        lines.append("-" * 80)
        for key in self.pk.regression_parameters:
            lines.append("{:<12}: {:>3.3f}".format(key, getattr(self.pk, key)))
        lines.append("-" * 80)
        for key in self.pk.parameters:
            lines.append("{:<12}: {:P}".format(key, getattr(self.pk, key)))
        lines.append("-" * 80)
        return "\n".join(lines)

    def figure(self, title=None) -> Figure:
        """Create figure from time course and pharmacokinetic parameters."""
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
        for ax in (ax1, ax2):
            if title is None:
                title = self.pk.compound
            ax.set_title(title)
            ax.set_xlabel(f"time [{self.t.units}]")
            ax.set_ylabel(f"concentration [{self.c.units}]")

        t = self.t.magnitude
        c = self.c.magnitude
        slope = self.pk.slope.magnitude
        intercept = self.pk.intercept.magnitude
        max_idx = self.pk.max_idx
        if max_idx is None or np.isnan(max_idx):
            max_idx = c.size - 1

        # pharmacokinetic parameters
        cmax = self.pk.cmax.magnitude
        tmax = self.pk.tmax.magnitude

        # aucinf
        tend = t[-1]
        cend = c[-1]

        for ax in (ax1, ax2):

            # auc
            ax.fill_between(
                t, np.zeros_like(c), c, color="green", alpha=0.2, label="AUCend"
            )
            ax.plot((tend, tend), (0, cend), linestyle="-", color="black")

            # aucinf
            t_aucinf = np.linspace(0, 0.3 * tend, 50)  # interpolate by 30%
            c_aucinf = cend * np.exp(slope * t_aucinf)
            ax.fill_between(
                tend + t_aucinf,
                c_aucinf,
                np.zeros_like(c_aucinf),
                color="red",
                alpha=0.2,
                label="AUCinf",
            )
            ax.plot(tend + t_aucinf, c_aucinf, linestyle="-", color="black")

            # fit
            if not np.isnan(slope):
                ax.plot(
                    t,
                    np.exp(intercept) * np.exp(slope * t),
                    "-",
                    color="blue",
                    label="fit",
                    linewidth=2.0,
                )
            # cmax (hline)
            ax.plot((0, tmax), (cmax, cmax), linestyle="--", color="black")
            # tmax (vline)
            ax.plot((tmax, tmax), (0, cmax), linestyle="--", color="black")

            ax.plot(t, c, "o-", color="black", markersize=6, linewidth=2)

            # plot data points used for fitting
            if not np.isnan(slope):
                if max_idx < c.size - 1:
                    ax.plot(
                        t[max_idx + 2 :],
                        c[max_idx + 2 :],
                        "s",
                        color="blue",
                        linewidth=2,
                        markersize=8,
                    )
            ax.annotate("(tmax, cmax)", xy=(tmax, cmax))

        ax1.set_ylim(bottom=0)
        ax2.set_yscale("log")

        for ax in (ax1, ax2):
            ax.set_xlim(left=0)
            ax.legend()
        return fig


class TimecoursePK(TimecoursePKNoDosing):
    """Class for calculating pharmacokinetics from timecourses."""

    def __init__(
        self,
        time: Quantity,
        concentration: Quantity,
        dose: Quantity,
        ureg: UnitRegistry,
        intervention_time: Quantity = None,
        substance: str = "substance",
        min_treshold=1e6,
        **kwargs,
    ):
        """Pharmacokinetics parameters are calculated for a single dose experiment.

        TODO: support errors on concentrations which are then used in calculation
        FIXME: ctype is used in kwargs for "value", "mean", "median", but not
         processed

        tmax values are reported relative to intervention time

        :param time: ndarray (with units)
        :param concentration: ndarray (with units)
        :param dose: dose of the test substance (with units)
        :param ureg: unit registry, allowing to calculate the pk in the respective unit system
        :param substance: name of compound/substance
        :param intervention_time: time of intervention (with unit)

        :return: pharmacokinetic parameters
        """
        self._init(time, concentration, ureg, substance, min_treshold, **kwargs)
        if intervention_time is None:
            intervention_time = self.Q_(0.0, "hr")
        if dose is None:
            dose = self.Q_(np.nan, "mg")
        if not isinstance(dose, Quantity):
            raise ValueError(f"'dose' must be a pint Quantity: {type(dose)}")
        if not isinstance(intervention_time, Quantity):
            raise ValueError(
                f"'intervention_time' must be a pint Quantity: {type(intervention_time)}"
            )

        # check dimensionality of dose
        dr = (
            dose.to_base_units().to_reduced_units()
        )  # see https://github.com/hgrecco/pint/issues/1058
        if not (
            dr.check("[mass]")
            or dr.check("[substance]")
            or dr.check("[mass]/[mass]")
            or dr.check("[substance]/[mass]")
        ):
            warnings.warn(
                f"dose_reduced.dimensionality must either be in '[mass]', '[substance']', '[mass]/[mass]' or '[substance]/[mass]'"
                f"The given units are: '{dr.dimensionality}' for {dr.units}. "
                f"Check that dose units are correct."
            )
            raise ValueError(
                f"Incorrect dimensionality '{dr.dimensionality}' for dose: {dose.units}"
            )

        self.dose = dose
        # convert dosing time to units of timecourse
        self.intervention_time = intervention_time.to(time.units)
        self.substance = substance
        self.pk = self._f_pk()

    def _f_pk(self) -> PKParameters:
        """Calculate all pk parameters from given time course.

        The returned data structure can be used to
        - create a report with pk_report
        - create a visualization with pk_figure

        """
        # calculate all results relative to the intervention time
        t = self.t - self.intervention_time
        c = self.c

        # simple pk
        auc = self._auc(t, c)
        tmax, cmax = self._max(t, c)
        tmaxhalf, cmaxhalf = self._max_half(t, c)

        [slope, intercept, r_value, p_value, std_err, max_idx] = self._ols_regression(
            t, c
        )

        kel = self._kel(slope=slope)
        thalf = self._thalf(kel=kel)
        aucinf = self._aucinf(t, c, auc=auc, slope=slope)

        if self.dose is not None and not np.isnan(self.dose.magnitude):
            # parameters depending on dose
            vdss = self._vdss(dose=self.dose, intercept=intercept)
            vd = self._vd(aucinf=aucinf, dose=self.dose, kel=kel)
            cl = kel * vd
        else:
            vd_units = self.dose.units / (auc.units / kel.units)
            vdss = self.Q_(np.nan, vd_units)
            vd = self.Q_(np.nan, vd_units)
            cl = self.Q_(np.nan, kel.units * vd.units)

        # perform unit normalization on volumes
        vd.to_base_units().to_reduced_units(),  # see https://github.com/hgrecco/pint/issues/1058
        vdss.to_base_units().to_reduced_units(),  # see https://github.com/hgrecco/pint/issues/1058
        for vd_par in [vd, vdss]:
            if vd_par.check("[length] ** 3"):
                vd_par.ito("liter")
            elif vd_par.check("[length] ** 3/[mass]"):
                vd_par.ito("liter/kg")

        return PKParameters(
            compound=self.substance,
            dose=self.dose.to_reduced_units(),
            auc=auc.to_reduced_units(),
            aucinf=aucinf.to_reduced_units(),
            tmax=tmax.to_reduced_units(),
            cmax=cmax.to_reduced_units(),
            tmaxhalf=tmaxhalf.to_reduced_units(),
            cmaxhalf=cmaxhalf.to_reduced_units(),
            kel=kel.to_reduced_units(),
            thalf=thalf.to_reduced_units(),
            vd=vd,
            vdss=vdss,
            cl=cl.to_reduced_units(),
            slope=slope.to_reduced_units(),
            intercept=intercept.to_reduced_units(),
            r_value=r_value,
            p_value=p_value,
            std_err=std_err,
            max_idx=max_idx,
        )

    def _vdss(self, dose, intercept=None):
        """Apparent volume of distribution.

        Not a physical space, but a dilution space.

        Definition: Fluid volume that would be required to contain the amount of drug present
        in the body at the same concentration as in the plasma.

        Calculation: The Vd is calculated as the ratio of the dose present in the body
        and its plasma concentration, when the distribution of the drug between
        the tissues and the plasma is at equilibrium. The extrapolated plasma concentration
        at time 0, C(0), is back-extrapolated from the slope of the elimination phase of
        the semilogarithmic plasma concentration vs. time decay curve.

        If both the dose (mg/kg) and the drug concentration in plasma
        (the Y intercept of the terminal component of the plasma drug concentration [PDC] versus time curve)
        are known, then an "apparent" volume of distribution can be calculated from Vd = dose/PDC.
        This theoretical volume describes the volume to which the drug must be distributed
        if the concentration in plasma represents the concentration throughout the body
        (i.e., distribution has reached equilibrium).
        The term "apparent" underscores the fact that where the drug is distributed cannot be
        determined from Vd; only that it goes somewhere.
        """
        return dose / self.Q_(np.exp(intercept.magnitude), intercept.units)

    def _vd(self, aucinf, dose, kel):
        """Apparent volume of distribution.

        Not a physical space, but a dilution space.

        Volume of distribution is calculated via
            vd = Dose/(AUC_inf*kel)
        """
        vd = dose / (aucinf * kel)
        return vd
