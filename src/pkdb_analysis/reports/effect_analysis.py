from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from pkdb_analysis import PKData
from pkdb_analysis.meta_analysis import MetaAnalysis


class OutputPair(object):
    def __init__(
        self,
        category: str,
        control: PKData,
        investigate: PKData,
        control_value: str = "value",
        investigate_value: str = "value",
    ):
        self.category = category
        self.control = control
        self.investigate = investigate
        self.validate_pkdata()

    def validate_pkdata(self):
        if len(set(self.control.outputs.group_pk)) > 2:
            raise ValueError("Only one control group is allowed.")
        if len(set(self.investigate.outputs.group_pk)) > 2:
            raise ValueError("Only one investigate group is allowed.")

    @staticmethod
    def get_statistics(pkdata: PKData):
        number_individuals = len(pkdata.individuals.pks)
        number_groups = len(pkdata.groups.pks)

        if number_individuals > 0 and number_groups > 0:
            raise ValueError("One group or individuals are allowed not both.")

        if number_individuals == 0 and number_groups == 0:
            raise ValueError("Empty data not allowed.")

        if number_individuals > 0:
            count = number_individuals
            average = pkdata.outputs["value"].mean()
            sd = pkdata.outputs["value"].std()

        elif number_groups > 0:
            count = pkdata.groups.iloc[0].group_count
            average = get_value(pkdata.outputs.iloc[0])
            sd = pkdata.outputs.iloc[0]["sd"]
        return count, average, sd

    @staticmethod
    def esc_mean_sd(
        count_1: float,
        count_2: float,
        mean_1: float,
        mean_2: float,
        sd_1: float,
        sd_2: float,
    ) -> pd.Series:
        """To calculate Hedges’ g from the Mean, Standard Deviation, and counts of both trial arms
        ( adopted from r package https://github.com/strengejacke/esc/tree/eba3c6a62875d9c894466012fe82c0d2253e6137).
        """

        total_n = count_2 + count_1
        mean_diff = mean_2 - mean_1

        pooled_sd = np.sqrt(
            (((count_1 - 1) * sd_1 ** 2) + ((count_2 - 1) * sd_2 ** 2))
            / (count_1 + count_2 - 2)
        )

        es = mean_diff / pooled_sd

        variance_1 = total_n / (count_2 * count_1)
        variance_2 = es ** 2 / (2 * (count_2 + count_1))
        variance = variance_1 + variance_2
        return pd.Series(
            {
                "pooled_sd": pooled_sd,  # of output
                "variance": variance,  # of effect size
                "se": np.sqrt(variance),  # of effect size
                "weight": 1 / variance,
                "es": es,  # effect size
                "hedges_g": es * (1 - 3 / (4 * (total_n) - 9)),
            }
        )

    def pair_statistics(self) -> Dict:
        """"""

        control_count, control_mean, control_sd = self.get_statistics(self.control)
        investigate_count, investigate_mean, investigate_sd = self.get_statistics(
            self.investigate
        )
        pair_statistics = self.esc_mean_sd(
            control_count,
            investigate_count,
            control_mean,
            investigate_mean,
            control_sd,
            investigate_sd,
        )
        return {
            "study": self.control.outputs.iloc[0]["study_name"],
            "category": self.category,
            "control_count": control_count,
            "control_mean": control_mean,
            "control_sd": control_sd,
            "investigate_count": investigate_count,
            "investigate_mean": investigate_mean,
            "investigate_sd": investigate_sd,
            **pair_statistics,
        }


def fixed_effect(df: pd.DataFrame, effect_size: str, variance: str) -> Dict:
    weights = 1 / df[variance]
    fixed_effect_variance = 1 / np.sum(weights)

    return {
        "fixed_effect_variance": fixed_effect_variance,
        "fixed_effect_se": np.sqrt(fixed_effect_variance),
        "fixed_effect_weighted_mean": np.sum(weights * df[effect_size])
        / np.sum(weights),
    }


def random_effects(df: pd.DataFrame, effect_size: str, variance: str) -> Dict:
    fe_statistics = fixed_effect(df, effect_size, variance)
    weights = 1 / df[variance]

    q = np.sum(weights * (df[effect_size]) ** 2) - (
        np.sum(weights * df[effect_size])
    ) ** 2 / np.sum(weights)
    c = np.sum(weights) - (np.sum(weights ** 2) / np.sum(weights))

    df_ = len(df) - 1
    if q > df_ and c != 0:
        between_studies_variance = (q - df_) / c
    else:
        between_studies_variance = 0

    weights_random_effects = 1 / (df[variance] + between_studies_variance)
    weighted_mean_random_effects_denominator = np.sum(
        weights_random_effects * df[effect_size]
    )
    weighted_mean_random_effects_nominator = np.sum(weights_random_effects)
    weighted_mean_random_effects = (
        weighted_mean_random_effects_denominator
        / weighted_mean_random_effects_nominator
    )
    variance_random_effects = 1 / weighted_mean_random_effects_nominator
    sd_random_effects = np.sqrt(variance_random_effects)

    return {
        **fe_statistics,
        "random_effects_weighted_mean": weighted_mean_random_effects,
        "random_effects_variance": variance_random_effects,
        "random_effects_sd": sd_random_effects,
    }


def between_studies_statistics(df, on):
    df_result = pd.DataFrame()
    for category, category_df in df.groupby([on]):
        random_effects_result = random_effects(category_df, "hedges_g", "variance")
        df_result = df_result.append(
            {"category": category, **random_effects_result}, ignore_index=True
        )
    return df_result


def get_value(series: pd.Series) -> float:
    for key in ["mean", "median"]:
        if pd.notnull(series[key]):
            return series[key]
    assert False, f"mean or median, one of the fields must not be null.{series}"


def errorbars(output_pairs: List[OutputPair]):
    df = pd.DataFrame([output_pair.pair_statistics() for output_pair in output_pairs])
    df_statistics = between_studies_statistics(df, on="category")

    fig, ax = plt.subplots()
    for row, studies_statistics in df_statistics.iterrows():
        ax.errorbar(
            y=row,
            x=studies_statistics["random_effects_weighted_mean"],
            xerr=studies_statistics["random_effects_sd"],
        )
    ax.set_yticks(np.arange(len(df_statistics["category"])))
    ax.set_yticklabels(tuple(df_statistics["category"]))

    plt.show()
