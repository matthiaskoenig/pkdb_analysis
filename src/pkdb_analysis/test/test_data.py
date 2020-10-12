import pytest

from pkdb_analysis import PKDB, PKData
from pkdb_analysis.test import TESTDATA_CONCISE_FALSE_ZIP, TESTDATA_CONCISE_TRUE_ZIP


def test_concise_pks():
    """Test if the pks of the concise=True/False data are identical."""
    d1 = PKData.from_archive(path=TESTDATA_CONCISE_TRUE_ZIP)
    d1 = PKDB._intervention_pk_update(d1)

    d2 = PKData.from_archive(path=TESTDATA_CONCISE_FALSE_ZIP)
    d2 = PKDB._intervention_pk_update(d2)
    d2._concise()

    assert d1.studies.pks == d2.studies.pks
    assert d1.groups.pks == d2.groups.pks
    assert d1.individuals.pks == d2.individuals.pks
    assert d1.interventions.pks == d2.interventions.pks
    assert d1.outputs.pks == d2.outputs.pks
    assert d1.timecourses.pks == d2.timecourses.pks
    assert d1.scatters.pks == d2.scatters.pks
