import numpy as np
from pkdb_analysis.pk.pharmacokinetics_example import example1, example2
from pkdb_analysis.pk.pharmacokinetics import Q_, PKInference, ureg
from pint import Unit


def test_pharmacokinetics():
    t = np.linspace(0, 100, num=50)
    kel = 1.0
    c0 = 10.0
    dose = Q_(10.0, "mg") * Q_(1.0, "mole/g")
    c = c0 * np.exp(-kel * t)

    pkinf = PKInference(time=Q_(t, "hr"), concentration=Q_(c, "nmol/l"),
                     dose=dose)
    print(pkinf.info())
    pk = pkinf.pk
    assert pk.kel.magnitude == kel
    assert pk.dose == Q_(0.01, "mole")
    assert pk.tmax == Q_(0.0, "hr")
    assert pk.cmax == Q_(10.0, "nmol/l")
    assert pk.vd.units == ureg.Unit("liter")


def test_example1():
    example1()


def test_example2():
    example2()
