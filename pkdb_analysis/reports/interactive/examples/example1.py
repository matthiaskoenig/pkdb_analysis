"""
This script creates an interactive pharmacokinetics plot.
"""
import pandas as pd
from pathlib import Path

from pkdb_analysis.filter import f_smoking, f_n_smoking, f_n_oc, f_effective_n_oc, f_oc
from pkdb_analysis.reports.interactive.interactive import interactive_plot_factory, PlottingParameter as PP, LegendArgs as LA
from pkdb_analysis import PKData

from pkdb_analysis.tests import TEST_HDF5


# substances used in the interventions
INTERVENTION_SUBSTANCES = {"caffeine"}

# substances measured in the outputs
OUTPUT_SUBSTANCES = {"caffeine"}

# create plotting categories
PLOTTING_CATEGORIES = [
    PP(["auc_end"], []),
    PP(["auc_inf"], []),
    PP(["vd"], []),
    PP(["thalf"], [], infer_by_output=False),
    PP(["clearance"], ['milliliter / meter ** 2 / minute']),
    PP(["cmax"], [], infer_by_output=False),
    PP(["kel"], []),
    PP(["tmax"], [], infer_by_output=False),
    PP(["vd"], []),
]

# Change formating on specific values in specific columns
REPLACEMENTS = {
    "sex": {"NR": "not reported"},
    "intervention_route": {"iv": "intravenous"},
}

# The url which will be used to href on click.
URL = "https://develop.pk-db.com"

# The name and key of the column which has categories. The categories can be clicked on an interactive legend.
# The categories cannot be color coded.
MULTI_LEGEND = {"Study": "study_name"}
# The name and key of the column which has categories. The categories can be clicked on an interactive legend.
# The categories can be color coded.

MULTI_COLOR_LEGEND = {
    "Data type": LA("data_type"),
    "Outlier": LA("outlier", [False, ]),
    "Sex": LA("sex"),
    "Healthy": LA("healthy", [True], ),
    "Lifestyle": LA("life_style", ),
    "Administration route": LA("intervention_route"),
    "Number of interventions": LA("intervention_number", [1, ]),
    "Tissue": LA("tissue"),

}
# Information shown on hover.
TOOLTIP = [
    'study_sid:N',
    'study_name:N',
    "url:N",
    'output_pk:N',
    "group_name:N",
    "individual_name:N",
    'intervention_value:Q',
    'y:Q',
    "intervention_names:N",
    "intervention_number:Q",
    "weight:Q",
    "unit_weight:N",
    "sex:N",
]


def outlier_studies(df):
    outlier_study_names = ["Balogh1992", "Harder1988", "Harder1988", "Stille1987"]
    if df.study_name in outlier_study_names:
        return True
    else:
        return False


def lifestyle(df):
    if not df.extra[f_smoking].empty and df.extra[f_n_smoking].empty:
        return "smoking"
    elif not df.extra[f_oc].empty and df.extra[f_n_oc].empty:
        return "oral contraceptive"
    elif not df.extra[f_n_smoking].empty and not df.extra[f_effective_n_oc].empty:
        return "control"
    else:
        return "unknown"


def intervention_names(df):
    """calculates a column with a information on all applied intervention names.
    This is information is displayed on hover."""

    if isinstance(df.intervention_extra, pd.DataFrame):
        return " | ".join(df.intervention_extra["name"])
    else:
        print(df.intervention_extra)


# column name and function on how the column name is calculated.
# The column names can be used e.g. as colored multi legends.
ADDITIONAL_INFORMATION = {
    "intervention_names": intervention_names,
    "outlier": outlier_studies,
    "life_style": lifestyle,
}


def create_plots(path):
    pkdata = PKData.from_hdf5(TEST_HDF5)

    kwargs = {
        "plotting_categories": PLOTTING_CATEGORIES,
        "intervention_substances": INTERVENTION_SUBSTANCES,
        "output_substances": OUTPUT_SUBSTANCES,
        "exclude_study_names": [],
        "additional_information": ADDITIONAL_INFORMATION,
        "multi_color_legend": MULTI_COLOR_LEGEND,
        "tooltip": TOOLTIP,
        "multi_legend": MULTI_LEGEND,
        "url": URL,
        "create_json": True,
        "replacements": REPLACEMENTS,
    }

    interactive_plot_factory(pkdata, path=path, **kwargs)


if __name__ == "__main__":
    # !Delete the output after running!
    output_path = Path(__file__).parent / "results"
    #if not output_path.exists():
    #    output_path.mkdir()
    create_plots(path=output_path)
