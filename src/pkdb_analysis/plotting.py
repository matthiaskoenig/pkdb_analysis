import math
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import Normalizer


def _classify(df, n_clusters):
    coocurence_matrix = df.pivot_table(
        index="source", columns="target", aggfunc="sum"
    ).fillna(0)
    norm_coocurence_matrix = Normalizer(norm="l2").fit_transform(coocurence_matrix)
    norm_coocurence_matrix = pd.DataFrame(
        norm_coocurence_matrix,
        index=coocurence_matrix.index,
        columns=coocurence_matrix.columns,
    )
    classification_model = AgglomerativeClustering(
        linkage="single", n_clusters=n_clusters
    )
    classes = classification_model.fit_predict(norm_coocurence_matrix.T.corr())
    nodes = pd.DataFrame()
    nodes["name"] = norm_coocurence_matrix.index
    nodes["group"] = classes
    return nodes


def _detail_link(study):
    substances = [substance["name"] for substance in study.substances]
    substances = combinations(substances, 2)
    substances = pd.DataFrame(substances, columns=["source", "target"])
    substances["study_sid"] = study.sid
    substances["study_name"] = study.name
    return substances


def _basic_links(df):
    df["value"] = 1
    df2 = pd.DataFrame()
    df2["source"] = df["target"]
    df2["target"] = df["source"]
    df2["value"] = df["value"]
    df2["study_sid"] = df["study_sid"]
    df2["study_name"] = df["study_name"]
    return df2.append(df, ignore_index=True)


def _updated_links(basic_links, nodes):
    links = pd.DataFrame()
    map_s = pd.Series(nodes.name).reset_index().set_index("name")["index"]

    links["source"] = basic_links["source"].apply(lambda x: map_s.loc[x])
    links["target"] = basic_links["target"].apply(lambda x: map_s.loc[x])
    links["value"] = basic_links["value"]
    links["study_sid"] = basic_links["study_sid"]  # not jet used
    links["study_name"] = basic_links["study_name"]  # not jet used

    links = links.groupby(["source", "target"]).sum().reset_index()

    return links


def show_values_on_bars(axs, bottom):
    def _show_on_single_plot(ax):
        for p in ax.patches:
            _x = p.get_x() + p.get_width() / 2
            _y = p.get_y() + bottom

            try:
                value = int(p.get_height())
            except ValueError:
                continue

            ax.text(
                _x,
                _y,
                value,
                ha="center",
            )

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)


def arc_plot(pkdata, n_clusters=7):
    df = pd.DataFrame([], columns=["source", "target", "study"])
    for study in pkdata.studies.itertuples():
        df = df.append(_detail_link(study))
    basic_links = _basic_links(df)
    nodes = _classify(basic_links, n_clusters)
    links = _updated_links(basic_links, nodes)
    json_dict = {}
    json_dict["nodes"] = nodes.to_dict(orient="records")
    json_dict["links"] = links.to_dict(orient="records")
    return json_dict


def study_overview(pkdata, title=None, max_values={}, **kwargs):
    fig, axes = plt.subplots(ncols=1, nrows=5, sharex=True, **kwargs)
    if title is not None:
        fig.suptitle(title, fontsize=16)
    sns.set_style("white")
    sns.despine(left=True, bottom=True)
    df = pkdata.studies.df.set_index("name")[
        [
            "group_count",
            "individual_count",
            "intervention_count",
            "output_count",
            "output_calculated_count",
            "timecourse_count",
        ]
    ].replace({0, 0.1})

    colors = sns.color_palette("Set1", n_colors=8, desat=0.5)

    plot_info = [
        {"name": "groups", "col_name": "group_count", "color": colors[0], "ax": 0},
        {
            "name": "individuals",
            "col_name": "individual_count",
            "color": colors[1],
            "ax": 1,
        },
        {
            "name": "interventions",
            "col_name": "intervention_count",
            "color": colors[2],
            "ax": 2,
        },
        {"name": "outputs", "col_name": "output_count", "color": colors[3], "ax": 3},
        {
            "name": "timecourses",
            "col_name": "timecourse_count",
            "color": colors[4],
            "ax": 4,
        },
    ]

    plot_info = pd.DataFrame(plot_info, columns=["ax", "name", "col_name", "color"])
    color_timecourse = colors[4]
    color_output = colors[3]

    for subplot in plot_info.itertuples():
        ax = axes[subplot.ax]
        if subplot.name == "outputs":
            df["output_reported_count"] = (
                df["output_count"] - df["output_calculated_count"]
            )
            data = (
                df[["output_calculated_count", "output_reported_count"]]
                .stack()
                .reset_index(1)
                .rename(columns={"level_1": "type", 0: "value"})
                .replace(
                    {
                        "output_calculated_count": "Calculated",
                        "output_reported_count": "Reported",
                    }
                )
            )

            sns.barplot(
                data=data,
                x=data.index,
                y="value",
                hue=data.type,
                ax=ax,
                palette=[color_timecourse, color_output],
            )
            ax.get_legend().remove()

        else:
            sns.barplot(
                data=df, x=df.index, y=subplot.col_name, ax=ax, color=subplot.color
            )

        ax.set_yscale("log")
        param = {"bottom": 0.1}
        if max_values.get(subplot.name, False):
            param["top"] = max_values.get(subplot.name)
        ax.set_ylim(**param)

        ax.set_xlabel("")

        ax.set_ylabel(subplot.name, rotation=0, labelpad=5, horizontalalignment="right")
        ax.set_yticks([])
        show_values_on_bars(ax, 0.2)
    plt.setp(
        axes[4].get_xticklabels(), rotation=70, horizontalalignment="right", fontsize=8
    )
    return fig


def study_overview_wrapped(pkdata, rows):
    rows_per_plot = math.ceil(len(pkdata.studies) / rows)
    index = 0
    max_values = {
        "groups": pkdata.studies.group_count.max(),
        "individuals": pkdata.studies.individual_count.max(),
        "interventions": pkdata.studies.intervention_count.max(),
        "outputs": pkdata.studies.output_count.max(),
        "timecourses": pkdata.studies.timecourse_count.max(),
    }
    for row in range(rows):
        subset = pkdata.copy()
        new_index = index + rows_per_plot
        subset.studies = subset.studies.iloc[index:new_index]
        index = new_index
        subset._concise()
        fig = study_overview(
            subset, max_values=max_values, figsize=(len(subset.studies), 6)
        )
        fig.savefig(
            f"./caffeine_overview_{rows}-{row}.png", dpi=300, bbox_inches="tight"
        )
