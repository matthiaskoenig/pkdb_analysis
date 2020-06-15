from pkdb_analysis.data import PKData
from pkdb_analysis.tests import TEST_HDF5


def _load_test_data():
    return PKData.from_hdf5(TEST_HDF5)


def test_sids():
    # check number of studies
    data = _load_test_data()
    assert len(data.study_sids) == 4


def test_intervention_filter():
    data = _load_test_data()

    def dosing_and_caffeine(d):
        return (d["measurement_type"] == "dosing") & (d["substance"] == "caffeine")

    test_data = data.filter_individual(dosing_and_caffeine)
    # check non-existing study
    assert len(test_data.study_sids) == 3

    test_data_not_concise = data.filter_individual(dosing_and_caffeine, concise=False)
    assert len(test_data_not_concise.study_sids) == 4


def test_output_filter():
    data = _load_test_data()

    def is_auc_inf(d):
        return d["measurement_type"] == "auc_inf"

    test_data = data.filter_output(is_auc_inf)
    measurement_types = test_data.outputs["measurement_type"].unique()
    assert len(measurement_types) == 1
    assert measurement_types[0] == "auc_inf"
    assert len(test_data.timecourses) > 0

    test_data = data.filter_output(is_auc_inf).delete_timecourses()
    measurement_types = test_data.outputs["measurement_type"].unique()
    assert len(measurement_types) == 1
    assert measurement_types[0] == "auc_inf"
    assert len(test_data.timecourses) == 0


def test_timecourses_filter():
    data = _load_test_data()

    def is_caffeine(d):
        return d["substance"] == "caffeine"

    test_data = data.filter_timecourse(is_caffeine)
    substances = test_data.timecourses["substance"].unique()
    assert len(substances) == 1
    assert substances[0] == "caffeine"
    assert len(test_data.timecourses) > 0

    test_data = data.filter_timecourse(is_caffeine).delete_outputs()
    substances = test_data.timecourses["substance"].unique()
    assert len(substances) == 1
    assert substances[0] == "caffeine"
    assert len(test_data.outputs) == 0


def test_subject_filter():
    data = _load_test_data()

    def smoking(d):
        return d["measurement_type"] == "smoking"

    def healthy(d):
        return d["measurement_type"] == "healthy"

    def choice_y(d):
        return d["choice"] == "Y"

    def is_healthy(d):
        return healthy(d) & choice_y(d)

    def smoker_n(d):
        return smoking(d) & (d["choice"] == "N")

    healthy_smoker_n_data = data.filter_subject([is_healthy, smoker_n])
    individual_smoking_choices = healthy_smoker_n_data.individuals[smoking].choice.unique()
    group_smoking_choices = healthy_smoker_n_data.groups[smoking].choice.unique()

    assert "N" in individual_smoking_choices
    assert "N" in group_smoking_choices

    individual_healthy_choices = healthy_smoker_n_data.individuals[healthy].choice.unique()
    group_healthy_choices = healthy_smoker_n_data.groups[healthy].choice.unique()

    assert "Y" in individual_healthy_choices
    assert "Y" in group_healthy_choices


def test_subject_exclude():
    data = _load_test_data()

    def smoking(d):
        return d["measurement_type"] == "smoking"

    def smoker_y(d):
        return smoking(d) & (d["choice"] == "Y")

    exclude_smoker_data = data.exclude_subject(smoker_y)

    individual_smoking_choices = exclude_smoker_data.individuals[smoking].choice.unique()
    group_smoking_choices = exclude_smoker_data.groups[smoking].choice.unique()

    assert "Y" not in individual_smoking_choices
    assert "Y" not in group_smoking_choices


def test_group_filter_exclude():
    data = _load_test_data()

    def smoking(d):
        return d["measurement_type"] == "smoking"

    def choice_y(d):
        return d["choice"] == "Y"

    def healthy(d):
        return d["measurement_type"] == "healthy"

    def is_healthy(d):
        return healthy(d) & choice_y(d)

    def disease(d):
        return d["measurement_type"] == "disease"

    def smoker_n(d):
        return smoking(d) & (d["choice"] == "N")

    def smoker_y(d):
        return smoking(d) & choice_y(d)

    healthy_smoker_n_data = data.filter_group([is_healthy, smoker_n]).exclude_group([smoker_y, disease])

    group_smoking_choices = healthy_smoker_n_data.groups[smoking].choice.unique()

    assert "Y" not in group_smoking_choices
    assert "N" in group_smoking_choices

    group_healthy_choices = healthy_smoker_n_data.groups[healthy].choice.unique()

    assert "Y" in group_healthy_choices
