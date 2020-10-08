import pytest
from pkdb_analysis import PKData, PKDB
from pkdb_analysis.test import TEST_ZIP, TEST_CONCISED_ZIP


def test_concise():
    pkdata = PKData.from_archive(path=TEST_ZIP)
    pkdata = PKDB._intervention_pk_update(pkdata)

    pkdata_concise = pkdata.copy()
    pkdata_concise._concise()

    pkdata_import_concise = PKData.from_archive(path=TEST_CONCISED_ZIP)
    pkdata_import_concise = PKDB._intervention_pk_update(pkdata_import_concise)

    assert not pkdata_import_concise.timecourses.pks.symmetric_difference(pkdata_concise.timecourses.pks)
    assert not pkdata_import_concise.outputs.pks.symmetric_difference(pkdata_concise.outputs.pks)
    assert not pkdata_import_concise.individuals.pks.symmetric_difference(pkdata_concise.individuals.pks)
    assert not pkdata_import_concise.groups.pks.symmetric_difference(pkdata_concise.groups.pks)
    assert not pkdata_import_concise.studies.pks.symmetric_difference(pkdata_concise.studies.pks)







