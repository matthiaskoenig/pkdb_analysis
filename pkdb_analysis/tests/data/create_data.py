"""
Creates test data
"""

from pkdb_analysis import PKData, PKFilter
from pkdb_analysis.query import PKDB


def load_test_studies() -> PKData:
    """ Loads test studies from database.

    Ensure test studies are uploaded to database before running this script.
    """
    test_study_names = ["Test1", "Test2", "Test3", "Test4"]
    url_study_names = "__".join(test_study_names)
    pkfilter = PKFilter()
    for df_key in ["groups", "individuals", "interventions", "outputs", "timecourses"]:
        setattr(pkfilter, df_key, {"study_name__in": url_study_names})
    return PKDB.query(pkfilter=pkfilter)


if __name__ == "__main__":
    from pkdb_analysis.tests import TEST_HDF5
    pkdata = load_test_studies()
    pkdata._concise()
    pkdata.to_hdf5(TEST_HDF5)
