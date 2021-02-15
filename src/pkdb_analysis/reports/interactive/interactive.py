import math
import os
import shutil
from pathlib import Path
from typing import Callable, Dict, List, Set

import altair as alt
import pandas as pd
import pint
import seaborn as sns
import yaml

from pkdb_analysis.core import Sid
from pkdb_analysis.data import PKData
from pkdb_analysis.plotting.factory import (
    PlotContentDefinition,
    pkdata_by_plot_content,
    results,
)
from pkdb_analysis.utils import create_parent


alt.data_transformers.disable_max_rows()
# alt.data_transformers.enable('json')

ureg = pint.UnitRegistry()


class LegendArgs(object):
    def __init__(self, field, init=None):
        self.field = field
        self.init = init


def column_to_color(column):
    mapping = {v: n for n, v in enumerate(column.unique())}
    colors = sns.color_palette(
        "colorblind",
        12,
    ).as_hex()

    return column.apply(lambda x: colors[mapping[x]])


def expand_df(df, on):
    result_df = pd.DataFrame()
    black = "#323232"
    for choice, mc in on.items():
        this_df = df.copy()

        this_df["show"] = choice
        this_df["show_value"] = df[mc.field]

        for key in on.keys():
            this_df[f"color_{key}"] = black

        this_df[f"color_{choice}"] = column_to_color(df[mc.field])
        this_df[f"color"] = this_df[f"color_{choice}"]
        result_df = result_df.append(this_df)
    return result_df.reset_index(drop=True)


def abs_abs(d):
    return (d["per_bw"] == False) & (d["intervention_per_bw"] == False)


