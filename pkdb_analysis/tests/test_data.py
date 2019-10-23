import pytest
from pkdb_analysis.data import PKData
from pkdb_analysis.pkfilter import PKFilter, PKFilterFactory
import pandas as pd


def _check_data(data):
    assert data

    for key in ["groups", "individuals", "interventions", "outputs", "timecourses"]:
        df = getattr(data, key)

        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "study_sid" in df


def _check_data_empty(data):
    assert data

    for key in ["groups", "individuals", "interventions", "outputs", "timecourses"]:
        df = getattr(data, key)

        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
        assert "study_sid" not in df


def test_data_by_study_name():
    # check existing study
    pkfilter = PKFilterFactory.by_study_name("Test1")
    data = PKData.from_db(pkfilter=pkfilter)
    _check_data(data)

    for key in PKData.KEYS:
        df = getattr(data, key)
        study_names = df.study_name.unique()
        assert len(study_names) == 1
        assert "Test1" in study_names


def test_data_by_study_name_empty():
    # check non-existing study
    pkfilter = PKFilterFactory.by_study_name("xyzfasdfs")
    data = PKData.from_db(pkfilter=pkfilter)
    _check_data_empty(data)


def test_data_by_study_sid():
    # check existing study
    pkfilter = PKFilterFactory.by_study_sid("PKDB99999")
    data = PKData.from_db(pkfilter=pkfilter)

    _check_data(data)

    for key in PKData.KEYS:
        df = getattr(data, key)
        study_sids = df.study_sid.unique()
        assert len(study_sids) == 1
        assert "PKDB99999" in study_sids


def test_data_by_study_sid_empty():
    # check non-existing study
    pkfilter = PKFilterFactory.by_study_sid("xyzfasdfs")
    data = PKData.from_db(pkfilter=pkfilter)
    _check_data_empty(data)


def test_data_hdf5(tmp_path):
    """ Test HDF io"""
    data = PKData.from_db()

    h5_path = tmp_path / "test.h5"
    data.to_hdf5(h5_path)
    data2 = PKData.from_hdf5(h5_path)
    _check_data(data2)

    for key in PKData.KEYS:
        assert len(getattr(data, key)) == len(getattr(data2, key))



def test_data_test1():
    # check non-existing study
    pkfilter = PKFilterFactory.by_study_name("Test1")
    data = PKData.from_db(pkfilter=pkfilter)
    _check_data(data)

    assert len(data.groups) == 6
