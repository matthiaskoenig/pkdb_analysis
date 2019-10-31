""" Module for analysis of PKData"""
import os
from collections import namedtuple

import matplotlib.pyplot as plt
import pandas as pd
import pint
from matplotlib import ticker
from matplotlib.lines import Line2D
from matplotlib.ticker import FormatStrFormatter
import numpy as np

from pkdb_analysis import PKData

ureg = pint.UnitRegistry()

# ---- Styles for plotting ----

import matplotlib.font_manager as font_manager

font = font_manager.FontProperties(family='Roboto Mono',
                                   weight='normal',
                                   style='normal', size=16, )
plt.rcParams.update({
    'axes.labelsize': '20',
    'axes.labelweight': 'bold',
    'axes.titlesize': 'medium',
    'axes.titleweight': 'bold',
    'legend.fontsize': '20',
    'xtick.labelsize': '20',
    'ytick.labelsize': '20',
    'figure.facecolor': '1.00'
})
# ------------------------------


class FigureTemplate(object):
    def __init__(self, pk_data, intervention_type, output_type):
        self.pk_data = pk_data
        self.intervention_type = intervention_type
        self.output_type = output_type
        self.figure = False,
        self.ax = False


    def create_figure(self):
        if len(self.pk_data) > 0:
            self.figure, self.ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))


PlotCategory = namedtuple('PlotCategory', ['name', 'color', 'marker', 'pk_data'])


def create_figures(pk_data: PKData):

    def rel(d):
        RELATIVE_SUFFIX = "/ kilogram"
        return d["unit"].str.endswith(RELATIVE_SUFFIX)

    int_abs_out_abs = pk_data.exclude_intervention(rel).exclude_output(rel)

    int_rel_out_abs = pk_data.filter_intervention(rel).exclude_output(rel)
    int_abs_out_rel = pk_data.exclude_intervention(rel).filter_output(rel)

    int_rel_out_rel = pk_data.filter_intervention(rel).filter_output(rel)

    figure_templates = [
        FigureTemplate(
        pk_data=int_abs_out_abs,
        intervention_type="abs",
        output_type="abs"
        ),
        FigureTemplate(
            pk_data=int_rel_out_abs,
            intervention_type="rel",
            output_type="abs"
        ),
        FigureTemplate(
            pk_data=int_abs_out_rel,
            intervention_type="abs",
            output_type="rel"
        ),
        FigureTemplate(
            pk_data=int_rel_out_rel,
            intervention_type="rel",
            output_type="rel"
        )
    ]
    figure, axes = plt.subplots(nrows=2, ncols=2, figsize=(30, 30))

    for n, figure_template in enumerate(figure_templates):
        figure_template.figure = figure
        figure_template.ax = axes.flatten()[n]
    return figure_templates

