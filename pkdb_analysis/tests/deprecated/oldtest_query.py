import pandas as pd
import pytest
import requests

from pkdb_analysis import PKFilterFactory
from pkdb_analysis.data import PKData
from pkdb_analysis.envs import USER, PASSWORD, API_BASE
from pkdb_analysis.query import PKDB


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


def is_admin_and_connection():
    if USER == "admin":
        try:
            PKDB.get_authentication_headers(API_BASE, USER, PASSWORD)
            return False
        except requests.exceptions.InvalidURL:
            return True
    return True


@pytest.mark.skipif(is_admin_and_connection(), reason="Database not running or not admin user.")
def test_data_by_study_name():
    # check existing study
    pkfilter = PKFilterFactory.by_study_name("Test1")
    data = PKDB.query(pkfilter=pkfilter)
    _check_data(data)

    for key in PKData.KEYS:
        df = getattr(data, key)
        study_names = df.study_name.unique()
        assert len(study_names) == 1
        assert "Test1" in study_names


@pytest.mark.skipif(is_admin_and_connection(), reason="Database not running or not admin user.")
def test_data_by_study_name_empty():
    # check non-existing study
    pkfilter = PKFilterFactory.by_study_name("xyzfasdfs")
    data = PKDB.query(pkfilter=pkfilter)
    _check_data_empty(data)


@pytest.mark.skipif(is_admin_and_connection(), reason="Database not running or not admin user.")
def test_data_by_study_sid():
    # check existing study
    pkfilter = PKFilterFactory.by_study_sid("Test1")
    data = PKDB.query(pkfilter=pkfilter)

    _check_data(data)

    for key in PKData.KEYS:
        df = getattr(data, key)
        study_sids = df.study_sid.unique()
        assert len(study_sids) == 1
        assert "Test1" in study_sids


@pytest.mark.skipif(is_admin_and_connection(), reason="Database not running or not admin user.")
def test_data_by_study_sid_empty():
    # check non-existing study
    pkfilter = PKFilterFactory.by_study_sid("xyzfasdfs")
    data = PKDB.query(pkfilter=pkfilter)
    _check_data_empty(data)


@pytest.mark.skipif(is_admin_and_connection(), reason="Database not running or not admin user.")
def test_data_hdf5(tmp_path):
    """ Test HDF io"""
    data = PKDB.query()

    h5_path = tmp_path / "test.h5"
    data.to_hdf5(h5_path)
    data2 = PKData.from_hdf5(h5_path)
    _check_data(data2)

    for key in PKData.KEYS:
        assert len(getattr(data, key)) == len(getattr(data2, key))


@pytest.mark.skipif(is_admin_and_connection(), reason="Database not running or not admin user.")
def test_data_counts():
    pkfilter = PKFilterFactory.by_study_name("Test1")
    data = PKDB.query(pkfilter=pkfilter)
    assert data.groups_count == 1
    assert data.individuals_count == 6
    assert data.interventions_count == 3
    assert data.outputs_count == 105
    assert data.timecourses_count == 2


@pytest.mark.skipif(is_admin_and_connection(), reason="Database not running or not admin user.")
def test_data_mi():
    pkfilter = PKFilterFactory.by_study_name("Test1")
    data = PKDB.query(pkfilter=pkfilter)
    for field in PKData.KEYS:
        print(field)
        df = getattr(data, f"{field}_mi")
        assert df is not None
        assert not df.empty
        # number of entries should not change
        assert len(df) == len(getattr(data, f"{field}"))

@pytest.mark.skipif(is_admin_and_connection(), reason="Database not running or not admin user.")
def test_data_test1():
    # check non-existing study
    pkfilter = PKFilterFactory.by_study_name("Test1")
    data = PKDB.query(pkfilter=pkfilter)
    _check_data(data)

    assert len(data.groups) == 6
