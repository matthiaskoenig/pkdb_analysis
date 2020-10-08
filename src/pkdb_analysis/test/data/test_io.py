from pkdb_analysis import PKData, PKDB
from pkdb_analysis.test import TEST_ZIP


if __name__ == "__main__":
    pkdata = PKData.from_archive(path=TEST_ZIP)
    pkdata = PKDB._intervention_pk_update(pkdata)
