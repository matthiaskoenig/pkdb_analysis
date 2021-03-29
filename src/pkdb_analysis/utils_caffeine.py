"""Caffeine specific utility functions."""

INTERVENTION_FIELDS = ["substance", "value", "unit", "route", "form", "application"]


def one_intervention(d):
    if len(d) == 1:
        return d


def validate_1len(d):
    assert 1 == len(d[d]), d
    return d
