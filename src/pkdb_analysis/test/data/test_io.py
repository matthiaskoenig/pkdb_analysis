from pkdb_analysis import PKData
from pkdb_analysis.test import TESTDATA_CONCISE_FALSE_ZIP, TESTDATA_PATH


def test_read_from_archive():
    """Test reading from archive."""
    pkdata = PKData.from_archive(path=TESTDATA_CONCISE_FALSE_ZIP)
    assert pkdata

def test_write_to_archive(tmp_path):
    """Test writing to archive from archive."""
    pkdata = PKData.from_archive(path=TESTDATA_CONCISE_FALSE_ZIP)
    pkdata.to_archive(path=tmp_path / "test.zip")
    pkdata_loaded = PKData.from_archive(path=tmp_path / "test.zip")
    assert pkdata_loaded

def test_write_to_hdf5():
    """Test reading from archive."""
    assert pkdata
