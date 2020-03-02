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


def convert_unit(df, unit_in, unit_out, factor=None, unit_field="unit", data_fields=['mean','median','value', 'sd', 'se', 'min', 'max'], inplace=True, subset=None):
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


def paracetamol_idx(data):
    return (data.substance_intervention == 'paracetamol') \
           & (data.substance == 'paracetamol') \
           & (data[ ('healthy', 'choice')] == 'Y') \
           & (data['tissue'] == 'plasma')

def caffeine_idx(data):
    return (data.substance_intervention == 'caffeine') \
           & (data.substance == 'caffeine') \
           & (data[ ('healthy', 'choice')] == 'Y') \
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

def get_login_token(user, password):
    url = "http://0.0.0.0:8000/api-token-auth/"
    payload = {'username': user, 'password': password}
    response = requests.post(url, data=payload)
    return response.json().get("token")


def get_headers():
    user = "admin"
    password = "pkdb_admin"
    token = get_login_token(user, password)
    headers = {'Authorization': f'Token {token}'}
    return headers


def get_data(url,headers,**kwargs):

    """
    gets the data from a paginated rest api.
    """
    url_params = "?"+urlencode(kwargs)
    acctual_url = urljoin(url,url_params)
    response = requests.get(acctual_url,headers=headers)
    num_pages = response.json()["last_page"]
    data = []
    for page in range(1,num_pages +1):
        url_current = acctual_url + f"&page={page}"
        response = requests.get(url_current,headers=headers)
        data += response.json()["data"]["data"]

    flatten_data = [flatten_json(d) for d in data]
    return pd.DataFrame(flatten_data)

def flatten_json(y):
    """

    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
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








    

def preprocess_interventions(interventions):
            interventions = interventions.drop("normed",axis=1)
            return interventions[interventions.apply(lambda x: x.count()).sort_values(ascending=False).index]
    
def preprocess_outputs(outputs):
            outputs.drop(["normed"],axis=1, inplace=True)
            outputs["interventions"] =outputs["interventions"].apply(lambda interventions: interventions[0]['pk'] if len(interventions) == 1 else np.nan)
            outputs.dropna(subset = ["interventions"], inplace=True)
            outputs.interventions = outputs.interventions.astype(int)
            # sort columns by number of not nan values
            outputs = outputs[outputs.apply(lambda x: x.count()).sort_values(ascending=False).index]
            outputs.set_index(["study","pk"], inplace=True)
            return outputs

        
def preprocess_individuals(subject_data):
            lst_col = 'characteristica_all_normed'
            intermidiate_df = pd.DataFrame({col:np.repeat(subject_data[col].values, subject_data[lst_col].str.len()) for col in subject_data.columns.difference([lst_col])}).assign(**{lst_col:np.concatenate(subject_data[lst_col].values)})[subject_data.columns.tolist()]
            df = intermidiate_df["characteristica_all_normed"].apply(pd.Series)
            df["study"] = intermidiate_df["study"]
            df.drop(["pk"], axis=1,inplace=True)
            df["subject_pk"] = intermidiate_df["pk"]
            df["subject_name"] = intermidiate_df["name"]
            print(intermidiate_df.get("count"))
            
            df = df.pivot_table(index=["study","subject_pk","subject_name"], columns=["measurement_type"], aggfunc=my_tuple) # individual

            df.columns = df.columns.swaplevel(0, 1)
            df = df[df.groupby(level=0, axis=0).count().sum().max(level=0).sort_values(ascending=False).index]
            df.dropna(how="all", axis=1)
            return df
        
def preprocess_groups(subject_data):
            lst_col = 'characteristica_all_normed'
            intermidiate_df = pd.DataFrame({col:np.repeat(subject_data[col].values, subject_data[lst_col].str.len()) for col in subject_data.columns.difference([lst_col])}).assign(**{lst_col:np.concatenate(subject_data[lst_col].values)})[subject_data.columns.tolist()]
            df = intermidiate_df["characteristica_all_normed"].apply(pd.Series)
            df["study"] = intermidiate_df["study"]
            df.drop(["pk"], axis=1,inplace=True)
            df["subject_pk"] = intermidiate_df["pk"]
            df["subject_name"] = intermidiate_df["name"]
            print(intermidiate_df.get("count"))
            
            #group
            df["group_count"] = intermidiate_df["count"]
            df = df.pivot_table(index=["study","subject_pk","subject_name","group_count"], columns=["measurement_type"], aggfunc=my_tuple)
            df.reset_index(level=["group_count"], inplace=True, col_fill='general')
         

            df.columns = df.columns.swaplevel(0, 1)
            df = df[df.groupby(level=0, axis=0).count().sum().max(level=0).sort_values(ascending=False).index]
            df.dropna(how="all", axis=1)
            return df
            
            
            
def merge(individuals,groups,interventions,outputs):    
    all_subjects = merge_groups_individuals(individuals,groups)             
    return merge_all_subjects_interventions_outputs(all_subjects,interventions,outputs)


def merge_groups_individuals(groups, individuals):
        df = pd.concat([groups,individuals], 
                       keys=["individual","group"],
                      sort=False)
        df.reset_index(inplace=True)
        df.rename(columns={"level_0":"subject_type"},inplace=True)
        df.set_index(["study","subject_type","subject_pk","subject_name"], inplace=True)
        df = df[df.groupby(level=0, axis=0).count().sum().max(level=0).sort_values(ascending=False).index]
        df = df.dropna(how="all", axis=1)
        return df
       


def merge_all_subjects_interventions_outputs(subjects,interventions,outputs):

            all_complete_intermediate = pd.merge(left=outputs.reset_index(), right=interventions,  how='left', suffixes=('','_intervention'),left_on='interventions', right_on="pk")
            all_complete_intermediate["subject_type"] = False
            all_complete_intermediate["subject_pk"] = False

            group_idx = all_complete_intermediate["group_pk"].notnull()
            individual_idx = all_complete_intermediate["individual_pk"].notnull()


            all_complete_intermediate.loc[group_idx,"subject_type"] = "group"
            all_complete_intermediate.loc[individual_idx,"subject_type"] = "individual"

            all_complete_intermediate.loc[group_idx,"subject_pk"] = all_complete_intermediate[group_idx]["group_pk"]
            all_complete_intermediate.loc[individual_idx,"subject_pk"] = all_complete_intermediate[individual_idx]["individual_pk"]
            all_complete_df = pd.merge(all_complete_intermediate,subjects.reset_index(),  how='inner', suffixes=('','subject'), on=["subject_pk","subject_type"] )
            all_complete_df["inferred"] = False
            return all_complete_df
        
def infer_from_interventions(data):
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