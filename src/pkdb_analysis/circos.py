""" This module creates configuration files for circos plots."""
from pathlib import Path

import pandas as pd

from pkdb_analysis.utils import create_parent


def create_ideogram(studies_data):
    type_to_label = studies_data.set_index("type").to_dict()["label"]
    ideogram = pd.DataFrame()
    ideogram["len"] = studies_data.groupby(["type"]).apply(len)
    ideogram.index = ideogram.index.astype(int)
    ideogram["label"] = ideogram.apply(lambda x: type_to_label[x.name], axis=1)
    return ideogram.sort_values("label")


def create_config_files(studies_data: pd.DataFrame, path: Path):
    rows_per_study = 1
    ideogram = create_ideogram(studies_data)
    data_dir = path / "data"
    ideogram_path = data_dir / "ideogram.txt"
    create_parent(ideogram_path)
    with open(ideogram_path, "w") as f:

        for idx, substance in ideogram.reset_index().iterrows():
            number = idx + 1
            f.write(
                f"chr - {substance.label} {substance.label} 0 {substance.len * rows_per_study} pastel2-6-qual-{number}\n"
            )
    frames = []
    for _, data in studies_data.groupby("label"):
        data["start"] = range(0, len(data) * rows_per_study, rows_per_study)
        data["end"] = range(
            rows_per_study, (len(data) + 1) * rows_per_study, rows_per_study
        )
        frames.append(data)
    studies_data = pd.concat(frames)
    # names 2d track
    studies_data[["label", "start", "end", "name"]].to_csv(
        data_dir / "study_names.txt", sep=" ", header=False, index=False
    )
    # all subjects number for number track
    studies_data[["label", "start", "end", "subjects"]].to_csv(
        data_dir / "all_subjects_number.txt",
        sep=" ",
        header=False,
        index=False,
    )
    studies_data[["label", "start", "end", "timecourses"]].to_csv(
        data_dir / "timecourse_number.txt",
        sep=" ",
        header=False,
        index=False,
    )
    studies_data[["label", "start", "end", "outputs"]].to_csv(
        data_dir / "output_number.txt", sep=" ", header=False, index=False
    )
    studies_data[["label", "start", "end", "interventions"]].to_csv(
        data_dir / "intervention_number.txt",
        sep=" ",
        header=False,
        index=False,
    )

    bubbles_data_dict = bubbles_data(studies_data, 25)
    for name, data in bubbles_data_dict.items():
        data[["label", "start", "end", "type", "circle_type"]].to_csv(
            data_dir / f"{name}_bubble.txt", sep=" ", header=False, index=False
        )


def bubbles_data(studies_data, big_bubble_size):
    studies_data["outputs_raw"] = (
        studies_data["outputs"] - studies_data["outputs_calculated"]
    )
    studies_data["subjects_minus_individuals"] = (
        studies_data["subjects"] - studies_data["individuals"]
    )
    # studies_data["group_not_individual"] = studies_data[
    #    "group_not_individual"
    # ].mask(studies_data["group_not_individual"] < 0, 0)

    outputs_df = pd.DataFrame()
    timecourses_df = pd.DataFrame()
    interventions_df = pd.DataFrame()
    group_members_df = pd.DataFrame()

    for idx, study in studies_data.iterrows():

        raw_outputs = study_expand(study, "outputs_raw", big_bubble_size, "raw")
        if len(raw_outputs) > 0:
            outputs_df = outputs_df.append(raw_outputs)

        calc_outputs = study_expand(
            study, "outputs_calculated", big_bubble_size, "calc"
        )
        if len(calc_outputs) > 0:
            outputs_df = outputs_df.append(calc_outputs)

        timecourse = study_expand(study, "timecourses", big_bubble_size)
        if len(timecourse) > 0:
            timecourses_df = timecourses_df.append(timecourse)

        interventions = study_expand(study, "interventions", big_bubble_size)
        if len(interventions) > 0:
            interventions_df = interventions_df.append(interventions)

        group_subject = study_expand(
            study, "subjects_minus_individuals", big_bubble_size, "group_subjects"
        )
        if len(group_subject) > 0:
            group_members_df = group_members_df.append(group_subject)

        individuals = study_expand(study, "individuals", big_bubble_size, "individuals")
        if len(individuals) > 0:
            group_members_df = group_members_df.append(individuals)

    return {
        "outputs": outputs_df,
        "timecourses": timecourses_df,
        "interventions": interventions_df,
        "group_members": group_members_df,
    }


def study_expand(study, count_label, threshold, type_name="raw"):
    outputs = pd.DataFrame()
    study_numbers = study[count_label]
    df_study = study[["label", "start", "end"]]
    df_study["circle_type"] = None

    if type_name:
        df_study["type"] = type_name

    div, modulo = divmod(int(study_numbers), threshold)

    mega_size, div = divmod(int(div), 10)

    if mega_size > 0:
        mega_size_study = df_study.copy()
        mega_size_study["circle_type"] = "circle_type=M"
        expanded_outputs = pd.concat(
            [pd.DataFrame(mega_size_study).T] * mega_size, ignore_index=True
        )
        outputs = outputs.append(expanded_outputs)

    if div > 0:
        big_study = df_study.copy()
        big_study["circle_type"] = "circle_type=N"
        expanded_outputs = pd.concat(
            [pd.DataFrame(big_study).T] * div, ignore_index=True
        )
        outputs = outputs.append(expanded_outputs)

    if modulo > 0:
        df_study["circle_type"] = "circle_type=n"
        expanded_outputs = pd.concat(
            [pd.DataFrame(df_study).T] * modulo, ignore_index=True
        )
        outputs = outputs.append(expanded_outputs)

    return outputs
