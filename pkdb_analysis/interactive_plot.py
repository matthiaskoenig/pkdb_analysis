import math
import seaborn as sns
import pandas as pd
import pint
import altair as alt

ureg = pint.UnitRegistry()
ureg.define('yr = year')

from pkdb_analysis.meta_analysis import MetaAnalysis
from pkdb_analysis.filter import f_mt_in_substance_in, f_dosing_in


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
    return result_df


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




def create_interactive_plot(df,path, tooltip, multi_legend = {"study": "study_name"}, multi_color_legend= {"sex": "sex", "health": "healthy", "route": "intervention_route", "tissue": "tissue","data_type": "data_type"}):
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
    selection_base = alt.selection_single(fields=['show'], bind=input_dropdown, name='Select Type', init={'show': 'sex'})

    multi_legends  = {**multi_color_legend, **multi_legend}

    #for key in multi_legends:
    #    df[key] = df[key].astype(str)
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


    #u_unit_age = ureg(df["unit_age"].dropna().unique()[0])
    #u_unit_weight = ureg(df["unit_weight"].dropna().unique()[0])
    #title_age = f'age [{u_unit_age.u :~P}]'
    #title_weight = f'weight [{u_unit_weight.u :~P}]'

    x_age = alt.X("age:Q", scale=alt.Scale(domain=[0, 100], clamp=True), axis=alt.Axis(title=titles["age"]))
    y_weight = alt.Y("weight:Q", scale=alt.Scale(domain=[0, 150], clamp=True), axis=alt.Axis(title=titles["weight"]))

    errorbars_y = filter_transform_no_brush(alt.Chart(df).mark_errorbar().encode(
        x=alt.X('intervention_value:Q', axis=alt.Axis(title=x_title), scale=alt.Scale(domain=x_domain, clamp=True)),
        y=alt.Y("y_min:Q", axis=alt.Axis(title=y_title), scale=alt.Scale(domain=y_domain, clamp=True)),
        y2="y_max:Q",
        color=alt.Color('color:N', scale=None, legend=None),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.1)),
    )).add_selection(brush).add_selection(selection_base)

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
            # scale=alt.Scale(domain=(0, 0.012))
            y=alt.Y('y:Q', axis=alt.Axis(title=y_title), scale=alt.Scale(domain=y_domain, clamp=True)),
            # scale=alt.Scale(domain=(0, 28)),
            color=alt.Color('color:N', scale=None, legend=None),
            opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.1)),
            shape=alt.Shape('data_type:N', scale=alt.Scale(domain=domain_marker, range=range_marker)),
            size=alt.Size('subject_count:Q', scale=alt.Scale(domain=[0, size_max])),
            href="url:N",
            tooltip=tooltip,
        ).add_selection(brush).add_selection(selection_base))

    bars = filter_transform_all(alt.Chart(df).properties(width=600).mark_bar().encode(
        y=alt.Y('show_value:N', axis=alt.Axis(title=None)),
        color=alt.Color('color:N', scale=None, legend=None),
        x=alt.X('sum(subject_count):Q', axis=alt.Axis(title="Number of Subjects"))))

    # .mark_area(opacity=0.7, interpolate='step')
    histo_y = filter_transform_all(alt.Chart(df).properties(height=350, width=80).mark_bar(
        opacity=0.9,
    ).encode(
        y=alt.Y('y:Q', axis=None, bin=alt.Bin(maxbins=bins, minstep=stepsize_y),
                scale=alt.Scale(domain=[y_min, y_max], clamp=True)),
        color=alt.Color('color:N', scale=None, legend=None),
        # x=alt.X('sum(subject_count):Q', axis=alt.Axis(title="Number of Subjects"))
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
        legends_color[name] = legend(df, selections_multi[name], f'Select {name}', f'{key}:N', f'color_{name}:N').transform_filter(selection_base)



    legend_black = {}
    for name, key in multi_legend.items():
        legend_black[name] = legend(df, selections_multi[name], f'Select {name}',  f'{key}:N',
                               color=alt.value("#323232")).transform_filter(selection_base)

    pk_plot = alt.vconcat(histo_x, alt.hconcat(scatter + errorbars_y, histo_y))#.resolve_scale(y='shared'))
    age_weight_plot = errorbars_age + errorbars_weight + scatter.encode(x=x_age, y=y_weight)#.resolve_scale(x="independent").properties(height=300, width=500)
    legends_color_plot = alt.hconcat(*legends_color.values())
    legend_black_plot = alt.hconcat(*legend_black.values())


    chart = pk_plot  &  age_weight_plot & bars.resolve_scale(y="independent", x="independent") | \
            legends_color_plot & legend_black_plot
    chart.save(path, webdriver='firefox', embed_options={'renderer': 'svg'})




def pkdata_by_measurement_type(pkdata,
                               measurement_types,
                               intervention_substances,
                               output_substances,
                               exclude_study_names):

    # filter pkdata for given attributes
    data_dict = {}
    for measurement_type in measurement_types:
        data = pkdata.filter_intervention(f_dosing_in,
                                          substances=intervention_substances).filter_output(f_mt_in_substance_in,
                                                                               measurement_types=measurement_type,
                                                                               substances=output_substances).exclude_intervention(
                                                                                    lambda d: d["study_name"].isin(exclude_study_names))
        measurement_type_joined = "_".join(measurement_type)
        data.outputs["measurement_type"] = measurement_type_joined
        data_dict[measurement_type_joined] = data.copy()
    return data_dict


def results(data_dict, intervention_substances, additional_information):
    # creates one dataframe from PKData instance.
    # infers additional results from body weights.
    results_dict = {}
    for measurement_type, pkd in data_dict.items():
        meta_analysis = MetaAnalysis(pkd, intervention_substances)
        meta_analysis.create_results()
        for key, additional_function in additional_information.items():
            meta_analysis.results[key] = meta_analysis.results.apply(additional_function, axis=1)
        meta_analysis.infer_from_body_weight()
        meta_analysis.add_extra_info()
        results = meta_analysis.results
        results_dict[measurement_type] = results
    return results_dict

def check_legends(df, legend_keys):
    for legend_key in legend_keys:
        assert legend_key in df, f"{legend_key} is not in your data"


def create_plots(results_dict,path, multi_legend, multi_color_legend, tooltip):
    for measurement_type, result_infer in results_dict.items():
        for group, df in result_infer.groupby("unit_category"):
            file_name = f'{path}/{measurement_type}_{group}.html'
            check_legends(df, [*multi_color_legend.values(),*multi_legend.values()])
            create_interactive_plot(df, file_name, tooltip=tooltip, multi_legend=multi_legend, multi_color_legend=multi_color_legend)


def interactive_plot_factory(pkdata,
                             measurement_types,
                             intervention_substances,
                             output_substances,
                             exclude_study_names,
                             multi_color_legend,
                             multi_legend,
                             additional_information,
                             tooltip,
                             path):

    data_dict = pkdata_by_measurement_type(pkdata, measurement_types, intervention_substances, output_substances,exclude_study_names)
    results_dict = results(data_dict, intervention_substances, additional_information)
    create_plots(results_dict, path, multi_legend, multi_color_legend, tooltip)

