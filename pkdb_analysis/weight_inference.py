import numpy as np
import pandas as pd
import pint

ureg = pint.UnitRegistry()


def infer_output(d):
    d = d.copy()
    if len(d) > 0:
        u_unit = ureg(d["unit"])
        u_unit_weight = ureg(d["unit_weight"])

        if not np.isnan(d["value_weight"]):
            weight = d["value_weight"]
        elif not np.isnan(d["mean_weight"]):
            weight = d["mean_weight"]

        elif not np.isnan(d["median_weight"]):
            weight = d["median_weight"]
        else:
            return pd.Series(None, index=d.index)
        assert weight is not None, d

        if d["per_bodyweight"]:
            exponent = 1
        else:
            exponent = -1

        if d["group_pk"] == -1:
            if weight:
                result = d["value"] * u_unit * ((weight * u_unit_weight) ** exponent)
                d["value"] = result.m
                d["unit"] = str(result.u)
                d["inferred"] = True
                d["per_bodyweight"] = not d["per_bodyweight"]
                return d
        else:

            if weight:
                result = u_unit * ((d["mean_weight"] * u_unit_weight) ** exponent)
                for key in ["mean","median","min", "max", "sd", "se", "sd"]:
                    if d[key] is not None:
                        d[key] = result.m * d[key]


                d["unit"] = str(result.u)
                d["inferred"] = True
                d["per_bodyweight"] = not d["per_bodyweight"]
                return d
    return pd.Series(None, index=d.index)


def infer_intervention(d):
    d = d.copy()

    u_unit_intervention = ureg(d["unit_intervention"])

    if not np.isnan(d["value_weight"]):
        weight = d["value_weight"]
    elif not np.isnan(d["mean_weight"]):
        weight = d["mean_weight"]

    else:
        return pd.Series(None, index=d.index)

    u_unit_weight = ureg(d["unit_weight"])
    assert weight is not None, d

    if d["per_bodyweight_intervention"]:
        exponent = 1
    else:
        exponent = -1

    if d["group_pk"] == -1:
        if weight:
            result = d["value_intervention"] * u_unit_intervention * ((weight * u_unit_weight) ** exponent)
            d["value_intervention"] = result.m
            d["unit_intervention"] = str(result.u)
            d["inferred"] = True
            d["per_bodyweight_intervention"] = not d["per_bodyweight_intervention"]
            return d
    else:
        if weight:
            result = d["value_intervention"] * u_unit_intervention * ((weight * u_unit_weight) ** exponent)
            d["value_intervention"] = result.m
            d["unit_intervention"] = str(result.u)
            d["inferred"] = True
            d["per_bodyweight_intervention"] = not d["per_bodyweight_intervention"]
            return d


def infer_weight(d):
    result_bodyweight = d.dropna(subset=["unit_weight"])
    result_no_bodyweight = d[d["unit_weight"].isnull()]

    result_infer_outputs = result_bodyweight.apply(infer_output, axis="columns").dropna(how="all")

    result_infer = result_bodyweight.append(result_infer_outputs, ignore_index=True)

    result_infer_outputs = result_infer.apply(infer_intervention, axis="columns").dropna(how="all")



    result_infer = result_infer.append(result_infer_outputs, ignore_index=True)
    result_infer = result_infer.append(result_no_bodyweight, ignore_index=True)
    return result_infer
