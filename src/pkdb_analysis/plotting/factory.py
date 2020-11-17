"""
Module for static plot creation.
"""
import logging
import pandas as pd
from typing import List, Set, Dict, Callable, Tuple
from pathlib import Path
import numpy as np

import warnings

from pkdb_analysis.filter import f_dosing_in, f_mt_in_substance_in
from pkdb_analysis.deprecated.analysis import mscatter, get_one
from pkdb_analysis.data import PKData
from pkdb_analysis.meta_analysis import MetaAnalysis

# ---- Styles for plotting ----
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FormatStrFormatter
import matplotlib.font_manager as font_manager
from matplotlib import ticker
from pkdb_analysis.units import UnitRegistry
from pkdb_analysis.core import Sid
logger = logging.getLogger(__file__)

# FIXME: get rid of global module definitions! This overwrites local settings on import!
ureg = UnitRegistry()

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

# FIXME:


class PlotContentDefinition:
    """Defines all settings for a given output plot. """
    def __init__(
        self,
        sid: Sid = None,
        units_to_remove: List[str] = None,
        infer_by_intervention: bool = True,
        infer_by_output: bool = True,
    ):

        if units_to_remove is None:
            units_to_remove = list()

        self.key = str(sid.sid) if sid else None
        self.sid = sid
        self.units_rm = units_to_remove
        self.infer_by_intervention = infer_by_intervention
        self.infer_by_output = infer_by_output

    @property
    def measurement_types(self):
        return [self.sid.sid]


class PlotContentDefinitionMulti(PlotContentDefinition):
    """Defines all settings for a given output plot with multiple measurement types plotted together on the y axis."""

    def __init__(
        self,
        sids: List[Sid],
        units_to_remove: List[str] = None,
        infer_by_intervention: bool = True,
        infer_by_output: bool = True,
    ):
        super().__init__(
            sid=None,
            units_to_remove=units_to_remove,
            infer_by_intervention=infer_by_intervention,
            infer_by_output=infer_by_output
        )
        self.sids = sids
        self.key = self._joined_measurement_type()

    @property
    def measurement_types(self):
        return [sid.sid for sid in self.sids]

    def _joined_measurement_type(self):
        return "_".join(self.measurement_types)


def results(
    data_dict: Dict[PlotContentDefinition, PKData],
    intervention_substances: Set[str],
    additional_information: Dict[str, Callable],
    url: str,
    replacements: Dict[str, Dict[str, str]]
) -> Dict[PlotContentDefinition, pd.DataFrame]:
    """ Creates single dataframes from a pkdata instances and infers additional results from body weight. """

    results_dict = {}
    for plot_content, pkd in data_dict.items():
        meta_analysis = MetaAnalysis(pkd, intervention_substances, url)
        meta_analysis.create_results()

        for key, additional_function in additional_information.items():
            meta_analysis.results[key] = meta_analysis.results.apply(
                additional_function, axis=1
            )
        meta_analysis.infer_from_body_weight(
            by_intervention=plot_content.infer_by_intervention, by_output=plot_content.infer_by_output
        )
        meta_analysis.add_extra_info(replacements)
        results_dict[plot_content] = meta_analysis.results

    return results_dict


def add_legends(df: pd.DataFrame, color_label: str, color_by: str,  ax: plt.Axes):
    """ Adds legends to axis"""
    legend_elements = []
    for plotting_type, d in df.groupby(color_label):
        individuals_data = d[d.group_pk == -1]
        group_data = d[d.group_pk != -1]
        individuals_number = len(individuals_data)
        group_number = len(group_data)
        total_group_individuals = group_data["group_count"].sum()
        color = get_one(d[color_by])

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

    leg1 = ax.legend(handles=legend_elements, prop=font, loc="upper right")
    leg2 = ax.legend(handles=legend2_elements, prop=font, loc="upper left")
    leg3 = ax.legend(
        handles=legend3_elements, prop=font, labelspacing=1.3, loc="center right"
    )
    leg3.set_title(title="GROUP SIZE", prop=font)
    ax.add_artist(leg2)
    ax.add_artist(leg1)


def group_values(df_group: pd.DataFrame,
                 color_by: str) -> (pd.Series, pd.Series, pd.Series, pd.Series, pd.Series, pd.Series):
    """ Returns the values for plotting of group data"""
    x_group = df_group["intervention_value"]

    if np.isnan(df_group["mean"]):
        y_group = df_group["median"]
    else:
        y_group = df_group["mean"]

    yerr_group = df_group.se
    yerr_group = np.nan_to_num(yerr_group)
    ms = df_group.group_count + 5
    color = df_group[color_by]
    marker = df_group.marker
    return x_group, y_group, yerr_group, ms, color, marker


def add_group_scatter(df_group: pd.DataFrame, color_by: str, ax: plt.Axes) -> None:
    """ Adds scatter plots of outputs related to groups. """
    x_group, y_group, yerr_group, ms, color, marker = group_values(df_group, color_by)
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


def add_text(
        df_group: pd.DataFrame,
        df_figure_x_max: float,
        df_figure_y_max: float,
        color_by: str,
        ax: plt.Axes) -> None:
    """ Annotates every scatter point related to a group with the respective study name."""
    x_group, y_group, _, _, _, _ = group_values(df_group, color_by=color_by)
    txt = df_group.study_name
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


