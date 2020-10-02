from pathlib import Path

from pkdb_analysis.query import query_pkdb_data
from pkdb_analysis.test import TEST_HDF5


def create_h5_test_data(h5_path: Path = TEST_HDF5) -> None:
    """ Loads test studies from database.

    Ensure test studies are uploaded to database before running this script.
        ./pkdb_data/management/upload_studies.py tests

    :param h5_path: HDF5 path for storage
    """
    test_study_names = ["Test1", "Test2", "Test3", "Test4"]
    pkdata = query_pkdb_data(h5_path=h5_path, study_names=test_study_names)

    # FIXME: https://github.com/matthiaskoenig/pkdb_analysis/issues/25
    # print(pkdata.studies)
    # assert len(pkdata.studies) == len(test_study_names)
    print(pkdata.interventions)
    pkdata.to_hdf5(h5_path)


if __name__ == "__main__":
    create_h5_test_data(h5_path=TEST_HDF5)
