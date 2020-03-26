import math
import seaborn as sns
import pandas as pd
import pint
import altair as alt
import collections
import yaml
import os
import shutil
from pathlib import Path

import json

alt.data_transformers.disable_max_rows()
#alt.data_transformers.enable('json')

ureg = pint.UnitRegistry()
ureg.define('yr = year')

from pkdb_analysis.meta_analysis import MetaAnalysis
from pkdb_analysis.filter import f_mt_in_substance_in, f_dosing_in

PlottingParameter = collections.namedtuple('PlottingParameter',
                                           ['measurement_types',
                                            'units_rm'])

def column_to_color(column):
    mapping = {v: n for n, v in enumerate(column.unique())}
    colors = sns.color_palette("colorblind", 8, ).as_hex()

    return column.apply(lambda x: colors[mapping[x]])


def expand_df(df, on):
    result_df = pd.DataFrame()
    black = "#323232"
    for choice, field in on.items():
        this_df = df.copy()

        this_df["show"] = choice
        this_df["show_value"] = df[field]

        for key in on.keys():
            this_df[f"color_{key}"] = black

        this_df[f"color_{choice}"] = column_to_color(df[field])
        this_df[f"color"] = this_df[f"color_{choice}"]
        result_df = result_df.append(this_df)
    return result_df.reset_index(drop=True)


def abs_abs(d):
    return (d["per_bw"] == False) & (d["intervention_per_bw"] == False)


def legend(df, slection, title, value_field, color_field=None, color=None):
    if color_field is not None:
        color = alt.Color(color_field, scale=None, legend=None)

    return alt.Chart(df).mark_rect().encode(
        y=alt.Y(value_field, axis=alt.Axis(title=None)),
        color=alt.condition(slection, color,
                            alt.value('white'), legend=None),
        size=alt.value(250)
    ).properties(
        selection=slection,
        title=title
    )

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier




