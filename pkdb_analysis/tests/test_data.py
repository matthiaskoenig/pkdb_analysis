import pytest
from pkdb_analysis.data import PKDBData
import pandas as pd


def _check_data(data):
    assert data

    for key in ["interventions", "characteristica", "outputs", "timecourses"]:
        df = getattr(data, key)

        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "study_sid" in df


def test_all_data():
    """ Test database requests."""
    data = PKDBData.from_db(filter=None)
    _check_data(data)


def test_data_hdf5(tmp_path):
    """ Test HDF io"""
    data = PKDBData.from_db(filter=None)

    h5_path = tmp_path / "test.h5"
    data.to_hdf5(h5_path)
    data2 = PKDBData.from_hdf5(h5_path)
    _check_data(data2)

    for key in ["interventions", "characteristica", "outputs", "timecourses"]:
        assert len(getattr(data, key)) == len(getattr(data2, key))
