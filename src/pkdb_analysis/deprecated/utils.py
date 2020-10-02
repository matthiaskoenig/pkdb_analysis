import requests
import numpy as np
from urllib.parse import urljoin, urlencode
import pandas as pd
import attr
from pathlib import Path
import os
import pint
ureg = pint.UnitRegistry()

FPATH = os.path.realpath(__file__)


def unstring(value):
    if isinstance(value,str):
        return eval(value)
    else:
        return value


def array_from_string(value):
    try:
        return np.array(unstring(value)).astype('float32')
    except SyntaxError:
        return np.fromstring(value.strip('[]') ,dtype=float, sep=" ")


def to_numeric(data_row):
    potential_array_fields =["median","mean","value","se","sd","sd","cv"]
    value_fields = [("weight", "value"), ("weight", "mean"),"value_intervention"]
    for field in value_fields:
        data_row[field] = pd.to_numeric(data_row[field])

    for field in potential_array_fields:
            if data_row["output_type"] == "timecourses":
                data_row[field] = array_from_string(data_row[field])
            else:
                data_row[field] = pd.to_numeric(data_row[field])
    return data_row


def convert_unit(df, unit_in, unit_out, factor=None, unit_field="unit",
                 data_fields=['mean', 'median', 'value', 'sd', 'se', 'min', 'max'],
                 inplace=True, subset=None):
    """ Unit conversion in given data frame. """
    if not inplace:
        df = df.copy()
    if factor is None:
        factor = 1*ureg(unit_in).to(unit_out).m

    if subset is not None:
        for column in subset:
            is_weightidx = df[column].notnull()
            df = df[is_weightidx]
            if isinstance(factor, pd.Series):
                factor = factor[is_weightidx]

    idx = (df[unit_field] == unit_in)

    for key in data_fields:
        df.loc[idx, key] = df.loc[idx, key]*factor
    df.loc[idx, unit_field] = unit_out

    if subset is not None:
        return df[idx]

    return df


def caffeine_idx(data):
    return (data.substance_intervention == 'caffeine') \
           & (data.substance == 'caffeine') \
           & (data[('healthy', 'choice')] == 'Y') \
           & (data['tissue'] == 'plasma')


def paraxanthine_idx(data):
    return (data.substance_intervention == 'caffeine') \
           & (data.substance == 'paraxanthine') \
           & (data[ ('healthy', 'choice')] == 'Y') \
           & (data['tissue'] == 'plasma')

def theobromine_idx(data):
    return (data.substance_intervention == 'caffeine') \
           & (data.substance == 'theobromine') \
           & (data[ ('healthy', 'choice')] == 'Y') \
           & (data['tissue'] == 'plasma')




def paraxanthine_idx_n(data):
    return (data.substance_intervention == 'caffeine') \
           & (data.substance == 'paraxanthine') \
           & (data['tissue'] == 'plasma')

def caffeine_idx_n(data):
    return (data.substance_intervention == 'caffeine') \
           & (data.substance == 'caffeine') \
           & (data['tissue'] == 'plasma')


def measurement_type_data(data,measurement_type):
    return data[data.measurement_type==measurement_type]


def abs_idx(data,unit_field):
    return ~rel_idx(data,unit_field)

def rel_idx(data,unit_field):
    if unit_field == "unit":
        if data["measurement_type"][0] in ["auc_inf","auc_end","concentration"]:
            return data.apply(lambda x: ureg(x[unit_field]).dimensionality.get('[mass]') == 0, axis=1)

        return data.apply(lambda x: ureg(x[unit_field]).dimensionality.get('[mass]') == -1 , axis=1)
    if unit_field == "unit_intervention":
        return data.apply(lambda x: ureg(x[unit_field]).dimensionality.get('[mass]') == 0 , axis=1)


    #return  (data[unit_field].str.endswith("/ kilogram")) | (data[unit_field].str.contains('kg'))





def filter_out(data,unit_field,units):
    return data[~data[unit_field].isin(units)]

