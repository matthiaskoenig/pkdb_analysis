"""
Helper functions for pharmacokinetic analysis.

Takes concentration~time curves in plasma as input for analysis.
Pharmacokinetic parameters are than calculated and returned.
"""
import warnings

import numpy as np
import pandas as pd
from scipy import stats
from dataclasses import dataclass
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import Figure


# TODO: add estimation of confidence intervals (use also the errorbars on the curves)

import pint
from pint import Quantity
from pint.errors import DimensionalityError

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    Quantity([])

@dataclass
class PKParameters:
    compound: str
    dose: Quantity
    auc: Quantity
    aucinf: Quantity
    tmax: Quantity
    cmax: Quantity
    tmaxhalf: Quantity
    cmaxhalf: Quantity
    kel: Quantity
    thalf: Quantity
    vd: Quantity
    vdss: Quantity
    cl: Quantity
    slope: Quantity
    intercept: Quantity
    r_value: float
    p_value: float
    std_err: float
    max_idx: int


class PKInference(object):
    def __init__(self, time, concentration, dose,
                 intervention_time=Q_(0, "hr"), substance="substance"):
        """The given doses must be in absolute amount, not per bodyweight. If doses are given per bodyweight, e.g. [mg/kg]
        these must be multiplied with the bodyweight before calling this function.

        :param time: ndarray (with units)
        :param concentration: ndarray (with units)
        :param dose: dose of the test substance (with unit)
        :param substance: name of compound/substance
        :param intervention_time: time of intervention (with unit)

        :return: pharmacokinetic parameters
        """
        if not isinstance(time, Quantity):
            raise ValueError(f"'time' must be a pint Quantity: {type(dose)}")
        if not isinstance(concentration, Quantity):
            raise ValueError(f"'concentration' must be a pint Quantity: {type(dose)}")
        if not isinstance(dose, Quantity):
            raise ValueError(f"'dose' must be a pint Quantity: {type(dose)}")
        if not isinstance(intervention_time, Quantity):
            raise ValueError(f"'intervention_time' must be a pint Quantity: {type(dose)}")

        try:
            (dose.units/Q_("liter")).to(concentration.units)
        except DimensionalityError as err:
            warnings.warn("dose units per liter must be convertible to concentration.")
            raise err

        assert time.size == concentration.size

        self.t = time
        self.c = concentration
        self.dose = dose
        self.intervention_time = intervention_time
        self.substance = substance

        self.pk = self._f_pk()

    def _f_pk(self) -> PKParameters:
        """ Calculates all pk parameters from given time course.

        The returned data structure can be used to
        - create a report with pk_report
        - create a visualization with pk_figure

        """
        # calculate all results relative to the intervention time
        t = self.t + self.intervention_time
        c = self.c

        # simple pk
        auc = self._auc(t, c)
        tmax, cmax = self._max(t, c)
        tmaxhalf, cmaxhalf = self._max_half(t, c)

        [slope, intercept, r_value, p_value, std_err, max_idx] = self._ols_regression(t, c)
        if np.isnan(slope) or np.isnan(intercept):
            warnings.warn("Regression could not be calculated on timecourse curve.")

        kel = self._kel(slope=slope)
        thalf = self._thalf(kel=kel)
        aucinf = self._aucinf(t, c, slope=slope)

        if self.dose is not None:
            vdss = self._vdss(dose=self.dose, intercept=intercept)
            vd = self._vd(aucinf=aucinf, dose=self.dose, kel=kel)
            cl = kel * vd
        else:
            vd_units = self.dose.units/(auc.units/kel.units)
            vdss = Q_(np.nan, vd_units)
            vd = Q_(np.nan, vd_units)
            cl = Q_(np.nan, kel.units*vd.units)

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
            vd=vd.to_reduced_units(),
            vdss=vdss.to_reduced_units(),
            cl=cl.to_reduced_units(),
            slope=slope.to_reduced_units(),
            intercept=intercept.to_reduced_units(),
            r_value=r_value,
            p_value=p_value,
            std_err=std_err,
            max_idx=max_idx
        )

    def _ols_regression(self, t, c):
        """Linear regression on the log timecourse after maximal value.

        No check is performed if already in equilibrium distribution !.
        The linear regression is calculated from all data points after the maximum.

        :return:
        """
        max_index = np.argmax(c)
        # at least two data points after maximum are required for a regression
        if max_index > (len(c) - 3):
            return [np.nan] * 6

        # linear regression start regression on data point after maximum
        x = t.magnitude[max_index + 1:]
        y = np.log(c.magnitude[max_index + 1:])

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        slope = Q_(slope, 1/t.units)
        intercept = Q_(intercept, c.units)

        if slope > 0.0:
            warnings.warn("Regression gave a positive slope, "
                          "resulting in a negative elimination rate."
                          "This is not allowed. Slope is set to NaN.")
            slope = np.NAN

        return [slope, intercept, r_value, p_value, std_err, max_index]

    def _auc(self, t, c):
        """ Calculates the area under the curve (AUC) via trapezoid rule """
        auc = np.sum((t[1:] - t[0:-1]) * (c[1:] + c[0:-1]) / 2.0)
        return auc

    def _aucinf(self, t, c, slope=None):
        """ Calculates the area under the curve (AUC) via trapezoid rule
            and extrapolated to infinity """
        auc = self._auc(t, c)

        # by integrating from tend to infinity for c[-1]exp(slope * t) we get
        auc_d = -c[-1]/slope

        auc_tot = auc + auc_d
        if auc_d > 0.2*auc_tot:
            # If the % extrapolated is greater than 20%, than the total AUC may be unreliable.
            # The unreliability of the data is not due to a calculation error. Instead it
            # indicates that more sampling is needed for an accurate estimate of the elimination
            # rate constant and the observed area under the curve.
            warnings.warn("AUC(t-oo) is > 20% of total AUC, calculation may be unreliable.")

        return auc_tot

    def _max(self, t, c):
        """ Returns timepoint of maximal value and maximal value based on curve.

        The tmax depends on the value of both the absorption rate constant (ka)
        and the elimination rate constant (kel).

        :return: tuple (tmax, cmax)
        """
        idx = np.nanargmax(c)
        return t[idx], c[idx]

    def _max_half(self, t, c):
        """ Calculates timepoint of half maximal value.

        The max half is the timepoint before reaching the maximal value.

        The tmax depends on the value of both the absorption rate constant (ka)
        and the elimination rate constant (kel).

        :return: tuple (tmax, cmax)
        """
        idx = np.argmax(c)
        if idx == len(c) - 1:
            # no maximum reached within the time course
            #raise serializers.ValidationError({"timecourse": "No MAXIMUM reached within time course, last value used."})
            warnings.warn("No MAXIMUM reached within time course, last value used.")
        if idx == 0:
            # no maximum in time course
            return Q_(np.nan, t.units), Q_(np.nan, c.units)

        cmax = c[idx]
        tnew = t[:idx]
        cnew = np.abs(c[:idx] - 0.5 * cmax)
        idx_half = np.argmin(cnew)

        return tnew[idx_half], c[idx_half]

    def _kel(self, slope):
        """
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
        """ Calculates the half-life using the elimination constant.

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

    def _vdss(self, dose, intercept=None):
        """
        Apparent volume of distribution.
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
        return dose / Q_(np.exp(intercept.magnitude), intercept.units)

    def _vd(self, aucinf, dose, kel):
        """
        Apparent volume of distribution.
        Not a physical space, but a dilution space.

        Volume of distribution is calculated via
            vd = Dose/(AUC_inf*kel)
        """
        vd = dose / (aucinf*kel)
        print("vd", vd)
        return vd

    def info(self) -> str:
        """ Print report for given pharmacokinetic information.

        :return:
        """
        lines = []
        lines.append("-" * 80)
        lines.append(self.pk.compound)
        lines.append("-" * 80)
        for key in ["slope", "intercept", "r_value", "p_value", "std_err"]:
            lines.append("{:<12}: {:>3.3f}".format(key, getattr(self.pk, key)))
        lines.append("-" * 80)
        for key in [
            "dose",
            "auc",
            "aucinf",
            "tmax",
            "cmax",
            "tmaxhalf",
            "cmaxhalf",
            "kel",
            "thalf",
            "vd",
            "vdss",
            "cl",
        ]:
            lines.append(
                "{:<12}: {:P}".format(key, getattr(self.pk, key))
            )

        return "\n".join(lines)

    def figure(self) -> Figure:
        """
        Create figure from time course and pharmacokinetic parameters.
        """
        c = self.c.magnitude
        t = self.c.magnitude
        c_unit = self.c.units
        t_unit = self.t.units
        slope = self.pk.slope.magnitude
        intercept = self.pk.intercept.magnitude
        max_idx = self.pk.max_idx
        if max_idx is None or np.isnan(max_idx):
            max_idx = c.size - 1

        kwargs = {"markersize": 10}

        # create figure
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        f.subplots_adjust(wspace=0.3)

        ax1.plot(t, c, "--", color="black", label="__nolabel__", **kwargs)
        ax1.plot(t[: max_idx + 1], c[: max_idx + 1], "o", color="darkgray", **kwargs)
        if max_idx < c.size - 1:
            ax1.plot(
                t[max_idx + 1:],
                c[max_idx + 1:],
                "s",
                color="black",
                linewidth=2,
                **kwargs
            )

        ax1.set_ylabel("substance [{}]".format(c_unit))
        ax1.set_xlabel("time [{}]".format(t_unit))

        ax1.plot(t, np.exp(intercept) * np.exp(slope * t), "-", color="blue", label="fit")
        ax1.legend()

        # log
        ax2.plot(t[1:], np.log(c[1:]), "--", color="black", label="__nolabel__", **kwargs)

        ax2.plot(
            t[1: max_idx + 1],
            np.log(c[1: max_idx + 1]),
            "o",
            color="darkgray",
            label="log(substance)",
            **kwargs
        )
        if max_idx < c.size - 1:
            ax2.plot(
                t[max_idx + 1:],
                np.log(c[max_idx + 1:]),
                "s",
                color="black",
                linewidth=2,
                label="log(substance) fit",
                **kwargs
            )

        ax2.set_ylabel("log(substance [{}])".format(c_unit))
        ax2.set_xlabel("time [{}]".format(t_unit))
        ax2.plot(t, intercept + slope * t, "-", color="blue", label="fit")
        ax2.legend()

        return f


if __name__ == "__main__":
    t = np.linspace(0, 100, num=50)
    kel = 1.0
    c0 = 10.0
    dose = Q_(10.0, "mg") * Q_(1.0, "mole/g")
    c = c0 * np.exp(-kel*t)

    pk = PKInference(time=Q_(t, "hr"), concentration=Q_(c, "nmol/l"),
                     dose=dose)
    print(pk.info())

