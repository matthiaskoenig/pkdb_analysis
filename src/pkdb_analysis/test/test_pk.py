import pytest
import numpy as np
from pkdb_analysis.pk.pharmacokinetics_example import example0, example1, example2, \
    example_Kim2011_Fig2, example_Divoll1982_Fig1, show_results, example_midazolam, example1_NoDosing
from pkdb_analysis.pk.pharmacokinetics import TimecoursePK
from pint import UnitRegistry
from matplotlib import pyplot as plt


def test_pharmacokinetics():
    ureg = UnitRegistry()
    Q_ = ureg.Quantity
    t = np.linspace(0, 100, num=50)
    kel = 1.0
    c0 = 10.0
    dose = Q_(10.0, "mg") * Q_(1.0, "mole/g")
    c = c0 * np.exp(-kel * t)

    tcpk = TimecoursePK(time=Q_(t, "hr"), concentration=Q_(c, "nmol/l"),
                         dose=dose, ureg=ureg)
    pk = tcpk.pk
    assert pytest.approx(pk.kel.magnitude, kel)
    assert pk.dose == Q_(0.01, "mole")
    assert pk.tmax == Q_(0.0, "hr")
    assert pk.cmax == Q_(10.0, "nmol/l")
    assert pk.vd.units == ureg.Unit("liter")


def test_pharmacokinetics_small_values():
    """Test pharmacokinetics with very small values.

    This results of replacement of the values with NaN.
    This also tests the NaN regression.
    """
    ureg = UnitRegistry()
    Q_ = ureg.Quantity
    t = np.linspace(0, 100, num=50)
    kel = 1.0
    c0 = 10.0
    dose = Q_(10.0, "mg") * Q_(1.0, "mole/g")
    c = c0 * np.exp(-kel * t)

    tcpk = TimecoursePK(time=Q_(t, "hr"), concentration=Q_(c, "nmol/l"),
                        dose=dose, ureg=ureg)
    pk = tcpk.pk
    assert pytest.approx(pk.kel.magnitude, kel)
    assert pk.dose == Q_(0.01, "mole")
    assert pk.tmax == Q_(0.0, "hr")
    assert pk.cmax == Q_(10.0, "nmol/l")
    assert pk.vd.units == ureg.Unit("liter")


def test_mg_per_kg_units():
    # failing due to pint bug: https://github.com/hgrecco/pint/issues/1058
    # (required to go to base units first)
    ureg = UnitRegistry()
    Q_ = ureg.Quantity
    dose = Q_(10.0, "mg/kg") * Q_(1.0, "mole/g")
    print(dose)
    dose = dose.to_base_units().to_reduced_units()
    print(dose)


def test_pharmacokinetics_per_bodyweight():
    ureg = UnitRegistry()
    Q_ = ureg.Quantity
    t = np.linspace(0, 100, num=50)
    kel = 1.0
    c0 = 10.0
    dose = Q_(10.0, "mg/kg") * Q_(1.0, "mole/g")
    dose.ito("mmole/kg")  # do a hard conversion to avoid problems with units
    c = c0 * np.exp(-kel * t)

    tcpk = TimecoursePK(time=Q_(t, "hr"), concentration=Q_(c, "nmol/l"),
                        dose=dose, ureg=ureg)
    pk = tcpk.pk
    assert pk.kel.magnitude == pytest.approx(kel)
    assert pk.dose == Q_(0.01, "mole/kg")
    assert pk.tmax == Q_(0.0, "hr")
    assert pk.cmax == Q_(10.0, "nmol/l")
    assert pk.vd.units == ureg.Unit("liter/kg")

def test_pharmacokinetics_shifted_intervention():
    ureg = UnitRegistry()
    Q_ = ureg.Quantity
    t = np.linspace(0, 100, num=50)
    kel = 1.0
    c0 = 10.0
    c = c0 * np.exp(-kel * t)
    time_shift = 10
    t = t + time_shift
    intervention_time = Q_(time_shift, "hr")
    dose = Q_(10.0, "mg") * Q_(1.0, "mole/g")

    tcpk = TimecoursePK(time=Q_(t, "hr"), concentration=Q_(c, "nmol/l"),
                        dose=dose, ureg=ureg,
                        intervention_time=intervention_time)
    pk = tcpk.pk
    assert pk.kel.magnitude == pytest.approx(kel)
    assert pk.dose == Q_(0.01, "mole")
    assert pk.tmax == Q_(0.0, "hr")
    assert pk.cmax == Q_(10.0, "nmol/l")
    assert pk.vd.units == ureg.Unit("liter")


def test_pharmacokinetics_per_bodyweight2():
    ureg = UnitRegistry()
    Q_ = ureg.Quantity
    t = np.linspace(0, 100, num=50)
    kel = 1.0
    c0 = 10.0
    dose = Q_(10.0, "mg/kg")
    c = c0 * np.exp(-kel * t)

    tcpk = TimecoursePK(time=Q_(t, "hr"), concentration=Q_(c, "nmol/l"),
                        dose=dose, ureg=ureg)
    pk = tcpk.pk
    assert pytest.approx(pk.kel.magnitude, kel)
    assert pk.dose == Q_(10.0, "mg/kg")
    assert pk.tmax == Q_(0.0, "hr")
    assert pk.cmax == Q_(10.0, "nmol/l")
    # assert pk.vd.units == ureg.Unit("liter/kg")


def test_example0():
    results = example0()
    tcpk = results[0]
    tcpk.figure()
    plt.show()

    pk = tcpk.pk
    assert pk.kel.magnitude == 1.0
    assert pk.dose == tcpk.Q_(0.01, "mole")
    assert pk.tmax == tcpk.Q_(0.0, "hr")
    assert pk.cmax == tcpk.Q_(10.0, "nmol/l")
    assert pk.vd.units == tcpk.ureg.Unit("liter")
    show_results(results)


def test_example1():
    results = example1()
    tcpk = results[0]

    pk = tcpk.pk
    assert pk.dose == tcpk.Q_(100, "mg")
    assert pk.tmax == tcpk.Q_(1.0, "hr")
    assert pk.tmaxhalf == tcpk.Q_(0.5, "hr")

    assert pk.cmax.units == tcpk.ureg.Unit("mg/l")
    assert pk.vd.units == tcpk.ureg.Unit("liter")
    show_results(results)


def test_example1_NoDosing():
    results = example1_NoDosing()
    tcpk = results[0]

    pk = tcpk.pk
    assert not hasattr(pk, "dose")
    assert not hasattr(pk, "vd")
    assert not hasattr(pk, "vdss")
    assert pk.tmax == tcpk.Q_(1.0, "hr")
    assert pk.tmaxhalf == tcpk.Q_(0.5, "hr")
    assert pk.cmax.units == tcpk.ureg.Unit("mg/l")
    show_results(results)


def test_example2():
    results = example2()
    show_results(results)


def test_example_Kim2011_Fig2():
    results = example_Kim2011_Fig2()
    show_results(results)


def test_example_Divoll1982_Fig1():
    results = example_Divoll1982_Fig1()
    pk = results[0].pk
    assert np.isnan(pk.cmaxhalf.magnitude)
    assert np.isnan(pk.tmaxhalf.magnitude)

    show_results(results)


def test_example_midazolam():
    results = example_midazolam()
    pk = results[0].pk
    print(pk)
    assert not np.isnan(pk.auc.magnitude)
    assert not np.isnan(pk.aucinf.magnitude)
    assert not np.isnan(pk.vd.magnitude)