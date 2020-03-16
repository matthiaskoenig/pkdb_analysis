"""
Creates test data
"""
from pkdb_analysis import PKData, PKFilter
from pkdb_analysis.query import PKDB


def load_test_studies():
    """ loads test studies from database. Make sure test studies are uploaded to database.
        """

    test_study_names = ["Test1", "Test2", "Test3", "Test4"]
    url_study_names = "__".join(test_study_names)
    pkfilter = PKFilter()
    for df_key in ["groups", "individuals", "interventions", "outputs", "timecourses"]:
        setattr(pkfilter, df_key, {"study_name__in": url_study_names})
    return PKDB.query(pkfilter=pkfilter)


if __name__ == "__main__":
    from pathlib import Path

    data = load_test_studies()
    data._concise()
    print(data)
    h5_path = Path(".") / "data" / "test.h5"
    data.to_hdf5(h5_path)
