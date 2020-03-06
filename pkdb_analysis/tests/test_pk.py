import numpy as np
from pkdb_analysis.pk.pharmacokinetics_example import example0, example1, example2, show_results
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
    assert pk.kel.magnitude == kel
    assert pk.dose == Q_(0.01, "mole")
    assert pk.tmax == Q_(0.0, "hr")
    assert pk.cmax == Q_(10.0, "nmol/l")
    assert pk.vd.units == ureg.Unit("liter")


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


def test_example2():
    results = example2()
    show_results(results)