def legend(df, selection, title, value_field, color_field=None, color=None):
    if color_field is not None:
        color = alt.Color(color_field, scale=None, legend=None)

    return (
        alt.Chart(df)
        .mark_rect()
        .encode(
            y=alt.Y(value_field, axis=alt.Axis(title=None)),
            color=alt.condition(selection, color, alt.value("white"), legend=None),
            size=alt.value(250),
        )
        .properties(selection=selection, title=title)
    )


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def create_interactive_plot(
    df, path, tooltip, multi_legend, multi_color_legend, create_json=True
):
    df = expand_df(df, multi_color_legend)
    measurement_type = df["measurement_type"].unique()[0]
    u_unit = ureg(df["unit"].unique()[0])
    u_unit_intervention = ureg(df["intervention_unit"].unique()[0])
    substance = df["substance"].unique()[0]
    substance_intervention = df["intervention_substance"].unique()[0]

    y_axis_label = f"{substance} {measurement_type}"
    y_title = f"{y_axis_label} [{u_unit.u :~P}]".capitalize()
    x_label = f"{substance_intervention} dose"
    x_title = f"{x_label} [{u_unit_intervention.u :~P}]".capitalize()

    y_domain = alt.selection_interval(bind="scales", encodings=["y"])
    x_domain = alt.selection_interval(bind="scales", encodings=["x"])
    brush = alt.selection(type="interval")

    input_dropdown = alt.binding_select(options=df["show"].unique().tolist(), name=" ")
    selection_base = alt.selection_single(
        fields=["show"], bind=input_dropdown, init={"show": "Sex"}
    )

    multi_color_legend_fields = {
        key: mc.field for key, mc in multi_color_legend.items()
    }
    multi_legends = {**multi_color_legend_fields, **multi_legend}
    selections_multi_color = {}

    for key, mc in multi_color_legend.items():
        kwargs = {"fields": [mc.field]}
        if mc.init is not None:
            kwargs["init"] = [{mc.field: field for field in mc.init}]
        selections_multi_color[key] = alt.selection_multi(**kwargs)

    selections_multi = {
        key: alt.selection_multi(fields=[value]) for key, value in multi_legend.items()
    }
    selections_multi = {**selections_multi, **selections_multi_color}

    def filter_transform_no_brush(base):
        base = base.transform_filter(selection_base)
        for key, selection in selections_multi.items():
            base = base.transform_filter(selection)
        return base

    def filter_transform_all(base):
        return filter_transform_no_brush(base).transform_filter(brush)

    y_max = df.y.max()
    y_min = df.y.min()
    x_max = df.intervention_value.max()
    x_min = df.intervention_value.min()

    size_max = df.subject_count.max()
    bins = 50

    stepsize_y = (y_max - y_min) / bins
    stepsize_x = (x_max - x_min) / bins

    titles = {}

    for key in ["age", "weight"]:
        try:
            _u_unit = ureg(df[f"unit_{key}"].dropna().unique()[0])
            titles[key] = f"{key} [{_u_unit.u :~P}]".capitalize()
        except:
            # FIXME: too broad except
            titles[key] = f'{key} [""]'.capitalize()

    relevant_columns = {
        "age",
        "min_sd_age",
        "max_sd_age",
        "weight",
        "min_sd_weight",
        "max_sd_weight",
        "intervention_value",
        "y",
        "y_min",
        "y_max",
        "show",
        "show_value",
        "color",
        "data_type",
        "url",
        "subject_count",
    }

    color_columns = {f"color_{name}" for name in multi_color_legend.keys()}
    tooltip_columns = {name[:-2] for name in tooltip}

    relevant_columns = relevant_columns.union(set(multi_legends.values())).union(
        color_columns
    )
    relevant_columns = relevant_columns.union(tooltip_columns)

    # FIXME (? what does this FIXME mean?)
    df = df[relevant_columns.intersection(df.columns)]

    x_age = alt.X(
        "age:Q",
        scale=alt.Scale(domain=[0, 100], clamp=True),
        axis=alt.Axis(title=titles["age"]),
    )
    y_weight = alt.Y(
        "weight:Q",
        scale=alt.Scale(domain=[0, 150], clamp=True),
        axis=alt.Axis(title=titles["weight"]),
    )

    errorbars_y = filter_transform_no_brush(
        alt.Chart(df)
        .mark_errorbar()
        .encode(
            x=alt.X(
                "intervention_value:Q",
                axis=alt.Axis(title=x_title),
                scale=alt.Scale(domain=x_domain, clamp=True),
            ),
            y=alt.Y(
                "y_min:Q",
                axis=alt.Axis(title=y_title),
                scale=alt.Scale(domain=y_domain, clamp=True),
            ),
            y2="y_max:Q",
            color=alt.Color("color:N", scale=None, legend=None),
            opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.1)),
        )
    ).add_selection(
        brush
    )  # .add_selection(selection_base)

    errorbars_weight = (
        filter_transform_no_brush(
            alt.Chart(df)
            .mark_errorbar()
            .encode(
                x=x_age,
                y=alt.Y(
                    "min_sd_weight:Q",
                    scale=alt.Scale(domain=[0, 150], clamp=True),
                    axis=alt.Axis(title=titles["weight"]),
                ),
                y2="max_sd_weight:Q",
                color=alt.Color("color:N", scale=None, legend=None),
                opacity=alt.condition(
                    brush, alt.OpacityValue(1), alt.OpacityValue(0.1)
                ),
            )
        )
        .properties(height=300, width=500)
        .add_selection(brush)
        .add_selection(selection_base)
    )

    errorbars_age = (
        filter_transform_no_brush(
            alt.Chart(df)
            .mark_errorbar()
            .encode(
                x=alt.X(
                    "min_sd_age:Q",
                    scale=alt.Scale(domain=[0, 100], clamp=True),
                    axis=alt.Axis(title=titles["age"]),
                ),
                x2="max_sd_age:Q",
                y=y_weight,
                color=alt.Color("color:N", scale=None, legend=None),
                opacity=alt.condition(
                    brush, alt.OpacityValue(1), alt.OpacityValue(0.1)
                ),
            )
        )
        .properties(height=300, width=500)
        .add_selection(brush)
        .add_selection(selection_base)
    )

    domain_marker = ["publication", "from timecourse", "from bodyweight"]
    range_marker = ["circle", "square", "triangle"]

    scatter = filter_transform_no_brush(
        alt.Chart(df)
        .properties(height=350, width=500)
        .mark_point(opacity=0.8, filled=True)
        .encode(
            x=alt.X(
                "intervention_value:Q",
                axis=alt.Axis(title=x_title),
                scale=alt.Scale(domain=x_domain, clamp=True),
            ),
            y=alt.Y(
                "y:Q",
                axis=alt.Axis(title=y_title),
                scale=alt.Scale(domain=y_domain, clamp=True),
            ),
            color=alt.Color("color:N", scale=None, legend=None),
            opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.1)),
            shape=alt.Shape(
                "data_type:N",
                scale=alt.Scale(domain=domain_marker, range=range_marker),
                legend=alt.Legend(title="Data type", orient="left"),
            ),
            size=alt.Size(
                "subject_count:Q",
                scale=alt.Scale(domain=[0, size_max]),
                legend=alt.Legend(title="Number of subjects", orient="left"),
            ),
            href="url:N",
            tooltip=tooltip,
        )
        .add_selection(brush)
        .add_selection(selection_base)
    )

    bars = filter_transform_all(
        alt.Chart(df)
        .properties(width=500)
        .mark_bar()
        .encode(
            y=alt.Y("show_value:N", axis=alt.Axis(title=None)),
            color=alt.Color("color:N", scale=None, legend=None),
            x=alt.X("sum(subject_count):Q", axis=alt.Axis(title="Number of subjects")),
        )
    )

    histo_y = filter_transform_all(
        alt.Chart(df)
        .properties(height=350, width=80)
        .mark_bar(
            opacity=0.9,
        )
        .encode(
            y=alt.Y(
                "y:Q",
                axis=None,
                bin=alt.Bin(maxbins=bins, minstep=stepsize_y),
                scale=alt.Scale(domain=[y_min, y_max], clamp=True),
            ),
            color=alt.Color("color:N", scale=None, legend=None),
            x=alt.X("sum(subject_count):Q", axis=None, stack="normalize"),
        )
        .add_selection(y_domain)
    ).interactive()

    histo_x = filter_transform_all(
        alt.Chart(df)
        .properties(height=80, width=500)
        .mark_bar(
            opacity=0.9,
        )
        .encode(
            x=alt.X(
                "intervention_value:Q",
                axis=None,
                bin=alt.Bin(maxbins=bins, minstep=stepsize_x),
                scale=alt.Scale(domain=[x_min, x_max], clamp=True),
            ),
            color=alt.Color("color:N", scale=None, legend=None),
            y=alt.Y("sum(subject_count):Q", axis=None, stack="normalize"),
        )
        .add_selection(x_domain)
    ).interactive()

    legends_color = {}
    for name, key in multi_color_legend_fields.items():
        legends_color[name] = legend(
            df, selections_multi[name], f"{name}", f"{key}:N", f"color_{name}:N"
        ).transform_filter(selection_base)

    legend_black = {}
    for name, key in multi_legend.items():
        legend_black[name] = legend(
            df,
            selections_multi[name],
            f"{name}",
            f"{key}:N",
            color=alt.value("#323232"),
        ).transform_filter(selection_base)

    pk_plot = alt.vconcat(alt.hconcat(scatter + errorbars_y, histo_y))
    age_weight_plot = (
        errorbars_age + errorbars_weight + scatter.encode(x=x_age, y=y_weight)
    )
    legends_color_plot = alt.vconcat(*legends_color.values())
    legend_black_plot = alt.vconcat(*legend_black.values())

    chart = alt.vconcat(
        histo_x,
        pk_plot & age_weight_plot & bars
        | alt.hconcat(legends_color_plot, legend_black_plot),
    )

    if create_json:
        chart.save(
            f"{path}.json",
        )
    else:
        chart.save(
            f"{path}.html", webdriver="firefox", embed_options={"renderer": "svg"}
        )