def filter_df(filter_dict, df):
    for filter_key, filter_value in filter_dict.items():
        try:
            notfiltering = "NOT_" in filter_value
        except TypeError:
            notfiltering = False

        if notfiltering:
            df = df[df[filter_key] != filter_value[4:]]
        else:
            df = df[df[filter_key] == filter_value]
    return df.drop_duplicates()

def group_idx(data):
    return (data["subject_type"] == 'group')

def individual_idx(data):
    return (data["subject_type"] == 'individual')




def flatten_json(y):
    """

    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        #elif type(x) is list:
        #    i = 0
        #    for a in x:
        #        flatten(a, name + str(i) + '_')
        #       i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def assert_len_units(units):
    assert not len(units) > 2, f"to many intervention units in data set: <{units}>."
    assert len(units) != 0, f"no units : <{units}>."


def my_tuple(data):

    if any(data):
        if len(data) == 1:
            return tuple(data)[0]
        return tuple(data)
    else:
        np.NaN


def add_level_to_df(df, level_name):
    df.columns = pd.MultiIndex.from_tuples(list(zip(df.columns, len(df.columns)*[level_name])))
    return  df.swaplevel(axis=1)

def curator_parse(x):
    return ", ".join([curator['first_name'][0] + " " + curator['last_name'][0] for curator in x ])

def groups_parse(groups_pks, groups):
    this_groups = []
    if isinstance(groups_pks, list):
        for groups_pk in groups_pks:
            this_group = groups.data.loc[groups_pk]
            groups_dict  = {}
            groups_dict["count"] = this_group[("general","group_count")]
            groups_dict["name"] = this_group["subject_name"]
            #groups_dict["parent"] = this_group[("general","parent")]

            this_groups.append(groups_dict)
    return this_groups

def groups_all_count(groups_pks,groups):

    if  groups_pks["group_count"] > 0:
        try:
            for groups_pk in groups_pks["groupset_groups"]:
                this_group = groups.data.loc[groups_pk]
                if this_group["subject_name"] == "all":
                        return this_group[("general","group_count")]
        except TypeError:
            raise TypeError(f"Group is not working: {groups_pks} ,{groups} ")
        except KeyError:
            raise KeyError(f"Group is not working: {groups_pks} ,{groups} ")                      
    else:
        return 0




def individuals_parse(individuals_pks,individuals):
    result = None
    if isinstance(individuals_pks, list):
        result = [individuals.data.loc[individuals_pk]["subject_name"] for individuals_pk in individuals_pks]
        if len(result) == 0:
            result = None
    return result

def interventions_parse(interventions_pks,interventions):
    result = None
    if isinstance(interventions_pks, list):
        result =  [interventions.data.loc[interventions_pk]["name"] for interventions_pk in interventions_pks]
        if len(result) == 0:
            result = None
    return result


@attr.s
class PkdbModel(object):

    name = attr.ib()
    base_url =  attr.ib(default="http://0.0.0.0:8000/api/v1/")
    loaded = attr.ib(default=False)
    preprocessed =  attr.ib(default=False)
    saved = attr.ib(default=False)
    destination =  attr.ib(default="0-raw")
    headers = attr.ib(default=get_headers())

    @property
    def path(self):
        return Path(FPATH).parent / "data" / self.destination / f"{self.name}.tsv"

    @property
    def base_params(self):
        if self.name in ["individuals","groups","studies"]:
                   return {"format":"json"}
        else:
            return {"format":"json", "normed":"true"}

    @property
    def url(self):
        if self.name == "substances":
            return urljoin(self.base_url, f'{self.name}_statistics/')

        return urljoin(self.base_url, f'{self.name}_elastic/')


    def add_data(self, data):
        self.data = data

    def load(self):
        self.data = get_data(self.url,self.headers, **self.base_params)
        self.loaded = True

    def preprocess(self):
        self.data.dropna(how="all",axis=1, inplace=True)
        self._preprocess_outputs()
        self._preprocess_interventions()
        self._preprocess_characteristica()
        self._preprocess_substances()
        self._preprocess_studies()

        self.preprocessed = True
        self.destination = "1-preprocessed"

    def filter_out(self, unit_field, units):
        self.data = filter_out(self.data, unit_field, units)

    def infer_from_interventions(self):
        units = self.data["unit_intervention"].unique()
        assert_len_units(units)

        unit_rel = "g/kg"
        unit_abs = "g"


        for unit in units:
            dim_of_mass = ureg(unit).dimensionality.get('[mass]')
            if dim_of_mass == 0:
                unit_rel = unit
            elif dim_of_mass == 1:
                unit_abs = unit

        data_rel = convert_unit(self.data,
                                unit_in=unit_abs,
                                unit_out=unit_rel,
                                factor=1.0 / self.data[("weight", "value")],
                                unit_field="unit_intervention",
                                data_fields=['value_intervention'],
                                subset=[("weight", "value"), "value"])


        data_abs = convert_unit(self.data,
                                unit_in=unit_rel,
                                unit_out=unit_abs,
                                factor=self.data[("weight", "value")],
                                unit_field="unit_intervention",
                                data_fields=['value_intervention'],
                                subset=[("weight", "value"), "value"])
        data_rel["inferred"] = True
        data_abs["inferred"] = True

        self.data = pd.concat([self.data, data_rel, data_abs], ignore_index=True)

        data_rel = convert_unit(self.data,
                                unit_in=unit_abs,
                                unit_out=unit_rel,
                                factor=1.0 / self.data[("weight", "mean")],
                                unit_field="unit_intervention",
                                data_fields=['value_intervention'],
                                subset=[("weight", "mean"), "mean"])

        data_abs = convert_unit(self.data,
                                unit_in=unit_rel,
                                unit_out=unit_abs,
                                factor=self.data[("weight", "mean")],
                                unit_field="unit_intervention",
                                data_fields=['value_intervention'],
                                subset=[("weight", "mean"), "mean"])
        data_rel["inferred"] = True
        data_abs["inferred"] = True

        self.data = pd.concat([self.data, data_rel, data_abs], ignore_index=True)


    def infer_from_outputs(self):

        units = self.data["unit"].unique()
        assert_len_units(units)

        unit_rel = None
        unit_abs = None

        for unit in units:
            dim_of_mass = ureg(unit).dimensionality.get('[mass]')
            if self.data["measurement_type"].unique()[0] in ["auc_inf","auc_end","concentration"]:
                if dim_of_mass == 0:
                    unit_rel = unit
                elif dim_of_mass == 1:
                    unit_abs = unit
            else:
                if dim_of_mass == -1:
                    unit_rel = unit
                elif dim_of_mass == 0:
                    unit_abs = unit

        if unit_rel is None and unit_abs is not None:
            unit_rel = (ureg(unit_abs)/ureg("kg")).u

        if unit_rel is not None and unit_abs is None:
            unit_rel = (ureg(unit_rel)*ureg("kg")).u


        data_rel = convert_unit(self.data,
                                unit_in=unit_abs,
                                unit_out=unit_rel,
                                factor=1.0 / self.data[("weight", "value")],
                                unit_field="unit",
                                data_fields=['value'],
                                subset=[("weight", "value"), "value"])

        data_abs_i = convert_unit(self.data,
                                  unit_in=unit_rel,
                                  unit_out=unit_abs,
                                  factor=self.data[("weight", "value")],
                                  unit_field="unit",
                                  data_fields=['value'],
                                  subset=[("weight", "value"), "value"])
        data_rel["inferred"] = True
        data_abs_i["inferred"] = True

        self.data = pd.concat([self.data, data_rel, data_abs_i], ignore_index=True)

        data_rel = convert_unit(self.data,
                                unit_in=unit_abs,
                                unit_out=unit_rel,
                                factor=1.0 / self.data[("weight", "mean")],
                                unit_field="unit",
                                data_fields=['mean', 'median', 'sd', 'se'],
                                subset=[("weight", "mean"), "mean"])

        data_abs = convert_unit(self.data,
                                unit_in=unit_rel,
                                unit_out=unit_abs,
                                factor=self.data[("weight", "mean")],
                                unit_field="unit",
                                data_fields=['mean', 'median', 'sd', 'se'],
                                subset=[("weight", "mean"), "mean"])

        data_rel["inferred"] = True
        data_abs["inferred"] = True

        self.data = pd.concat([self.data, data_rel, data_abs], ignore_index=True)


    @property
    def read_kwargs(self):
        if self.name in ["interventions"]:
             return {'header' :[0],'index_col': [0,1,2]}
        elif self.name in ["outputs", 'timecourses']:
             return {'header' :[0],'index_col': [0,1]}
        elif self.name in ["individuals", "groups"]:
             return {'header' :[0,1],'index_col': [0,1,2]}
        elif self.name in ["all_subjects"]:
            return {'header':[0,1], "index_col":[0,1,2,3]}
        elif self.name in ["all_results"]:
            return {'header':[0]}
        elif self.name in ["all_complete"]:
             return {'header':[0], 'low_memory':False}
        
        else:
            return {'header':[0], "index_col":[0]}

    def save(self):
        self.data.to_csv(self.path, sep="\t")
        self.saved = True

    def read(self):
        self.data = pd.read_csv(self.path, sep="\t",**self.read_kwargs)
        self.data.columns = [eval(c) if "," in c else c for c in list(self.data.columns)]

    def to_numeric(self):
            self.data = self.data.apply(to_numeric, axis=1)

    def to_array(self):
        for value in ["mean","median","sd","se","cv","value","time"]:
            self.data[value] = self.data[value].apply(lambda x :array_from_string(x))


    def report(self):
        print("_"*60)
        print(f"Name: {self.name}")
        print(f"Loaded: {self.loaded}")
        print(f"Preprocessed: {self.preprocessed}")
        print(f"saved: {self.saved}")
        if all([self.loaded,self.preprocessed,self.saved]):
            print(f"{self.name} were succsesfully saved to <{self.path}>")


    def _preprocess_substances(self):
         if self.name in ["substances"]:
                
            self.data = self.data[["name","interventions","outputs","outputs_calculated","timecourses"]]
            #self.data.insert(1,"study_number", self.data["studies"].apply(len))
            #self.data = self.data[self.data["study_number"] > 0 ]
            self.data.insert(1,"intervention_number", self.data["interventions"].apply(len))
            self.data.insert(2,"timecourse_number", self.data["timecourses"].apply(len))
            self.data.insert(3,"output_number", self.data["outputs"].apply(len))
            self.data.insert(4,"output_calculated_number", self.data["outputs_calculated"].apply(len))
            self.data.insert(5,"output_raw_number", self.data["outputs"].apply(len)-self.data["outputs_calculated"].apply(len))
            #self.data.sort_values(by="study_number", ascending=False, inplace=True)

    def _preprocess_outputs(self):
        if self.name in ["outputs","timecourses"]:
            self.data.drop(["normed"],axis=1, inplace=True)
            self.data["interventions"] = self.data["interventions"].apply(lambda interventions: interventions[0]['pk'] if len(interventions) == 1 else np.nan) #fixme
            self.data.dropna(subset = ["interventions"], inplace=True)
            self.data.interventions = self.data.interventions.astype(int)
            # sort columns by number of not nan values
            self.data = self.data[self.data.apply(lambda x: x.count()).sort_values(ascending=False).index]
            self.data.set_index(["study","pk"], inplace=True)

    def _preprocess_interventions(self):
        if self.name in ["interventions"]:
            self.data = self.data.drop("normed",axis=1)
            self.data = self.data[self.data.apply(lambda x: x.count()).sort_values(ascending=False).index]

            self.data.set_index(["study","pk","name"], inplace=True)

    def _preprocess_characteristica(self):
        if self.name in ["individuals", "groups"]:
            lst_col = 'characteristica_all_normed'
            intermidiate_df = pd.DataFrame(
                {col:np.repeat(
                    self.data[col].values, 
                    self.data[lst_col].str.len()) for col in self.data.columns.difference([lst_col])}).assign(**{lst_col:np.concatenate(self.data[lst_col].values)})[self.data.columns.tolist()]
            df = intermidiate_df["characteristica_all_normed"].apply(pd.Series)
            df["study"] = intermidiate_df["study"]
            df.drop(["pk"], axis=1,inplace=True)
            df["subject_pk"] = intermidiate_df["pk"]
            df["subject_name"] = intermidiate_df["name"]
            if self.name == "groups" :
                df["group_count"] = intermidiate_df["count"]
                df["parent_pk"] = intermidiate_df["parent_pk"].fillna("None")

                df = df.pivot_table(index=["study","subject_pk","subject_name","group_count","parent_pk"], columns=["measurement_type"], aggfunc=my_tuple)
                df.reset_index(level=["group_count","parent_pk"], inplace=True, col_fill='general')
            else:
                df["group_pk"] = intermidiate_df["group_pk"]
                df = df.pivot_table(index=["study","subject_pk","subject_name","group_pk"], columns=["measurement_type"], aggfunc=my_tuple)
                df.reset_index(level=["group_pk"], inplace=True, col_fill='general')


            df.columns = df.columns.swaplevel(0, 1)
            df = df[df.groupby(level=0, axis=0).count().sum().max(level=0).sort_values(ascending=False).index]
            df.dropna(how="all", axis=1, inplace=True)
            self.data = df

    def _preprocess_studies(self):
        if self.name in ["studies"]:
            groups = PkdbModel("groups", destination="1-preprocessed")
            individuals = PkdbModel("individuals", destination="1-preprocessed")
            interventions = PkdbModel("interventions", destination="1-preprocessed")

            groups.read()
            individuals.read()
            interventions.read()

            groups.data.reset_index(level=["study","subject_name"], inplace=True)
            individuals.data.reset_index(level=["study","subject_name"], inplace=True)


            studies_statistics = pd.DataFrame()
            studies_statistics["name"] = self.data["name"]
            studies_statistics["substances"] = self.data["substances"].apply(lambda x: ', '.join(x))
            studies_statistics['creator'] = self.data[['creator_first_name', 'creator_last_name']].apply(lambda x: x["creator_first_name"][0]+" "+x["creator_last_name"][0], axis=1)
            studies_statistics["curators"] = self.data["curators"].apply(lambda x: curator_parse(x))
            studies_statistics["groups_count"] = self.data["group_count"]
            studies_statistics["group_all_count"] = self.data.apply(lambda x: groups_all_count(x,groups), axis=1)
            studies_statistics["groups"] = self.data["groupset_groups"].apply(lambda x: groups_parse(x,groups))
            studies_statistics["individuals_count"] = self.data["individual_count"]
            studies_statistics["individuals"] = self.data["individualset_individuals"].apply(lambda x:individuals_parse(x,individuals))
            studies_statistics["interventions_count"] = self.data["intervention_count"]
            studies_statistics["outputs_count"] = self.data["output_count"]
            studies_statistics["outputs_calculated_count"] = self.data["output_calculated_count"]
            studies_statistics["timecourses_count"] = self.data["timecourse_count"]
            studies_statistics["results_count"] = studies_statistics["outputs_count"] + studies_statistics["timecourses_count"]

            self.data = studies_statistics.sort_values(by="results_count", ascending=False)


@attr.s
class Preprocessed(object):

    destination = attr.ib(default="2-merged")

    def read(self):
        for field in self._preprocessed_fields:
            pkdb_model = PkdbModel(name=field, destination="1-preprocessed")
            pkdb_model.read()
            setattr(self,field,pkdb_model)

    def merge(self):

        self._merge_groups_individuals()
        self._merge_outputs_timecourses()
        self._merge_individuals_interventions_all_results()
        self._merge_groups_interventions_all_results()
        self._merge_all_subjects_interventions_all_results()

    def save(self):
        for field in self._merged_fields:
            getattr(self,field).save()


    @property
    def _preprocessed_fields(self):
        return ['outputs','timecourses','interventions','individuals','groups']

    @property
    def _merged_fields(self):
        return ["all_subjects", "all_results", "individuals_complete", "groups_complete","all_complete"]

    def _merge_groups_individuals(self):
        df = pd.concat([self.individuals.data,self.groups.data], 
                       keys=["individual","group"],
                      sort=False)
        df.reset_index(inplace=True)
        df.rename(columns={"level_0":"subject_type"},inplace=True)
        df.set_index(["study","subject_type","subject_pk","subject_name"], inplace=True)
        df = df[df.groupby(level=0, axis=0).count().sum().max(level=0).sort_values(ascending=False).index]
        df = df.dropna(how="all", axis=1)
        all_subjects = PkdbModel(name="all_subjects", destination=self.destination)
        all_subjects.add_data(df)
        self.all_subjects = all_subjects

    def _merge_outputs_timecourses(self):
        df = pd.concat([self.outputs.data,self.timecourses.data], keys=["outputs","timecourses"],
                      sort=False)
        df.reset_index(inplace=True)
        df.rename(columns={"level_0":"output_type"},inplace=True)
        df.set_index(["study","output_type","pk"], inplace=True)
        df = df[df.groupby(level=0, axis=0).count().sum().max(level=0).sort_values(ascending=False).index]
        df = df.dropna(how="all", axis=1)
        all_results = PkdbModel(name="all_results", destination=self.destination)
        all_results.add_data(df)
        self.all_results = all_results

    def _merge_individuals_interventions_all_results(self):

        individuals_complete_intermediate = pd.merge(left=self.all_results.data, right=self.interventions.data,  how='inner', suffixes=('','_intervention'),left_on='interventions', right_on="pk")
        individuals_complete_df = pd.merge(individuals_complete_intermediate,self.individuals.data.reset_index(),  how='inner', suffixes=('','subject'),left_on='individual_pk', right_on="subject_pk")
        individuals_complete = PkdbModel(name="individuals_complete", destination=self.destination)
        individuals_complete.add_data(individuals_complete_df)
        self.individuals_complete = individuals_complete

    def _merge_groups_interventions_all_results(self):
        groups_complete_intermediate = pd.merge(left=self.all_results.data, right=self.interventions.data,  how='inner', suffixes=('','_intervention'),left_on='interventions', right_on="pk")
        groups_complete_df = pd.merge(groups_complete_intermediate,self.groups.data.reset_index(),  how='inner', suffixes=('','subject'),left_on='group_pk', right_on="subject_pk")
        groups_complete = PkdbModel(name="groups_complete", destination=self.destination)
        groups_complete.add_data(groups_complete_df)
        self.groups_complete = groups_complete

    def _merge_all_subjects_interventions_all_results(self):

        all_complete_intermediate = pd.merge(left=self.all_results.data.reset_index(), right=self.interventions.data,  how='left', suffixes=('','_intervention'),left_on='interventions', right_on="pk")

        all_complete_intermediate["subject_type"] = False
        all_complete_intermediate["subject_pk"] = False

        group_idx = all_complete_intermediate["group_pk"].notnull()
        individual_idx = all_complete_intermediate["individual_pk"].notnull()


        all_complete_intermediate.loc[group_idx,"subject_type"] = "group"
        all_complete_intermediate.loc[individual_idx,"subject_type"] = "individual"

        all_complete_intermediate.loc[group_idx,"subject_pk"] = all_complete_intermediate[group_idx]["group_pk"]
        all_complete_intermediate.loc[individual_idx,"subject_pk"] = all_complete_intermediate[individual_idx]["individual_pk"]
        all_complete_df = pd.merge(all_complete_intermediate,self.all_subjects.data.reset_index(),  how='inner', suffixes=('','subject'), on=["subject_pk","subject_type"] )
        all_complete_df["inferred"] = False
        all_complete = PkdbModel(name="all_complete", destination=self.destination)
        all_complete.add_data(all_complete_df)
        self.all_complete = all_complete

    def _add_per_bodyweight(self):
            return None


@attr.s
class Result(object):
    compelete_all = attr.ib()


    def plot(self):
        return None

        

            
