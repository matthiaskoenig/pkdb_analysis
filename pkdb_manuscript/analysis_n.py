import matplotlib.pyplot as plt
from collections import namedtuple
from matplotlib.ticker import FormatStrFormatter
from matplotlib.lines import Line2D
from matplotlib import rc

from utils import abs_idx,rel_idx,group_idx,individual_idx
import os
import matplotlib.ticker as ticker
import pint
ureg = pint.UnitRegistry()

#plt.rcParams.update({
#        'axes.labelsize': '20',
#        'axes.labelweight': 'bold',
#        'axes.titlesize': 'medium',
#        'axes.titleweight': 'bold',
#        'legend.fontsize': '20',
#        'xtick.labelsize': '20',
#        'ytick.labelsize': '20',
#        'figure.facecolor': '1.00'
#    })

import matplotlib.font_manager as font_manager
font = font_manager.FontProperties(family='Roboto Mono',
                                   weight='normal',
                                   style='normal', size=16,)


#mpl.rcParams['text.latex.preamble'] = [
#       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
#       s'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       #r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       #r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
#]

#mpl.rcParams['text.usetex'] = True 
    

import matplotlib.font_manager as font_manager
font = font_manager.FontProperties(family='Roboto Mono',
                                   weight='normal',
                                   style='normal', size=16,)
def cm2inch(value):
    return value/2.54


class FigureTemplate(object):
    def __init__(self, data_idx, intervention_type, output_type):
        self.data_idx = data_idx,
        self.intervention_type = intervention_type
        self.output_type = output_type
        self.figure = False,
        self.ax = False

    def data_subset(self, data):
        return data.loc[self.data_idx]

    def create_figure(self, data, size="big"):
        if len(self.data_subset(data)) > 0:
            if size == "big":
                self.figure, self.ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
            elif size == "small":
                self.figure, self.ax = plt.subplots(nrows=1, ncols=1, figsize=(cm2inch(25), cm2inch(25)))


PlotCategory =  namedtuple('PlotCategory', ['name','color', 'marker','data_idx'])


def create_figures(df_data,size):
    figure_templates = [
        FigureTemplate(
            data_idx=rel_idx(df_data, "unit_intervention") & abs_idx(df_data, "unit"),
            intervention_type="rel",
            output_type="abs"
        )
    ]

    for figure_template in figure_templates:
        figure_template.create_figure(df_data,size)
    return figure_templates


pk_name = {
    "auc_end": "$AUC_{end}$",
    "auc_inf": "$AUC_{\infty}$",
    "clearance": "Clearance",
    "cmax": "$C_{max}$",
    "kel": "$k_{el}$",
    "thalf": "$t_{half}$",
    "tmax": "$t_{max}$",
    "vd": "$Vd$",
}


