"""
Definition of data and files for the tests.
The files are located in the data directory.
"""
from pathlib import Path

TEST_PATH = Path(__file__).parent  # directory of test files
TESTDATA_PATH = TEST_PATH / 'data'  # directory of data for tests
TEST_HDF5 = TESTDATA_PATH / "test.h5"