def create_interactive_plot(df,path, tooltip,
                            multi_legend,
                            multi_color_legend,
                            create_json=True):
    df = expand_df(df, multi_color_legend)
    measurement_type = df["measurement_type"].unique()[0]
    u_unit = ureg(df["unit"].unique()[0])
    u_unit_intervention = ureg(df["intervention_unit"].unique()[0])
    substance = df["substance"].unique()[0]
    substance_intervention = df["intervention_substance"].unique()[0]





    y_axis_label = f"{substance} {measurement_type}"
    y_title = f'{y_axis_label} [{u_unit.u :~P}]'
    x_label = f'{substance_intervention} dose'
    x_title = f'{x_label} [{u_unit_intervention.u :~P}]'

    y_domain = alt.selection_interval(bind='scales', encodings=['y'])
    x_domain = alt.selection_interval(bind='scales', encodings=['x'])
    brush = alt.selection(type='interval')

    input_dropdown = alt.binding_select(options=df["show"].unique().tolist())
    selection_base = alt.selection_single(fields=['show'], bind=input_dropdown, init={'show': 'Sex'})


    multi_legends  = {**multi_color_legend, **multi_legend}

    selections_multi = {key :alt.selection_multi(fields=[value])for key, value in multi_legends.items()}


    def filter_transform_no_brush(base):
        base = base.transform_filter(selection_base)
        for key, selection in selections_multi.items():
            base = base.transform_filter(selection)
        return base

    def filter_transform_all(base):
        return filter_transform_no_brush(base).transform_filter(
        brush)

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
            titles[key] = f'{key} [{_u_unit.u :~P}]'
        except:
            titles[key] = f'{key} [""]'



    relevant_columns = {"age",
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
                        "subject_count"}

    color_columns =    {f"color_{name}" for name in multi_color_legend.keys()}


    relevant_columns = relevant_columns.union(set(multi_legends.values())).union(color_columns)


    df = df[relevant_columns]


    x_age = alt.X("age:Q", scale=alt.Scale(domain=[0, 100], clamp=True), axis=alt.Axis(title=titles["age"]))
    y_weight = alt.Y("weight:Q", scale=alt.Scale(domain=[0, 150], clamp=True), axis=alt.Axis(title=titles["weight"]))

    errorbars_y = filter_transform_no_brush(alt.Chart(df).mark_errorbar().encode(
        x=alt.X('intervention_value:Q', axis=alt.Axis(title=x_title), scale=alt.Scale(domain=x_domain, clamp=True)),
        y=alt.Y("y_min:Q", axis=alt.Axis(title=y_title), scale=alt.Scale(domain=y_domain, clamp=True)),
        y2="y_max:Q",
        color=alt.Color('color:N', scale=None, legend=None),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.1)),
    )).add_selection(brush)#.add_selection(selection_base)

    errorbars_weight = filter_transform_no_brush(alt.Chart(df).mark_errorbar().encode(
        x=x_age,
        y=alt.Y("min_sd_weight:Q", scale=alt.Scale(domain=[0, 150], clamp=True), axis=alt.Axis(title=titles["weight"])),
        y2="max_sd_weight:Q",
        color=alt.Color('color:N', scale=None, legend=None),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.1)),
    )).properties(height=300, width=500).add_selection(brush).add_selection(selection_base)

    errorbars_age = filter_transform_no_brush(alt.Chart(df).mark_errorbar().encode(
        x=alt.X("min_sd_age:Q", scale=alt.Scale(domain=[0, 100], clamp=True), axis=alt.Axis(title=titles["age"])),
        x2="max_sd_age:Q",
        y=y_weight,
        color=alt.Color('color:N', scale=None, legend=None),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.1)),
    )).properties(height=300, width=500).add_selection(brush).add_selection(selection_base)

    domain_marker = ['from publication', 'from timecourse', 'from body weight']
    range_marker = ['circle', 'square', 'triangle']

    scatter = filter_transform_no_brush(
        alt.Chart(df).properties(height=350, width=500).mark_point(opacity=0.8, filled=True).encode(
            x=alt.X('intervention_value:Q', axis=alt.Axis(title=x_title), scale=alt.Scale(domain=x_domain, clamp=True)),
            y=alt.Y('y:Q', axis=alt.Axis(title=y_title), scale=alt.Scale(domain=y_domain, clamp=True)),
            color=alt.Color('color:N', scale=None, legend=None),
            opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.1)),
            shape=alt.Shape('data_type:N', scale=alt.Scale(domain=domain_marker, range=range_marker), legend=alt.Legend(title="Data Type",orient="left")),
            size=alt.Size('subject_count:Q', scale=alt.Scale(domain=[0, size_max]), legend=alt.Legend( title="Number of Subjects", orient="left")),
            href="url:N",
            tooltip=tooltip,
        ).add_selection(brush).add_selection(selection_base))

    bars = filter_transform_all(alt.Chart(df).properties(width=500).mark_bar().encode(
        y=alt.Y('show_value:N', axis=alt.Axis(title=None)),
        color=alt.Color('color:N', scale=None, legend=None),
        x=alt.X('sum(subject_count):Q', axis=alt.Axis(title="Number of Subjects"))))

    histo_y = filter_transform_all(alt.Chart(df).properties(height=350, width=80).mark_bar(
        opacity=0.9,
    ).encode(
        y=alt.Y('y:Q', axis=None, bin=alt.Bin(maxbins=bins, minstep=stepsize_y),
                scale=alt.Scale(domain=[y_min, y_max], clamp=True)),
        color=alt.Color('color:N', scale=None, legend=None),
        x=alt.X('sum(subject_count):Q', axis=None, stack="normalize")).add_selection(y_domain)).interactive()

    histo_x = filter_transform_all(alt.Chart(df).properties(height=80, width=500).mark_bar(
        opacity=0.9,
    ).encode(
        x=alt.X('intervention_value:Q', axis=None, bin=alt.Bin(maxbins=bins, minstep=stepsize_x),
                scale=alt.Scale(domain=[x_min, x_max], clamp=True)),
        color=alt.Color('color:N', scale=None, legend=None),
        y=alt.Y('sum(subject_count):Q', axis=None, stack="normalize")).add_selection(x_domain)).interactive()


    legends_color = {}
    for name, key in multi_color_legend.items():
        legends_color[name] = legend(df, selections_multi[name], f'{name}', f'{key}:N', f'color_{name}:N').transform_filter(selection_base)



    legend_black = {}
    for name, key in multi_legend.items():
        legend_black[name] = legend(df, selections_multi[name], f'{name}',  f'{key}:N', color=alt.value("#323232")).transform_filter(selection_base)

    pk_plot = alt.vconcat( alt.hconcat(scatter + errorbars_y, histo_y))
    age_weight_plot = errorbars_age + errorbars_weight + scatter.encode(x=x_age, y=y_weight)
    legends_color_plot = alt.vconcat(*legends_color.values())
    legend_black_plot = alt.vconcat(*legend_black.values())

    chart = alt.vconcat(histo_x, pk_plot & age_weight_plot & bars | \
                        alt.hconcat(legends_color_plot, legend_black_plot))

    if create_json:
        chart.save(f"{path}.json", )
    else:
        chart.save(f"{path}.html", webdriver='firefox', embed_options={'renderer': 'svg'})


def pkdata_by_measurement_type(pkdata,
                               plotting_categories: PlottingParameter,
                               intervention_substances,
                               output_substances,
                               exclude_study_names):

    # filter pkdata for given attributes
    data_dict = {}
    for plotting_category in plotting_categories:
        data = pkdata.filter_intervention(f_dosing_in,
                                          substances=intervention_substances).filter_output(f_mt_in_substance_in,
                                                                               measurement_types=plotting_category.measurement_types,
                                                                               substances=output_substances)
        data = data.exclude_output(lambda d : d["unit"].isin(plotting_category.units_rm))
        data = data.exclude_intervention(lambda d: d["study_name"].isin(exclude_study_names))

        measurement_type_joined = "_".join(plotting_category.measurement_types)
        data.outputs["measurement_type"] = measurement_type_joined
        data_dict[measurement_type_joined] = data.copy()
    return data_dict


