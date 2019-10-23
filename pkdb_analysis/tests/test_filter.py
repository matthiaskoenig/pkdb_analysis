import pytest
from pkdb_analysis.filter import Filter, FilterFactory


def test_empty_filter():
    filter = Filter(normed=None)

    assert len(filter.groups) == 0
    assert len(filter.individuals) == 0
    assert len(filter.interventions) == 0
    assert len(filter.outputs) == 0
    assert len(filter.timecourses) == 0

    d = filter.to_dict()
    assert isinstance(d, dict)
    for filter_key in Filter.KEYS:
        assert filter_key in d


def test_study_sid_filter():
    filter = FilterFactory.by_study_sid("PKDB00181")
    assert isinstance(filter, Filter)
    d = filter.to_dict()
    for filter_key in Filter.KEYS:
        assert filter_key in d
        assert "study_sid" in d[filter_key]
        assert d[filter_key]["study_sid"] == "PKDB00181"


def test_study_name_filter():
    filter = FilterFactory.by_study_name("Allonen1981")
    assert isinstance(filter, Filter)
    d = filter.to_dict()
    for filter_key in Filter.KEYS:
        assert filter_key in d
        assert "study_name" in d[filter_key]
        assert d[filter_key]["study_name"] == "Allonen1981"