def check_legends(df, legend_keys):
    for legend_key in legend_keys:
        assert legend_key in df, f"{legend_key} is not in your data"


def create_navigation_file(results_dict, path):
    navigation = []

    for plot_content, result_infer in results_dict.items():
        this_nav = {"name": plot_content.key, "link": "/#", "dropdown": []}
        for group, df in result_infer.groupby("unit_category"):

            u_unit = ureg(df["unit"].unique()[0])
            u_unit_intervention = ureg(df["intervention_unit"].unique()[0])
            this_dropdown_item = {
                "name": f"{plot_content.key} [{u_unit.u :~P}] / dosing [{u_unit_intervention.u :~P}]".capitalize(),
                "link": f"/_pages/{plot_content.key}_{group}/",
            }
            this_nav["dropdown"].append(this_dropdown_item)

        navigation.append(this_nav)
        path_data = path / "_data"
        path_data.mkdir(exist_ok=True)
        with open(path / "_data" / "navigation.yml", "w") as f:
            f.write(yaml.dump(navigation))


def create_pages(results_dict, path):
    for plot_content, result_infer in results_dict.items():
        for group, df in result_infer.groupby("unit_category"):

            u_unit = ureg(df["unit"].unique()[0])
            u_unit_intervention = ureg(df["intervention_unit"].unique()[0])
            intervention_substance = df["intervention_substance"].unique()[0]

            content = {
                "title": f"{plot_content.key} [{u_unit.u :~P}] / dosing [{u_unit_intervention.u :~P}]".capitalize(),
                "subtitle": f"Meta analysis of {intervention_substance} {plot_content.key}",
                "layout": "pk",
                "hero_height": "80px",
                "json": f"{plot_content.key}_{group}.json",
            }
            path_pages = path / "_pages"
            path_pages.mkdir(exist_ok=True)
            with open(path / "_pages" / f"{plot_content.key}_{group}.md", "w") as f:
                f.write("---\n")
                f.write(yaml.dump(content))
                f.write("---\n")


