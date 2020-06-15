"""
This examples shows how based on time and concentration vector the
pharmacokinetic parameters can be calculated.
"""
from typing import List, Dict
import numpy as np
import warnings
import pandas as pd
from pkdb_analysis.pk.pharmacokinetics import TimecoursePK, TimecoursePKNoDosing
from matplotlib import pyplot as plt
from pkdb_analysis.tests import TESTDATA_PATH
from pathlib import Path

import pint
from pint import Quantity
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    Quantity([])

# Define unit registry for examples
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity


def example0() -> List[TimecoursePK]:
    """Calculate pharmacokinetics from simulated data."""
    t = np.linspace(0, 3, num=50)
    kel = 1.0
    c0 = 10.0
    dose = Q_(10.0, "mg") * Q_(1.0, "mole/g")
    c = c0 * np.exp(-kel*t)

    tcpk = TimecoursePK(time=Q_(t, "hr"), concentration=Q_(c, "nmol/l"),
                      dose=dose, ureg=ureg)

    return [tcpk]


def example1() -> List[TimecoursePK]:
    """ Example for pharmacokinetics calculation.

    :return:
    """
    results = []
    df = pd.read_csv(TESTDATA_PATH / "pk" / "data_example1.csv", sep="\t", na_values="NA")

    # ------------------------------------------
    # Pharmacokinetic parameter for caffeine
    # ------------------------------------------
    # get caffeine data
    dose = Q_(100, "mg")
    substance = "caffeine"

    for tissue in df.tissue.unique():
        for group in df.group.unique():
            print("substance: {}, dose: {}".format(substance, dose))
            data = df[(df.tissue == tissue) & (df.group == group)]

            # calculate pharmacokinetic information
            t = Q_(data.time.values, "hr")
            c = Q_(data.caf.values, "mg/l")
            tcpk = TimecoursePK(
                time=t,
                concentration=c,
                substance=substance,
                dose=dose,
                ureg=ureg
            )
            results.append(tcpk)

    return results

def example1_NoDosing() -> List[TimecoursePKNoDosing]:
    """ Example for pharmacokinetics calculation.

    :return:
    """
    results = []
    df = pd.read_csv(TESTDATA_PATH / "pk" / "data_example1.csv", sep="\t", na_values="NA")

    # ------------------------------------------
    # Pharmacokinetic parameter for caffeine
    # ------------------------------------------
    # get caffeine data
    substance = "caffeine"

    for tissue in df.tissue.unique():
        for group in df.group.unique():
            print("substance: {}".format(substance))
            data = df[(df.tissue == tissue) & (df.group == group)]

            # calculate pharmacokinetic information
            t = Q_(data.time.values, "hr")
            c = Q_(data.caf.values, "mg/l")
            tcpk = TimecoursePKNoDosing(
                time=t,
                concentration=c,
                substance=substance,
                ureg=ureg
            )
            results.append(tcpk)

    return results
def example2() -> List[TimecoursePK]:
    """ Example for pharmacokinetics calculation.

    This demonstrates the extreme examples of time courses with only limited data points.
    On caffeine the regressions can be calculated, on paraxanthine this is not possible any more (only a single datapoint
    or one data point after the maximum.

    :return:
    """
    results = []
    df = pd.read_csv(TESTDATA_PATH / "pk" / "data_example2.csv", sep="\t", na_values="NA")

    # ------------------------------------------
    # Pharmacokinetic parameter for caffeine
    # ------------------------------------------
    # get caffeine data
    for (substance, dose_per_kg) in [
        ["caffeine", 2],
        ["caffeine", 4],
        ["paraxanthine", 2],
        ["paraxanthine", 4],
    ]:

        print("substance: {}, dose: {}".format(substance, dose_per_kg))
        data = df[(df.substance == substance) & (df.dose == dose_per_kg)]

        # calculate pharmacokinetic information
        dose_per_kg = Q_(dose_per_kg, "mg/kg")
        bodyweight = Q_(70, "kg")
        dose = dose_per_kg * bodyweight  # [mg]
        t = data.time
        if substance == "caffeine":
            c = data.caf
        elif substance == "paraxanthine":
            c = data.px

        t = Q_(t.values, "hr")
        c = Q_(c.values, "mg/l")

        tcpk = TimecoursePK(time=t, concentration=c, substance=substance,
                            dose=dose, ureg=ureg)

        results.append(tcpk)

    return results



def example_Kim2011_Fig2() -> List[TimecoursePK]:
    """ Example for pharmacokinetics calculation.

    :return:
    """
    results = []
    df = pd.read_csv(TESTDATA_PATH / "pk" / "Kim2011_Fig2.tsv", sep="\t", na_values="NA")
    df = df[(df.interventions == "paracetamol1000mg")]

    # ------------------------------------------
    # Pharmacokinetic parameter for acetaminophen
    # ------------------------------------------
    # get caffeine data
    dose = Q_(100, "mg")
    substance = "acetaminophen"

    # calculate pharmacokinetic information
    t = Q_(df.time.values, "hr")
    c = Q_(df["mean"].values, "µg/ml")
    tcpk = TimecoursePK(
        time=t,
        concentration=c,
        substance=substance,
        dose=dose,
        ureg=ureg
    )
    results.append(tcpk)

    return results


def example_Divoll1982_Fig1() -> List[TimecoursePK]:
    """ Example for pharmacokinetics calculation.

    :return:
    """
    results = []
    df = pd.read_csv(TESTDATA_PATH / "pk" / "Divoll1982_Fig1.tsv", sep="\t", na_values="NA")

    # ------------------------------------------
    # Pharmacokinetic parameter for acetaminophen
    # ------------------------------------------
    # get caffeine data
    dose = Q_(100, "mg")
    substance = "acetaminophen"

    # calculate pharmacokinetic information
    t = Q_(df.time.values, "hr")
    c = Q_(df["apap"].values, "µg/ml")
    tcpk = TimecoursePK(
        time=t,
        concentration=c,
        substance=substance,
        dose=dose,
        ureg=ureg
    )
    results.append(tcpk)

    return results

def example_midazolam() -> List[TimecoursePK]:
    """ Example for pharmacokinetics calculation.

    :return:
    """
    results = []
    df = pd.read_csv(TESTDATA_PATH / "pk" / "midazolam.tsv", sep="\t", na_values="NA")

    # ------------------------------------------
    # Pharmacokinetic parameter for acetaminophen
    # ------------------------------------------
    # get caffeine data
    dose = Q_(7.5, "mg")
    substance = "midazolam"

    # calculate pharmacokinetic information
    t = Q_(df.time.values, "min")
    c = Q_(df["Cve_mid"].values, "mmole/litre")
    tcpk = TimecoursePK(
        time=t,
        concentration=c,
        substance=substance,
        dose=dose,
        ureg=ureg
    )
    results.append(tcpk)

    return results


def show_results(results: List[TimecoursePK]):
    """Show given results."""
    for tcpk in results:
        print(tcpk.info())
        f = tcpk.figure()
        plt.show()


if __name__ == "__main__":
    r0 = example0()
    show_results(r0)

    r1 = example1()
    show_results(r1)

    r1_nd = example1_NoDosing()
    show_results(r1_nd)

    r2 = example2()
    show_results(r2)

    r3 = example_Kim2011_Fig2()
    show_results(r3)

    r4 = example_Divoll1982_Fig1()
    show_results(r4)

    r5 = example_midazolam()
    show_results(r5)

    plt.show()