def create_plots(df_data, categories, fig_path, log_y=False,size="big"):
    measurement_type = df_data["measurement_type"].unique()[0]
    figures = create_figures(df_data,size=size)


    for figure in figures:
        if figure.ax:
            df_figure = figure.data_subset(df_data)

            df_figure_max = max([df_figure["value"].max(), df_figure["mean"].max()]) * 1.05
            df_figure_x_max = df_figure["value_intervention"].max() * 1.05

            df_figure_min = min([df_figure["value"].min(), df_figure["mean"].min()]) / 1.05

            df_individual = df_figure[individual_idx(df_figure)]
            df_group = df_figure[group_idx(df_figure)]

            legend_elements = []

            for plot_category in categories:

                df_category = df_individual[plot_category.data_idx(df_individual)]

                units = df_category["unit"].unique()
                units_intervention = df_category["unit_intervention"].unique()
                assert len(units) <= 1, units
                try:
                    unit = units[0]
                    u_unit = ureg(unit)
                    unit_intervention = units_intervention[0]
                    u_unit_intervention = ureg(unit_intervention)

                    y_axis_label = pk_name.get(measurement_type, measurement_type)

                    figure.ax.set_ylabel(f'{y_axis_label} [{u_unit.u :~P}]')
                    substance_internvetion = df_category["substance_intervention"].unique()[0]
                    x_label = '$\text{Dose}_{\text{'+substance_internvetion+'}}$'
                    figure.ax.set_xlabel(f'{x_label} [{u_unit_intervention.u :~P}]')
                    figure.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

                except IndexError:
                    pass

                individuals_number = len(df_category)

                for (calculated, inferred), df_individuals in df_category.groupby(["calculated", "inferred"]):

                    if calculated:
                        marker = "s"
                    else:
                        marker = plot_category.marker

                    x = df_individuals["value_intervention"]
                    y = df_individuals["value"]
                    figure.ax.scatter(x, y, color=plot_category.color, marker=marker, alpha=0.7, label=None, s=20)

                df_category = df_group[plot_category.data_idx(df_group)]
                df_category = df_category[df_category["mean"].notnull()]
                group_number = len(df_category)
                total_group_individuals = 0
                x_group_max = df_category["value_intervention"].max()
                y_group_max = df_category["mean"].max()

                for i, df_row in df_category.iterrows():
                    if df_row["inferred"]:
                        marker = "v"

                    elif df_row["calculated"]:
                        marker = "s"
                    else:
                        marker = plot_category.marker

                    x_group = df_row["value_intervention"]
                    y_group = df_row["mean"]

                    if figure.output_type == "rel":
                        xerr_group = (df_row[("weight", "sd")] / df_row[("weight", "mean")]) * x_group
                    else:
                        xerr_group = 0
                    yerr_group = df_row["se"]
                    group_count = df_row['group_count']
                    total_group_individuals += group_count

                    figure.ax.errorbar(x_group, y_group, yerr=yerr_group, xerr=xerr_group, color=plot_category.color,
                                       fmt=marker, ms=group_count + 5, alpha=0.7)
                    txt = df_row[('study', '')]
                    figure.ax.annotate(txt, (x_group + (0.01 * x_group_max),
                                             y_group + (0.01 * y_group_max)), alpha=0.7)

                label_text = f"{plot_category.name:<10} IP: {individuals_number:<3} G: {group_number:<3} TP: {int(total_group_individuals + individuals_number):<3}"
                
                # "
                label = Line2D([0], [0], marker='o', color='w', label=label_text, markerfacecolor=plot_category.color,
                               markersize=10)
                legend_elements.append(label)

            legend2_elements = [
                Line2D([0], [0], marker='o', color='w', label=r"PK DATA", markerfacecolor="black", markersize=10),
                Line2D([0], [0], marker='s', color='w', label=r"PK FROM TIME COURSE", markerfacecolor="black",
                       markersize=10),
                Line2D([0], [0], marker='v', color='w', label=r"PK FROM BODY WEIGHT", markerfacecolor="black",
                       markersize=10)

            ]

            legend3_elements = [
                Line2D([0], [10], marker='o', color='w', label=r"1", markerfacecolor="black", markersize=5 + 1),
                Line2D([0], [20], marker='o', color='w', label=r"10", markerfacecolor="black", markersize=5 + 10),
                Line2D([0], [50], marker='o', color='w', label=r"30", markerfacecolor="black", markersize=5 + 30),
            ]

            # figure.ax.set_title(measurement_type.capitalize())
            figure.ax.set_xlim(left=0, right=df_figure_x_max)
            # figure.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            figure.ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))

            leg1 = figure.ax.legend(handles=legend_elements, prop=font, loc="upper right")

            leg2 = figure.ax.legend(handles=legend2_elements, prop=font, loc="upper left")
            leg3 = figure.ax.legend(handles=legend3_elements, prop=font, labelspacing=1.3, loc=("center right"))
            leg3.set_title(title=r"\verb|GROUP SIZE|", prop=font)
            figure.ax.add_artist(leg2)
            figure.ax.add_artist(leg1)

            if log_y:
                figure.ax.set_yscale("log")
                figure.ax.set_ylim(bottom=df_figure_min, top=df_figure_max)
            else:
                figure.ax.set_ylim(bottom=0, top=df_figure_max)

            figure.figure.savefig(
                os.path.join(fig_path, f"{measurement_type}_{figure.output_type}-vs-dosing_{figure.intervention_type}.png"),
                bbox_inches="tight", dpi=300)