def create_plots(
    results_dict, path, multi_legend, multi_color_legend, tooltip, create_json
):
    for plot_content, result_infer in results_dict.items():
        for group, df in result_infer.groupby("unit_category"):
            path_reports = path / "_static" / "reports"
            path_reports.mkdir(parents=True, exist_ok=True)
            file_name = path_reports / f"{plot_content.key}_{group}"
            multi_color_legend_fields = [mc.field for mc in multi_color_legend.values()]
            check_legends(df, [*multi_color_legend_fields, *multi_legend.values()])
            create_interactive_plot(
                df,
                file_name,
                tooltip=tooltip,
                multi_legend=multi_legend,
                multi_color_legend=multi_color_legend,
                create_json=create_json,
            )


def copy_dir(src, dst, substance):
    """
    Recursively copies the content of the directory src to the directory dst.
    If dst doesn't exist, it is created, together with all missing parent directories.
    If a file from src already exists in dst, the file in dst is overwritten.
    Files already existing in dst which don't exist in src are preserved.
    Symlinks inside src are copied as symlinks, they are not resolved before copying.

    :param src:
    :param dst:
    :return:
    """
    dst.mkdir(parents=True, exist_ok=True)
    for item in os.listdir(src):
        s = src / item
        d = dst / item
        if s.is_dir():
            copy_dir(s, d, substance)
        else:
            if str(s).endswith(".md") or str(s).endswith(".yml"):
                with open(s, "r") as f:
                    data = f.read()
                    with open(d, "w") as df:
                        df.write(
                            data.replace("?Substance?", substance.capitalize()).replace(
                                "?substance?", substance
                            )
                        )
            else:
                shutil.copy2(str(s), str(d))


def interactive_plot_factory(
    pkdata: PKData,
    plotting_categories: List[PlotContentDefinition],
    intervention_substances: Set[Sid],
    output_substances: Set[Sid],
    exclude_study_names: Set[str],
    additional_information: Dict[str, Callable],
    multi_color_legend,
    multi_legend,
    tooltip,
    path: Path,
    url: str = "http://0.0.0.0:8081",
    create_json=True,
    replacements={},
):
    intervention_substances_str = {
        substance.sid for substance in intervention_substances
    }
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
        url=url,
        replacements=replacements,
    )
    copy_dir(Path(__file__).parent / "template", path, "_".join(output_substances_str))
    create_parent(path)
    create_navigation_file(results_dict, path)
    create_pages(results_dict, path)
    create_plots(
        results_dict,
        path,
        multi_legend,
        multi_color_legend,
        tooltip,
        create_json=create_json,
    )
