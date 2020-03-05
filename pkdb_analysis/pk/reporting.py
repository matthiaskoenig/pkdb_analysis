"""
Plotting and reporting of pharmacokinetics.
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import Figure

def pk_report(pk):
    """ Print report for given pharmacokinetic information.

    :param pk: set of pharamacokinetic parameters returned by f_pk.
    :param t_unit:
    :param dose_unit:
    :param c_unit:
    :param vd_unit:
    :param vdbw_unit:
    :return:
    """
    lines = []
    lines.append("-" * 80)
    lines.append(pk["compound"])
    lines.append("-" * 80)
    for key in ["slope", "intercept", "r_value", "p_value", "std_err"]:
        lines.append("{:<12}: {:>3.3f}".format(key, pk[key]))
    lines.append("-" * 80)
    for key in [
        "dose",
        "bodyweight",
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
        pk_key = pd.to_numeric(pk[key])
        lines.append(
            "\t{:<12}: {:>3.3f} [{}]".format(key, pk_key, pk["{}_unit".format(key)])
        )

    lines.append("")
    for key in ["dose", "auc", "aucinf", "kel", "vd", "vdss", "cl"]:
        key_bw = "{}/bw".format(key)
        pk_key = pd.to_numeric(pk[key])

        lines.append(
            "\t{:<12}: {:>3.3f} [{}/{}]".format(
                key_bw,
                1.0 * pk_key / pd.to_numeric(pk["bodyweight"]),
                pk["{}_unit".format(key)],
                pk["bodyweight_unit"],
            )
        )

    return "\n".join(lines)


def pk_figure(t, c, pk) -> Figure:
    """ Create figure from time course and pharmacokinetic parameters.

    :param t: time vector
    :param c: concentration vector
    :param pk: set of pharmacokinetic parameters returned by f_pk.

    :return: matplotlib figure instance
    """
    c_unit = pk["cmax_unit"]
    t_unit = pk["tmax_unit"]
    slope = pk["slope"]
    intercept = pk["intercept"]
    max_idx = pk["max_idx"]
    if max_idx is None or np.isnan(max_idx):
        max_idx = c.size - 1

    kwargs = {"markersize": 10}

    # create figure
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=80)
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
