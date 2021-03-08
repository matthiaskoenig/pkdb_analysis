"""Definition of data and files for the tests.

The files are located in the data directory.
"""
from pathlib import Path

TEST_PATH = Path(__file__).parent  # directory of test files

TESTDATA_PATH = TEST_PATH / "data"  # directory of data for tests

# downloaded test data using concise True/False (filter endpoint)
TESTDATA_CONCISE_TRUE_ZIP = TESTDATA_PATH / "testdata_concise_true.zip"
TESTDATA_CONCISE_FALSE_ZIP = TESTDATA_PATH / "testdata_concise_false.zip"
