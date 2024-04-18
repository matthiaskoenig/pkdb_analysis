from pathlib import Path

import pytest

from pkdb_analysis import PKData
from pkdb_analysis.test import TESTDATA_CONCISE_FALSE_ZIP, TESTDATA_CONCISE_TRUE_ZIP


def test_read_from_archive() -> None:
    """Test reading from archive."""
    pkdata = PKData.from_archive(path=TESTDATA_CONCISE_FALSE_ZIP)
    assert pkdata


def test_write_to_archive(tmp_path: Path) -> None:
    """Test writing to archive from archive."""
    pkdata = PKData.from_archive(path=TESTDATA_CONCISE_FALSE_ZIP)
    pkdata.to_archive(path=tmp_path / "test.zip")
    pkdata_loaded = PKData.from_archive(path=tmp_path / "test.zip")
    assert pkdata_loaded


@pytest.mark.parametrize(
    "input_path", [TESTDATA_CONCISE_FALSE_ZIP, TESTDATA_CONCISE_TRUE_ZIP]
)
def test_h5(input_path: Path, tmp_path: Path) -> None:
    """Test conversion to HDF5."""
    pkdata = PKData.from_archive(path=input_path)
    pkdata.to_hdf5(tmp_path / "test.h5")
