import math
import seaborn as sns
import pandas as pd
import pint
import altair as alt

ureg = pint.UnitRegistry()
ureg.define('yr = year')


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
    return (d["per_bodyweight"] == False) & (d["intervention_per_bodyweight"] == False)


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




def create_interactive_plot(df,path, multi_legend = {"study": "study_name"}, multi_color_legend= {"sex": "sex", "health": "healthy", "route": "intervention_route", "tissue": "tissue","data_type": "data_type"}):

    df = expand_df(df, multi_color_legend)
    u_unit = ureg(df["unit"].unique()[0])
    u_unit_intervention = ureg(df["intervention_unit"].unique()[0])
    measurement_type = df["measurement_type"].unique()[0]
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



    selections_multi = {key:alt.selection_multi(fields=[key])for key in {**multi_color_legend, **multi_legend}}



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

    u_unit_age = ureg(df["unit_age"].dropna().unique()[0])
    u_unit_weight = ureg(df["unit_weight"].dropna().unique()[0])
    title_age = f'age [{u_unit_age.u :~P}]'
    title_weight = f'weight [{u_unit_weight.u :~P}]'

    x_age = alt.X("age:Q", scale=alt.Scale(domain=[0, 100], clamp=True), axis=alt.Axis(title=title_age))
    y_weight = alt.Y("weight:Q", scale=alt.Scale(domain=[0, 150], clamp=True), axis=alt.Axis(title=title_weight))

    errorbars_y = filter_transform_no_brush(alt.Chart(df).mark_errorbar().encode(
        x=alt.X('intervention_value:Q', axis=alt.Axis(title=x_title), scale=alt.Scale(domain=x_domain, clamp=True)),
        y=alt.Y("y_min:Q", axis=alt.Axis(title=y_title), scale=alt.Scale(domain=y_domain, clamp=True)),
        y2="y_max:Q",
        color=alt.Color('color:N', scale=None, legend=None),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.1)),
    )).add_selection(brush).add_selection(selection_base)

    errorbars_weight = filter_transform_no_brush(alt.Chart(df).mark_errorbar().encode(
        x=x_age,
        y=alt.Y("min_sd_weight:Q", scale=alt.Scale(domain=[0, 150], clamp=True), axis=alt.Axis(title=title_weight)),
        y2="max_sd_weight:Q",
        color=alt.Color('color:N', scale=None, legend=None),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.1)),
    )).properties(height=300, width=500).add_selection(brush).add_selection(selection_base)

    errorbars_age = filter_transform_no_brush(alt.Chart(df).mark_errorbar().encode(
        x=alt.X("min_sd_age:Q", scale=alt.Scale(domain=[0, 100], clamp=True), axis=alt.Axis(title=title_age)),
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
            tooltip=['intervention_value:Q', 'y:Q', 'output_pk:N', 'study_name:N', 'study_sid:N', "url:N",
                     "individual_name", "group_name:N", "weight:Q", "unit_weight:N", "sex:N"],
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

    chart = alt.vconcat(histo_x, alt.hconcat(scatter + errorbars_y, histo_y)) & bars | alt.vconcat(
        errorbars_age + errorbars_weight + scatter.encode(x=x_age, y=y_weight).properties(height=300, width=500),
        alt.hconcat(*legends_color.values()) | alt.hconcat(*legend_black.values()))
    chart.save(path, webdriver='firefox', embed_options={'renderer': 'svg'})