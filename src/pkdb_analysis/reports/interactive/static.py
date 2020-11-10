import pint
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from matplotlib.ticker import FormatStrFormatter
from pkdb_analysis.analysis import mscatter, _get_one
from pkdb_analysis.meta_analysis import MetaAnalysis
from pkdb_analysis.reports.interactive.interactive import pkdata_by_measurement_type, _get_pc

# ---- Styles for plotting ----

import matplotlib.font_manager as font_manager
from matplotlib import ticker

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

ureg = pint.UnitRegistry()

def results(
    data_dict,
    intervention_substances,
    additional_information,
    plotting_categories,
    replacements,
):
    # creates one dataframe from PKData instance.
    # infers additional results from body weights.
    results_dict = {}
    for measurement_type, pkd in data_dict.items():
        meta_analysis = MetaAnalysis(pkd, intervention_substances, "")
        meta_analysis.create_results()

        for key, additional_function in additional_information.items():
            meta_analysis.results[key] = meta_analysis.results.apply(
                additional_function, axis=1
            )
        pc = _get_pc(measurement_type, plotting_categories)
        meta_analysis.infer_from_body_weight(
            by_intervention=pc.infer_by_intervention, by_output=pc.infer_by_output
        )
        meta_analysis.add_extra_info(replacements)
        results = meta_analysis.results
        results_dict[measurement_type] = results
    return results_dict

def create_plot(df,
                file_name,
                color_by,
                color_label,
                figsize=(30, 30),
                log_y=False):

    measurement_type = df["measurement_type"].unique()[0]
    u_unit = ureg(df["unit"].unique()[0])
    u_unit_intervention = ureg(df["intervention_unit"].unique()[0])
    substance = df["substance"].unique()[0]
    substance_intervention = df["intervention_substance"].unique()[0]

    y_axis_label = f"{substance} {measurement_type}"
    figure, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    ax.set_ylabel(f"{y_axis_label} [{u_unit.u :~P}]")
    x_label = "$Dose_{" + substance_intervention + "}$"
    ax.set_xlabel(f"{x_label} [{u_unit_intervention.u :~P}]")
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    individuals_data = df[df.group_pk == -1]
    group_data = df[df.group_pk != -1]

    max_values = np.array(
        [
            df["value"].max(),
            df["mean"].max(),
            df["median"].max(),
        ]
    )
    max_values = max_values[~np.isnan(max_values)]
    df_figure_y_max = np.max(max_values) * 1.05
    df_figure_x_max = df.intervention_value.max() * 1.05
    df_figure_y_min = 0

    x = individuals_data.intervention_value
    y = individuals_data.value
    color = list(individuals_data[color_by])
    marker = list(individuals_data["marker"])
    mscatter(x, y, ax=ax, color=color, m=marker, alpha=0.7, label=None, s=20)

    for group, df_group in group_data.iterrows():
        x_group = df_group["intervention_value"]

        if np.isnan(df_group["mean"]):
            y_group = df_group["median"]

        else:
            y_group = df_group["mean"]
        yerr_group = df_group.se
        ms = df_group.group_count + 5
        color = df_group.color
        marker = df_group.marker

        ax.errorbar(
            x_group,
            y_group,
            yerr=yerr_group,
            xerr=0,
            color=color,
            fmt=marker,
            ms=ms,
            alpha=0.7,
        )

        txt = df_group["study_name"]

        data_values = [
            x_group + (0.01 * df_figure_x_max),
            y_group + (0.01 * df_figure_y_max),
        ]
        isnan = np.isnan(np.array(data_values))
        if not any(isnan):
            ax.annotate(
                txt,
                (x_group + (0.01 * df_figure_x_max), y_group + (0.01 * df_figure_y_max)),
                alpha=0.7,
            )
    legend_elements = []
    for plotting_type, d in df.groupby(color_label):
        individuals_data = d[d.group_pk == -1]
        group_data = d[d.group_pk != -1]
        individuals_number = len(individuals_data)
        group_number = len(group_data)
        total_group_individuals = group_data["group_count"].sum()
        color = _get_one(d.color)

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
        ax.set_ylim(bottom=df_figure_y_min, top=df_figure_y_max)
    else:
        ax.set_ylim(bottom=0, top=df_figure_y_max)

    figure.savefig(
        file_name,
        bbox_inches="tight",
        dpi=72,
        format="png",
    )

def create_plots(
        results_dict, path, color_by, color_label):
    for measurement_type, result_infer in results_dict.items():
        for group, df in result_infer.groupby("unit_category"):
            file_name = path / f"{measurement_type}_{group}.png"
            create_plot(df, file_name, color_by, color_label)


def plot_factory(
    pkdata,
    plotting_categories,
    intervention_substances,
    output_substances,
    exclude_study_names,
    additional_information,
    path,
    color_by,
    color_label,
    replacements={},):

    data_dict = pkdata_by_measurement_type(
        pkdata,
        plotting_categories,
        intervention_substances,
        output_substances,
        exclude_study_names,
    )
    results_dict = results(
        data_dict=data_dict,
        intervention_substances=intervention_substances,
        additional_information=additional_information,
        plotting_categories=plotting_categories,
        replacements=replacements,
    )

    create_plots(
        results_dict,
        path,
        color_by,
        color_label)


