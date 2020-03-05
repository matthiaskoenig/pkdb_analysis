"""
Helper functions for pharmacokinetic analysis.

Takes concentration~time curves in plasma as input for analysis.
Pharmacokinetic parameters are than calculated and returned.
"""
import warnings

import numpy as np
import pandas as pd

from scipy import stats

# TODO: add estimation of confidence intervals (use also the errorbars on the curves)
# Currently only simple calculation of pharmacokinetic parameters


# TODO: Refactor in class to cache regressions

def f_pk(
        t,
        c,
        compound,
        dose=np.nan,
        bodyweight=np.nan,
        t_unit="h",
        c_unit="mg/L",
        dose_unit="mg",
        vd_unit="L",
        bodyweight_unit="kg",
        intervention_time=0,
):
    """ Calculates all the pk parameters from given time course.

    The returned data structure can be used to
    - create a report with pk_report
    - create a visualization with pk_figure

    The given doses must be in absolute amount, not per bodyweight. If doses are given per bodyweight, e.g. [mg/kg]
    these must be multiplied with the bodyweight before calling this function.

    :param t: time vector
    :param c: concentration vector corresponding to time vector
    :param compound: name of compound/substance
    :param dose: given dose of the test substance (absolute amount, not per bodyweight)
    :param bodyweight: bodyweight
    :param t_unit: time unit
    :param c_unit: concentration unit
    :param dose_unit: dose unit
    :param vd_unit: unit for volume of distribution (normally [L])
    :param bodyweight_unit: unit of bodyweight (normally [kg])

    :return: dict with pharmacokinetic paramatern and information
    """
    # make sure we work on ndarrays
    if isinstance(t, pd.core.series.Series):
        t = np.copy(t.values)
    if isinstance(c, pd.core.series.Series):
        c = np.copy(c.values)
    assert isinstance(t, np.ndarray)
    assert isinstance(c, np.ndarray)
    assert t.size == c.size

    # calculate all results relative to the intervention time
    t = t + intervention_time

    # calculate pk
    auc = _auc(t, c)
    tmax, cmax = _max(t, c)
    tmaxhalf, cmaxhalf = _max_half(t, c)

    [slope, intercept, r_value, p_value, std_err, max_idx] = _regression(t, c)
    if np.isnan(slope) or np.isnan(intercept):
        warnings.warn("Regression could not be calculated on timecourse curve.")

    kel = _kel(t, c, slope=slope)
    thalf = _thalf(t, c, slope=slope)
    aucinf = _aucinf(t, c, slope=slope, intercept=intercept)

    if dose is not None:
        vdss = _vdss(t, c, dose, intercept=intercept)
        vd = _vd(t, c, dose)
        cl = kel * vdss
    else:
        vdss = np.nan
        cl = np.nan

    return {
        "compound": compound,
        "dose": dose,
        "dose_unit": dose_unit,
        "bodyweight": bodyweight,
        "bodyweight_unit": bodyweight_unit,
        "auc": auc,
        "auc_unit": "({})*({})".format(c_unit, t_unit),
        "aucinf": aucinf,
        "aucinf_unit": "({})*({})".format(c_unit, t_unit),
        "tmax": tmax,
        "tmax_unit": t_unit,
        "cmax": cmax,
        "cmax_unit": c_unit,
        "tmaxhalf": tmaxhalf,
        "tmaxhalf_unit": t_unit,
        "cmaxhalf": cmaxhalf,
        "cmaxhalf_unit": c_unit,
        "kel": kel,
        "kel_unit": "1/({})".format(t_unit),
        "thalf": thalf,
        "thalf_unit": t_unit,
        "vd": vd,
        "vd_unit": vd_unit,
        "vdss": vdss,
        "vdss_unit": vd_unit,
        "cl": cl,
        "cl_unit": "({})/({})".format(vd_unit, t_unit),
        "slope": slope,
        "intercept": intercept,
        "r_value": r_value,
        "p_value": p_value,
        "std_err": std_err,
        "max_idx": max_idx,
    }


def _auc(t, c):
    """ Calculates the area under the curve (AUC) via trapezoid rule """
    return np.sum((t[1:] - t[0:-1]) * (c[1:] + c[0:-1]) / 2.0)


