"""pkdb_analysis - Python interface for PK-DB."""
from pkdb_analysis.data import PKData
from pkdb_analysis.query import PKDB, PKFilter
from pkdb_analysis.query import query_pkdb_data
from pkdb_analysis.utils import show_versions


__version__ = "0.2.2"


from pathlib import Path

RESOURCES_PATH = Path(__file__).parent / "resources"  # directory of test files
TESTDATA_PATH = RESOURCES_PATH / "testdata"  # directory of data for tests

# downloaded test data using concise True/False (filter endpoint)
TESTDATA_CONCISE_TRUE_ZIP = TESTDATA_PATH / "testdata_concise_true.zip"
TESTDATA_CONCISE_FALSE_ZIP = TESTDATA_PATH / "testdata_concise_false.zip"
