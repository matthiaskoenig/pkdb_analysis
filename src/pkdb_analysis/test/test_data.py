import pytest

from pkdb_analysis import PKData
from pkdb_analysis.test import TESTDATA_CONCISE_FALSE_ZIP, TESTDATA_CONCISE_TRUE_ZIP


def test_zips():
    """Test if the pks of remote concise=True/False are different."""
    d1 = PKData.from_archive(path=TESTDATA_CONCISE_TRUE_ZIP)
    d2 = PKData.from_archive(path=TESTDATA_CONCISE_FALSE_ZIP)

    assert d1.groups.pks != d2.groups.pks
    assert d1.individuals.pks != d2.individuals.pks


def test_concise_pks_1():
    """Test if the pks of local concise=True/False are different."""
    d1 = PKData.from_archive(path=TESTDATA_CONCISE_FALSE_ZIP)
    d2 = d1.copy()
    d2._concise()

    assert d1.groups.pks != d2.groups.pks
    assert d1.individuals.pks != d2.individuals.pks


def test_concise_pks_2():
    """Test concise has no effect on concised data."""
    d1 = PKData.from_archive(path=TESTDATA_CONCISE_TRUE_ZIP)
    d2 = d1.copy()
    d2._concise()

    assert d1.studies.pks == d2.studies.pks
    assert d1.groups.pks == d2.groups.pks
    assert d1.individuals.pks == d2.individuals.pks
    assert d1.interventions.pks == d2.interventions.pks
    assert d1.outputs.pks == d2.outputs.pks
    assert d1.timecourses.pks == d2.timecourses.pks


def test_concise_pks_3():
    """Test if the pks of the concise=True/False data are identical."""
    d1 = PKData.from_archive(path=TESTDATA_CONCISE_TRUE_ZIP)
    d2 = PKData.from_archive(path=TESTDATA_CONCISE_FALSE_ZIP)
    d2._concise()

    assert d1.studies.pks == d2.studies.pks
    assert d1.groups.pks == d2.groups.pks
    assert d1.individuals.pks == d2.individuals.pks
    assert d1.interventions.pks == d2.interventions.pks
    assert d1.outputs.pks == d2.outputs.pks
    assert d1.timecourses.pks == d2.timecourses.pks
    # assert d1.scatters.pks == d2.scatters.pks