def _aucinf(t, c, slope=None, intercept=None):
    """ Calculates the area under the curve (AUC) via trapezoid rule and extrapolated to infinity """

    if (slope is None) or (intercept is None):
        [slope, intercept, r_value, p_value, std_err, max_index] = _regression(t, c)
    auc = _auc(t, c)

    # necessary to calculate the slope at last datapoint via differentiation
    # dy/dt with y(t) = c0 exp(slope*t) and t=0
    # => slope_eff = c0*slope
    # delta_x from last data point to x-axis is via m*x + c = 0
    # delta_x = - c/m
    # area is then 1/2 * c * delta_x
    slope_eff = c[-1] * slope
    auc_d = - 0.5 * c[-1]**2 / slope_eff

    return auc + auc_d


def _max(t, c):
    """ Returns timepoint of maximal value and maximal value based on curve.

    The tmax depends on the value of both the absorption rate constant (ka)
    and the elimination rate constant (kel).

    :return: tuple (tmax, cmax)
    """
    idx = np.nanargmax(c)
    return t[idx], c[idx]


def _max_half(t, c):
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
        return np.nan, np.nan

    cmax = c[idx]

    tnew = t[:idx]
    cnew = np.abs(c[:idx] - 0.5 * cmax)
    idx_half = np.argmin(cnew)

    return tnew[idx_half], c[idx_half]


def _kel(t, c, slope=None):
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
    if slope is None:
        [slope, intercept, r_value, p_value, std_err, max_index] = _regression(t, c)

    return -slope


def _kel_cv(t, c, std_err=None, slope=None):
    if std_err is None or slope is None:
        [slope, intercept, r_value, p_value, std_err, max_index] = _regression(t, c)
    return std_err / slope


def _thalf(t, c, slope=None):
    """ Calculates the half-life using the elimination constant.

    Definition: Time it takes for the plasma concentration or the amount
    of drug in the body to be reduced by 50%.

    Half-life determines the length of the drug effect. It also indicates
    whether accumulation of the drug will occur under a multiple dosage regimen
    and it is essential to decide on the appropriate dosing interval.

    If no kel is provided t and c must be provided for calculation
    of the elimination constant.
    """
    kel = _kel(t, c, slope=slope)
    # np.log is natural logarithm, i.e. ln(2)
    return np.log(2) / kel


def _thalf_cv(t, c, slope=None, std_err=None):
    kel = _kel(t, c, slope=slope)

    return np.log(2) / _kel_cv(t, c, slope=slope, std_err=std_err)


def _vdss(t, c, dose, intercept=None):
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
    if intercept is None:
        [slope, intercept, r_value, p_value, std_err, max_index] = _regression(t, c)
    return dose / np.exp(intercept)


def _vd(t, c, dose):
    """
    Apparent volume of distribution.
    Not a physical space, but a dilution space.

    Volume of distribution is calculated via
        vd = Dose/(AUC_inf*kel)
    """
    # FIXME: refactor everything in class to avoid recalculation of regression
    [slope, intercept, r_value, p_value, std_err, max_index] = _regression(t, c)
    kel = _kel(t, c, slope=slope)
    aucinf = _aucinf(t, c, slope=slope, intercept=intercept)

    return dose / (aucinf*kel)


def _regression(t, c):
    """ Linear regression on the log timecourse after maximal value.
    No check is performed if already in equilibrium distribution !.
    The linear regression is calculated from all data points after the maximum.

    :return:
    """
    # TODO: check for distribution and elimination part of curve.
    max_index = np.argmax(c)
    # at least two data points after maximum are required for a regression
    if max_index > (len(c) - 3):
        return [np.nan] * 6

    # linear regression start regression on datapoint after maximum
    x = t[max_index + 1:]
    y = np.log(c[max_index + 1:])
    # x = t[-4:]
    # y = np.log(c[-4:])

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    if -slope < 0:
        warnings.warn("The regression results in a positive slope, a negative elimination rates follows form that."
                      "This is not allowed. Elimination rate is set to NaN ")
        slope = np.NAN

    return [slope, intercept, r_value, p_value, std_err, max_index]