def create_plots(df_data, categories, fig_path, log_y=False):
    figures = create_figures(df_data)
    for figure in figures:
        if figure.ax:

            max_values = np.array([figure.pk_data.outputs["value"].max(), figure.pk_data.outputs["mean"].max()])
            max_values = max_values[~np.isnan(max_values)]
            df_figure_max = np.max(max_values) * 1.05

            df_figure_x_max = figure.pk_data.interventions.value.max() * 1.05
            df_figure_min = 0  # min([df_figure["value"].min(), df_figure["mean"].min()]) / 1.05

            individuals_data =  figure.pk_data.delete_groups()
            group_data = figure.pk_data.delete_individuals()


            legend_elements = []
            for plot_category in categories:

                individual_intersect = individuals_data.individuals.pks.intersection(plot_category.pk_data.individuals.pks)
                category_data = individuals_data.filter_individual(lambda d: d["individual_pk"].isin(individual_intersect))


                units_intervention = category_data.interventions.unit.unique()
                units = category_data.outputs.unit.unique()


                assert len(units) <= 1, units
                try:
                    unit = units[0]
                    u_unit = ureg(unit)
                    unit_intervention = units_intervention[0]
                    u_unit_intervention = ureg(unit_intervention)

                    intervention_substance = category_data.interventions.substance.unique()[0]
                    output_substance = category_data.outputs.substance.unique()[0]
                    measurement_type = category_data.outputs.measurement_type.unique()[0]

                    y_axis_label = f"{output_substance} {measurement_type}"

                    figure.ax.set_ylabel(f'{y_axis_label} [{u_unit.u :~P}]')
                    x_label = '$Dose_{'+intervention_substance+'}$'
                    figure.ax.set_xlabel(f'{x_label} [{u_unit_intervention.u :~P}]')
                    figure.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

                except IndexError:
                    pass

                individuals_number = category_data.individuals.pk_len

                df_merged = pd.merge(category_data.interventions.df, category_data.outputs.df, on="intervention_pk",
                                     how="inner",
                                     suffixes=('_intervention', '_outputs'))

                for calculated, df_individuals in df_merged.groupby(["calculated"]):
                    #if df_row["inferred"]:
                    #    marker = "v"

                    if calculated:
                        marker = "s"
                    else:
                        marker = plot_category.marker



                    #y = df_individuals.

                    x = df_individuals.value_intervention
                    y = df_individuals.value_outputs


                    figure.ax.scatter(x, y, color=plot_category.color, marker=marker, alpha=0.7, label=None, s=20)

                group_intersect = group_data.groups.pks.intersection(plot_category.pk_data.groups.pks)
                category_data = group_data.filter_group(lambda d: d["group_pk"].isin(group_intersect))

                group_number = category_data.groups.pk_len
                total_group_individuals = 0
                x_group_max = category_data.interventions.value.max()
                y_group_max = category_data.outputs["mean"].max()

                df_merged = pd.merge(category_data.interventions.df, category_data.outputs.df, on="intervention_pk",
                                     how="inner",
                                     suffixes=('_intervention', '_outputs'))

                df_merged = pd.merge(df_merged, category_data.groups.df, on="group_pk",
                                    how="inner",
                                    suffixes=('', '_groups'))
                for i, df_row in df_merged.drop_duplicates(subset="output_pk").iterrows():
                    #if df_row["inferred"]:
                    #    marker = "v"

                    if df_row["calculated"]:

                        marker = "s"
                    else:
                        marker = plot_category.marker

                    x_group = df_row.value_intervention
                    y_group = df_row.mean_outputs

                    #x_group = df_row["value_intervention"]
                    #y_group = df_row["mean"]

                    #if figure.output_type == "rel":
                    #    xerr_group = (df_row[("weight", "sd")] / df_row[("weight", "mean")]) * x_group
                    #else:
                    #    xerr_group = 0
                    yerr_group = df_row.se_outputs
                    group_count = df_row.group_count
                    total_group_individuals += group_count

                    figure.ax.errorbar(x_group, y_group, yerr=yerr_group, xerr=0, color=plot_category.color,
                                       fmt=marker, ms=group_count + 5, alpha=0.7)
                    # for i, txt in enumerate(df_category[('study', '')]):
                    txt = df_row["study_name_intervention"]
                    figure.ax.annotate(txt, (x_group + (0.01 * x_group_max),
                                             y_group + (0.01 * y_group_max)), alpha=0.7)
                

                label_text = f"{plot_category.name:<10} I: {individuals_number:<3} G: {group_number:<2} TI: {int(total_group_individuals + individuals_number):<3}"
                # "
                label = Line2D([0], [0], marker='o', color='w', label=label_text, markerfacecolor=plot_category.color,
                               markersize=10)
                legend_elements.append(label)

            legend2_elements = [
                Line2D([0], [0], marker='o', color='w', label="PK DATA", markerfacecolor="black", markersize=10),
                Line2D([0], [0], marker='s', color='w', label="PK FROM TIME COURSE", markerfacecolor="black",
                       markersize=10),
                Line2D([0], [0], marker='v', color='w', label="PK FROM BODY WEIGHT", markerfacecolor="black",
                       markersize=10)

            ]

            legend3_elements = [
                Line2D([0], [10], marker='o', color='w', label="1", markerfacecolor="black", markersize=5 + 1),
                Line2D([0], [20], marker='o', color='w', label="10", markerfacecolor="black", markersize=5 + 10),
                Line2D([0], [50], marker='o', color='w', label="30", markerfacecolor="black", markersize=5 + 30),
            ]

            figure.ax.set_title(f"{figure.output_type}-vs-dosing_{figure.intervention_type}")
            figure.ax.set_xlim(left=0, right=df_figure_x_max)
            # figure.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            figure.ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))

            leg1 = figure.ax.legend(handles=legend_elements, prop=font, loc="upper right")

            leg2 = figure.ax.legend(handles=legend2_elements, prop=font, loc="upper left")
            leg3 = figure.ax.legend(handles=legend3_elements, prop=font, labelspacing=1.3, loc=("center right"))
            leg3.set_title(title="GROUP SIZE", prop=font)
            figure.ax.add_artist(leg2)
            figure.ax.add_artist(leg1)

            if log_y:
                figure.ax.set_yscale("log")
                figure.ax.set_ylim(bottom=df_figure_min, top=df_figure_max)
            else:
                figure.ax.set_ylim(bottom=0, top=df_figure_max)

    figures[0].figure.savefig(
        os.path.join(fig_path, f"{intervention_substance}_{measurement_type}.png"),
        bbox_inches="tight", dpi=72)

