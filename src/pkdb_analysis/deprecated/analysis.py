""" Module for analysis of PKData"""
# FIXME: Probably deprecated
import os

import matplotlib.pyplot as plt
import numpy as np
import pint
from matplotlib import ticker
from matplotlib.lines import Line2D
from matplotlib.ticker import FormatStrFormatter


ureg = pint.UnitRegistry()

# ---- Styles for plotting ----

import matplotlib.font_manager as font_manager
import matplotlib.markers as mmarkers


font = font_manager.FontProperties(
    family="Roboto Mono",
    weight="normal",
    style="normal",
    size=16,
)
plt.rcParams.update(
    {
        "axes.labelsize": "20",
        "axes.labelweight": "bold",
        "axes.titlesize": "medium",
        "axes.titleweight": "bold",
        "legend.fontsize": "20",
        "xtick.labelsize": "20",
        "ytick.labelsize": "20",
        "figure.facecolor": "1.00",
    }
)
# ------------------------------


def get_one(d):
    """return only one element if all elements are the same."""
    d = d.dropna()
    assert len(set(d)) <= 1, set(d)
    return list(set(d))[0]


def _str_all(d):
    """String representation of a list."""
    d = d.dropna()
    return ", ".join(set(d))


def mscatter(x, y, ax, m=None, **kw):

    sc = ax.scatter(x, y, **kw)
    if (m is not None) and (len(m) == len(x)):
        paths = []
        for marker in m:
            if isinstance(marker, mmarkers.MarkerStyle):
                marker_obj = marker
            else:
                marker_obj = mmarkers.MarkerStyle(marker)
            path = marker_obj.get_path().transformed(marker_obj.get_transform())
            paths.append(path)
        sc.set_paths(paths)
    return sc


def figure_category(d):
    if d["per_bw"] and d["intervention_per_bw"]:
        return "rel_output_rel_intervention"
    elif d["per_bw"] and not d["intervention_per_bw"]:
        return "rel_output_abs_intervention"
    elif not d["per_bw"] and not d["intervention_per_bw"]:
        return "abs_output_abs_intervention"
    elif not d["per_bw"] and d["intervention_per_bw"]:
        return "abs_output_rel_intervention"


