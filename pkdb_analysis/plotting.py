TEST_STUDY_NAMES = ["Test1", "Test2", "Test3", "Test4"]
from pkdb_analysis.data import PKData

def exclude_tests(data: PKData):
    return data.exclude_intervention(lambda d: d["study_name"].isin(TEST_STUDY_NAMES))