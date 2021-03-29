"""Examples for pharmacokinetics calculation.

This examples shows how based on time and concentration vector the
pharmacokinetic parameters can be calculated.
"""
import warnings
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import pint
from matplotlib import pyplot as plt
from pint import Quantity

from pkdb_analysis.pk.pharmacokinetics import TimecoursePK, TimecoursePKNoDosing
from pkdb_analysis.test import TESTDATA_PATH


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
    c = c0 * np.exp(-kel * t)

    tcpk = TimecoursePK(
        time=Q_(t, "hr"), concentration=Q_(c, "nmol/l"), dose=dose, ureg=ureg
    )

    return [tcpk]


def example1() -> List[TimecoursePK]:
    """Create example for pharmacokinetics calculation."""
    results = []
    df = pd.read_csv(
        TESTDATA_PATH / "pk" / "data_example1.csv", sep="\t", na_values="NA"
    )

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
                time=t, concentration=c, substance=substance, dose=dose, ureg=ureg
            )
            results.append(tcpk)

    return results


def example1_NoDosing() -> List[TimecoursePKNoDosing]:
    """Creaete example for pharmacokinetics calculation."""
    results = []
    df = pd.read_csv(
        TESTDATA_PATH / "pk" / "data_example1.csv", sep="\t", na_values="NA"
    )

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
                time=t, concentration=c, substance=substance, ureg=ureg
            )
            results.append(tcpk)

    return results


def example2() -> List[TimecoursePK]:
    """Create example for pharmacokinetics calculation.

    This demonstrates the extreme examples of time courses with only limited data points.
    On caffeine the regressions can be calculated, on paraxanthine this is not possible any more (only a single datapoint
    or one data point after the maximum.
    """
    results = []
    df = pd.read_csv(
        TESTDATA_PATH / "pk" / "data_example2.csv", sep="\t", na_values="NA"
    )

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

        tcpk = TimecoursePK(
            time=t, concentration=c, substance=substance, dose=dose, ureg=ureg
        )

        results.append(tcpk)

    return results


def example_midazolam() -> List[TimecoursePK]:
    """Create example for pharmacokinetics calculation."""
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
        time=t, concentration=c, substance=substance, dose=dose, ureg=ureg
    )
    results.append(tcpk)

    return results


def example_Kim2011_Fig2() -> List[TimecoursePK]:
    """Create example for pharmacokinetics calculation."""
    results = []
    df = pd.read_csv(
        TESTDATA_PATH / "pk" / "Kim2011_Fig2.tsv", sep="\t", na_values="NA"
    )
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
        time=t, concentration=c, substance=substance, dose=dose, ureg=ureg
    )
    results.append(tcpk)

    return results


def example_Divoll1982_Fig1() -> List[TimecoursePK]:
    """Create example for pharmacokinetics calculation."""
    results = []
    df = pd.read_csv(
        TESTDATA_PATH / "pk" / "Divoll1982_Fig1.tsv", sep="\t", na_values="NA"
    )

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
        time=t, concentration=c, substance=substance, dose=dose, ureg=ureg
    )
    results.append(tcpk)

    return results


def example_Lane2014_Fig1() -> List[TimecoursePK]:
    """Create example for pharmacokinetics calculation."""
    results = []
    df = pd.read_csv(
        TESTDATA_PATH / "pk" / "Lane2014_Fig1.tsv", sep="\t", na_values="NA"
    )

    # ------------------------------------------
    # Pharmacokinetic parameter for acetaminophen
    # ------------------------------------------
    # get caffeine data
    dose = Q_(0, "mg")
    substance = "caffeine"

    # calculate pharmacokinetic information
    t = Q_(df.time.values, "hr")
    c = Q_(df["mean"].values, "µg/ml")
    tcpk = TimecoursePK(
        time=t, concentration=c, substance=substance, dose=dose, ureg=ureg
    )
    results.append(tcpk)

    return results


def show_results(results: List[TimecoursePK]):
    """Show given results."""
    for tcpk in results:
        print(tcpk.info())
        _ = tcpk.figure()
        plt.show()


if __name__ == "__main__":
    for f_example in [
        example0,
        example1,
        example1_NoDosing,
        example2,
        example_midazolam,
        example_Kim2011_Fig2,
        example_Divoll1982_Fig1,
        example_Lane2014_Fig1,
    ]:
        res = f_example()
        show_results(res)

    plt.show()