def add_axis_config(ax: plt.Axes,
                    substance: str,
                    substance_intervention: str,
                    measurement_type: str,
                    u_unit,
                    u_unit_intervention,
                    df_figure_x_max: float,
                    df_figure_y_min: float,
                    df_figure_y_max: float,
                    log_y: bool
                    ) -> None:
    y_axis_label = f"{substance} {measurement_type}"
    ax.set_ylabel(f"{y_axis_label} [{u_unit.u :~P}]")
    x_label = "$Dose_{" + substance_intervention + "}$"
    ax.set_xlabel(f"{x_label} [{u_unit_intervention.u :~P}]")
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    ax.set_xlim(left=0, right=df_figure_x_max)
    # ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))

    if log_y:
        ax.set_yscale("log")
        ax.set_ylim(bottom=df_figure_y_min, top=df_figure_y_max)
    else:
        ax.set_ylim(bottom=0, top=df_figure_y_max)


def create_plot(df: pd.DataFrame,
                file_name: Path,
                color_by: str,
                color_label: str,
                figsize: Tuple[int, int] = (15, 15),
                log_y: bool = False) -> None:
    """ Creates a single plot from the dataframe created by MetaAnalysis.create_results()"""

    measurement_type = df["measurement_type"].unique()[0]
    substance = df["substance"].unique()[0]  # fixme: multiple substances are possible.
    substance_intervention = df["intervention_substance"].unique()[0]  # fixme: multiple substances are possible.
    u_unit = ureg(get_one(df["unit"]))
    u_unit_intervention = ureg(get_one(df["intervention_unit"]))

    figure, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
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
    rows_with_nan = individuals_data[["intervention_value", "value"]].isnull().any(axis=1)
    nan_individuals_data = individuals_data[rows_with_nan]
    if len(nan_individuals_data) > 0:
        for row, output in nan_individuals_data.iterrows():
            warnings.warn(f"individual: <{output['individual_name']}> in study <{output['study_name']}> is has a nan value "
                          f"on intervention <{output['intervention_value']}> or output <{output['value']}>,"
                          f" which will not be displayed.")

    individuals_data = individuals_data[~rows_with_nan]
    x = individuals_data.intervention_value
    y = individuals_data.value

    color = list(individuals_data[color_by])
    marker = list(individuals_data["marker"])
    mscatter(list(x), list(y), ax=ax, color=color, m=marker, alpha=0.7, label=None, s=20)

    for group, df_group in group_data.iterrows():
        add_group_scatter(df_group, color_by, ax)
        add_text(df_group, df_figure_x_max, df_figure_y_max, color_by, ax)

    add_legends(df, color_label, color_by, ax)
    add_axis_config(ax,
                    substance,
                    substance_intervention,
                    measurement_type,
                    u_unit,
                    u_unit_intervention,
                    df_figure_x_max,
                    df_figure_y_min,
                    df_figure_y_max,
                    log_y)

    figure.savefig(
        file_name,
        bbox_inches="tight",
        dpi=72,
        format="png",
    )


def create_plots(results_dict, path, color_by, color_label) -> None:
    """Creates multiple static plots."""
    for plot_content, result_infer in results_dict.items():
        for group, df in result_infer.groupby("unit_category"):
            file_name = path / f"{plot_content.key}_{group}.png"
            create_plot(df, file_name, color_by, color_label)


def plot_factory(
    pkdata: PKData,
    plotting_categories: List[PlotContentDefinition],
    intervention_substances: Set[Sid],
    output_substances: Set[Sid],
    exclude_study_names: Set[str],
    additional_information: Dict[str, Callable],
    path: Path,
    color_by: str,
    color_label: str,
    replacements: Dict[str,Dict[str, str]] = {},
) -> None:
    """ Factory function to create multiple plots defined by each entry of the plotting_categories."""
    intervention_substances_str = {substance.sid for substance in intervention_substances}
    output_substances_str = {substance.sid for substance in output_substances}

    data_dict = pkdata_by_plot_content(
        pkdata,
        plotting_categories,
        intervention_substances_str,
        output_substances_str,
        exclude_study_names,
    )

    results_dict = results(
        data_dict=data_dict,
        intervention_substances=intervention_substances_str,
        additional_information=additional_information,
        url=None,
        replacements=replacements,
    )

    create_plots(
        results_dict,
        path=path,
        color_by=color_by,
        color_label=color_label
    )


def pkdata_by_plot_content(
    pkdata: PKData,
    plotting_categories: List[PlotContentDefinition],
    intervention_substances: Set[str],
    output_substances: Set[str],
    exclude_study_names: Set[str],
) -> Dict[PlotContentDefinition, PKData]:
    """Splits the PKData instance in a dictonary with each entry related to one PlotContentDefinition."""
    # filter pkdata for given attributes
    data_dict = {}
    for plotting_category in plotting_categories:

        data = pkdata.filter_intervention(
            f_dosing_in, substances=intervention_substances
        ).filter_output(
            f_mt_in_substance_in,
            measurement_types=plotting_category.measurement_types,
            substances=output_substances,
        )
        data = data.exclude_output(lambda d: d["unit"].isin(plotting_category.units_rm))
        data = data.exclude_intervention(
            lambda d: d["study_name"].isin(exclude_study_names)
        )

        data.outputs["measurement_type"] = plotting_category.key
        data_dict[plotting_category] = data.copy()

    return data_dict



