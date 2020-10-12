from pkdb_analysis import PKDB, PKData
from pkdb_analysis.test import TESTDATA_CONCISE_FALSE_ZIP


def test_read_from_archive():
    """Test reading from archive."""
    pkdata = PKData.from_archive(path=TESTDATA_CONCISE_FALSE_ZIP)
    pkdata = PKDB._intervention_pk_update(pkdata)
    assert pkdata