def results(data_dict, intervention_substances, additional_information,url):
    # creates one dataframe from PKData instance.
    # infers additional results from body weights.
    results_dict = {}
    for measurement_type, pkd in data_dict.items():
        meta_analysis = MetaAnalysis(pkd, intervention_substances, url)
        meta_analysis.create_results()
        for key, additional_function in additional_information.items():
            meta_analysis.results[key] = meta_analysis.results.apply(additional_function, axis=1)
        meta_analysis.infer_from_body_weight()
        meta_analysis.add_extra_info()
        results = meta_analysis.results
        results_dict[measurement_type] = results
        print(measurement_type)
        print(len(results))

    return results_dict

def check_legends(df, legend_keys):
    for legend_key in legend_keys:
        assert legend_key in df, f"{legend_key} is not in your data"

def create_navigation_file(results_dict, path):
    navigation = []

    for measurement_type, result_infer in results_dict.items():
        this_nav = {
        "name": measurement_type,
        "link": "/#",
        "dropdown": []
        }
        for group, df in result_infer.groupby("unit_category"):

            u_unit = ureg(df["unit"].unique()[0])
            u_unit_intervention = ureg(df["intervention_unit"].unique()[0])


            this_dropdown_item = {
                "name":f"{measurement_type} [{u_unit.u :~P}] / dosing [{u_unit_intervention.u :~P}]",
                "link": f"/_pages/{measurement_type}_{group}/",
            }
            this_nav["dropdown"].append(this_dropdown_item)

        navigation.append(this_nav)
        with open(f"{path}_data/navigation.yml", "w") as f:
         f.write(yaml.dump(navigation))

def create_pages(results_dict, path):
    for measurement_type, result_infer in results_dict.items():
        this_nav = {
            "name": measurement_type,
            "link": "/#",
            "dropdown": []
        }
        for group, df in result_infer.groupby("unit_category"):

            u_unit = ureg(df["unit"].unique()[0])
            u_unit_intervention = ureg(df["intervention_unit"].unique()[0])
            u_unit_intervention = ureg(df["intervention_unit"].unique()[0])
            intervention_substance = df["intervention_substance"].unique()[0]

            content = {
                "title": f"{measurement_type} [{u_unit.u :~P}] / dosing [{u_unit_intervention.u :~P}]",
                "subtitle": f"Meta analysis of {intervention_substance} {measurement_type}",
                "layout": "pk",
                "json": f"{measurement_type}_{group}.json"

            }

            with open(f"{path}_pages/{measurement_type}_{group}.md", "w") as f:
                f.write("---\n")
                f.write(yaml.dump(content))
                f.write("---\n")



def create_plots(results_dict,path, multi_legend, multi_color_legend, tooltip, create_json):
    for measurement_type, result_infer in results_dict.items():
        for group, df in result_infer.groupby("unit_category"):
            file_name = f'{path}/_static/reports/{measurement_type}_{group}'
            check_legends(df, [*multi_color_legend.values(),*multi_legend.values()])
            create_interactive_plot(df, file_name, tooltip=tooltip, multi_legend=multi_legend, multi_color_legend=multi_color_legend, create_json=create_json)



def copy_dir(src, dst,substance):
    """
    Recusively copies the content of the directory src to the directory dst.
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
            copy_dir(s, d,substance)
        else:
            if str(s).endswith(".md") or str(s).endswith(".yml"):
                with open(s, 'r') as f:
                    data = f.read()
                    with open(d, 'w') as df:
                        df.write(data.replace("?Substance?", substance.capitalize()).replace("?substance?", substance))
            else:
                shutil.copy2(str(s), str(d))

def interactive_plot_factory(pkdata,
                             plotting_categories,
                             intervention_substances,
                             output_substances,
                             exclude_study_names,
                             multi_color_legend,
                             multi_legend,
                             additional_information,
                             tooltip,
                             path,
                             url="http://0.0.0.0:8081",
                             create_json = True,
                             ):

    data_dict = pkdata_by_measurement_type(pkdata, plotting_categories, intervention_substances, output_substances,exclude_study_names)
    results_dict = results(data_dict=data_dict, intervention_substances=intervention_substances, additional_information=additional_information,url=url)
    copy_dir(Path(__file__).parent / "template",Path(path), "_".join(output_substances))
    create_navigation_file(results_dict, path)
    create_pages(results_dict, path)
    create_plots(results_dict, path, multi_legend, multi_color_legend, tooltip, create_json=create_json)