def create_plots(  # FIXME: Probably deprecated
    data,
    fig_path,
    color_by=None,
    color_mapping=None,
    nrows=2,
    ncols=2,
    figsize=(30, 30),
    log_y=False,
    formats=["png", "svg"],
):
    data["plotting_category"] = data[["per_bw", "intervention_per_bw"]].apply(
        figure_category, axis=1
    )
    figure, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    axes_iter = iter(axes.flatten())
    substance = get_one(data.substance)
    substance_intervention = _str_all(data.substance_intervention)
    measurement_type = get_one(data.measurement_type)

    for plotting_category, data_category in data.groupby("plotting_category"):

        unit = get_one(data_category.unit)
        u_unit = ureg(unit)
        unit_intervention = get_one(data_category.unit_intervention)
        u_unit_intervention = ureg(unit_intervention)
        ax = next(axes_iter)

        y_axis_label = f"{substance} {measurement_type}"

        ax.set_ylabel(f"{y_axis_label} [{u_unit.u :~P}]")
        x_label = "$Dose_{" + substance_intervention + "}$"
        ax.set_xlabel(f"{x_label} [{u_unit_intervention.u :~P}]")
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))

        max_values = np.array(
            [
                data_category["value"].max(),
                data_category["mean"].max(),
                data_category["median"].max(),
            ]
        )
        max_values = max_values[~np.isnan(max_values)]
        df_subplot_max = np.max(max_values) * 1.05
        df_figure_x_max = data_category.value_intervention.max() * 1.05
        df_figure_min = 0

        individuals_data = data_category[data_category.group_pk == -1]
        x = individuals_data.value_intervention
        y = individuals_data.value
        color = list(individuals_data.color)
        marker = list(individuals_data.marker)
        mscatter(x, y, ax=ax, color=color, m=marker, label=None, s=20)

        group_data = data_category[data_category.group_pk != -1]

        x_group_max = group_data["value_intervention"].max()
        y_group_max = group_data["mean"].max()
        for group, df_group in group_data.iterrows():
            x_group = df_group["value_intervention"]

            if np.isnan(df_group["mean"]):
                y_group = df_group["median"]

            else:
                y_group = df_group["mean"]
            yerr_group = df_group.se
            ms = df_group.group_count + 5
            color = df_group.color
            marker = df_group.marker

            mfc = color
            if color == (0, 0, 0, 0.7):
                mfc = (0, 0, 0, 0)

            ax.errorbar(
                x_group,
                y_group,
                yerr=yerr_group,
                xerr=0,
                mfc=mfc,
                ecolor=color,
                mec=color,
                fmt=marker,
                ms=ms,
                alpha=0.7,
            )

            txt = df_group["study_name"]

            data_values = [
                x_group + (0.01 * x_group_max),
                y_group + (0.01 * y_group_max),
            ]
            isnan = np.isnan(np.array(data_values))
            if not any(isnan):
                ax.annotate(
                    txt,
                    (x_group + (0.01 * x_group_max), y_group + (0.01 * y_group_max)),
                    alpha=0.7,
                )

            legend_elements = []

        for plotting_type, d in data_category.groupby("plotting_type"):
            individuals_data = d[d.group_pk == -1]
            group_data = d[d.group_pk != -1]

            individuals_number = len(individuals_data)
            group_number = len(group_data)
            total_group_individuals = group_data["group_count"].sum()
            color = get_one(d.color)

            label_text = f"{plotting_type:<10} I: {individuals_number:<3} G: {group_number:<2} TI: {int(total_group_individuals + individuals_number):<3}"
            label = Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label=label_text,
                markerfacecolor=color,
                markersize=10,
            )
            legend_elements.append(label)

        legend2_elements = [
            Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                label="PK DATA",
                markerfacecolor="black",
                markersize=10,
            ),
            Line2D(
                [0],
                [0],
                marker="s",
                color="w",
                label="PK FROM TIME COURSE",
                markerfacecolor="black",
                markersize=10,
            ),
            Line2D(
                [0],
                [0],
                marker="v",
                color="w",
                label="PK FROM BODY WEIGHT",
                markerfacecolor="black",
                markersize=10,
            ),
        ]

        legend3_elements = [
            Line2D(
                [0],
                [10],
                marker="o",
                color="w",
                label="1",
                markerfacecolor="black",
                markersize=5 + 1,
            ),
            Line2D(
                [0],
                [20],
                marker="o",
                color="w",
                label="10",
                markerfacecolor="black",
                markersize=5 + 10,
            ),
            Line2D(
                [0],
                [50],
                marker="o",
                color="w",
                label="30",
                markerfacecolor="black",
                markersize=5 + 30,
            ),
        ]

        ax.set_title(f"{plotting_category}")
        ax.set_xlim(left=0, right=df_figure_x_max)
        # ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))

        leg1 = ax.legend(handles=legend_elements, prop=font, loc="upper right")
        leg2 = ax.legend(handles=legend2_elements, prop=font, loc="upper left")
        leg3 = ax.legend(
            handles=legend3_elements, prop=font, labelspacing=1.3, loc="center right"
        )
        leg3.set_title(title="GROUP SIZE", prop=font)
        ax.add_artist(leg2)
        ax.add_artist(leg1)

        if log_y:
            ax.set_yscale("log")
            ax.set_ylim(bottom=df_figure_min, top=df_subplot_max)
        else:
            ax.set_ylim(bottom=0, top=df_subplot_max)
    for format in formats:
        figure.savefig(
            os.path.join(fig_path, f"{measurement_type}.{format}"),
            bbox_inches="tight",
            dpi=72,
            format=format,
        )
    # figure.savefig(os.path.join(fig_path, f"{measurement_type}.png"), bbox_inches="tight", dpi=72)
