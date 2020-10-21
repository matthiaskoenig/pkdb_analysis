from pkdb_analysis import PKFilter, PKDB


def test_pkfilter():
    creator_username = "yduport"
    pkfilter = PKFilter()
    pkfilter.studies = {"creator": creator_username}
    pkdata = PKDB.query_(pkfilter)
    assert all(pkdata.studies.creator == creator_username)
