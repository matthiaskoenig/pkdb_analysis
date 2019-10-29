import pytest
from pkdb_analysis.data import PKData
from pathlib import Path


def _load_test_data():
    h5_path = Path(".") / "test.h5"
    return PKData.from_hdf5(h5_path)

def test_sids():
    # check non-existing study
    data = _load_test_data()
    assert len(data.study_sids) == 4


