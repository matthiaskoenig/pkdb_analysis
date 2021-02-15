import os

from pkdb_analysis import PKDB, PKFilter


os.environ["API_BASE"] = "http://localhost:8000/api/v1"


def test_pkfilter():
    creator_username = "yduport"
    pkfilter = PKFilter()
    pkfilter.studies = {"creator": creator_username}
    pkdata = PKDB.query(pkfilter)
    assert all(pkdata.studies.creator == creator_username)


def test_quer_infonodes():
    info_nodes = PKDB.query_info_nodes_sids()
    print(info_nodes)
