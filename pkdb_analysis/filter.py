"""
Helpers for filtering PKDB data
"""
from copy import deepcopy


class Filter(object):
    """
    Filter objects for PKDBData
    """
    KEYS = ['groups', 'individuals', "interventions", "outputs", "timecourses"]

    def __init__(self, normed=True):
        """ Create new Filter instance.

        :param normed: [True, False, None] return [normed data, unnormalized data, normed and unnormalized data]
        """
        self.groups = dict()
        self.individuals = dict()
        self.interventions = dict()
        self.outputs = dict()
        self.timecourses = dict()

        # FIXME: make generic with code completion (the following is not working with pycharm)
        # for filter_key in Filter.KEYS:
        #    setattr(self, filter_key, dict())

        self.set_normed(normed)

    def set_normed(self, normed=None):
        """ Set the normed attribute"""
        if normed not in [True, False, None]:
            raise ValueError

        if normed in [True, False]:
            if normed:
                normed_value = "true"
            else:
                normed_value = "false"
            for filter_key in ["interventions", "outputs", "timecourses"]:
                d = getattr(self, filter_key)
                d["normed"] = normed_value

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {filter_key: deepcopy(getattr(self, filter_key)) for filter_key in Filter.KEYS}

    def add_to_all(self, key, value):
        """ Adds entry (key, value) to all KEY dictionaries

        :return: None
        """
        for filter_key in Filter.KEYS:
            getattr(self, filter_key)[key] = value

    @staticmethod
    def combine_filters(**filters):
        """ Combie multiple filters

        :param filters:
        :return:
        """
        pass


class FilterFactory(object):

    @staticmethod
    def by_study_sid(study_sid: str) -> Filter:
        """ Creates filter based on study_sid.
        Only data for the given study_sid is returned.
        """
        filter = Filter()
        filter.add_to_all("study_sid", study_sid)
        return filter

    @staticmethod
    def by_study_name(study_name: str) -> Filter:
        """ Creates filter based on study_name.
        Only data for the given study_name is returned.
        """
        filter = Filter()
        filter.add_to_all("study_name", study_name)
        return filter
