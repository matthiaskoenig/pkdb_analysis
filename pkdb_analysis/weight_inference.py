
import pint
import numpy as np
ureg = pint.UnitRegistry()


def infer_output(d):
    d = d.copy()
    u_unit = ureg(d["unit"])
    u_unit_weight = ureg(d["unit_weight"])

    if not np.isnan(d["value_weight"]):
        weight = d["value_weight"]
    elif not np.isnan(d["mean_weight"]):
        weight = d["mean_weight"]
    else:
        return None

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
        # if d["study_name"] == "Murphy1988":
        #    print(d)
        if weight:
            result = u_unit * ((d["mean_weight"] * u_unit_weight) ** exponent)
            d["mean"] = result.m * d["mean"]
            d["sd"] = result.m * d["sd"]
            d["se"] = result.m * d["se"]
            d["cv"] = result.m * d["cv"]

            d["unit"] = str(result.u)
            d["inferred"] = True
            d["per_bodyweight"] = not d["per_bodyweight"]
            return d


def infer_intervention(d):
    d = d.copy()

    u_unit_intervention = ureg(d["unit_intervention"])

    if not np.isnan(d["value_weight"]):
        weight = d["value_weight"]
    elif not np.isnan(d["mean_weight"]):
        weight = d["mean_weight"]

    else:
        return None

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