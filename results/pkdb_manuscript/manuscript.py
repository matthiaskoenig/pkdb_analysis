import pint
import pandas as pd
import numpy as np

from urllib.parse import urljoin, urlencode
import requests
import attr
ureg = pint.UnitRegistry()


###############################################################
# Load Data
###############################################################

def get_data(base,dtype, login = None, **kwargs):

    """
    gets the data from a paginated rest api.
    """
    rest_api =  urljoin(base,"api/v1/")
    authentication = urljoin(base,"/api-token-auth/")
    
    headers = {}
    if login:
        headers = get_headers(authentication,**login)
        
    url_params = "?"+urlencode(kwargs)
    url =  urljoin(rest_api,f"{dtype}_elastic/")
    url_filter = urljoin(url,url_params)

    response = requests.get(url_filter)
    num_pages = response.json()["last_page"]
    data = []
    for page in range(1,num_pages +1):
        url_current = url_filter + f"&page={page}"
        response = requests.get(url_current,headers=headers)
        data += response.json()["data"]["data"]
    flatten_data = [flatten_json(d) for d in data]
    return pd.DataFrame(flatten_data)

# User authentication

def get_login_token(url, user, password):
    payload = {'username': user, 'password': password}
    response = requests.post(url, data=payload)


    return response.json().get("token") 

def get_headers(url ,user, password):
    token = get_login_token(url,user, password)
    return {'Authorization': f'Token {token}'}

# Helper function
def flatten_json(y):
    """
    flatten the nested json. into a single dictonary.
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

###############################################################
# utils
###############################################################
def filter_out(data,unit_field,units):
    return data[~data[unit_field].isin(units)]

def assert_len_units(units):
    assert not len(units) > 2, f"to many intervention units in data set: <{units}>."
    assert len(units) != 0, f"no units : <{units}>."
def to_numeric(df):
    columns = ["mean","median","min","max","sd","se","cv","value"]
    for column in columns:
        df[column].fillna(value=pd.np.nan, inplace=True)
        df[column] = pd.to_numeric(df[column])
    return df




###############################################################
# Calculated from body weight
###############################################################
   


def convert_unit(df, unit_in, unit_out, factor=None, unit_field="unit", data_fields=['mean','median','value', 'sd', 'se', 'min', 'max'], inplace=True, subset=None):
    """ Unit conversion in given data frame. """

    if not inplace:
        df = df.copy()
    if factor is None:
        factor = 1*ureg(unit_in).to(unit_out).m

    if subset is not None:
        for column in subset:
            is_weightidx = df[column].notna()
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





@attr.s
class PKData(object):
    groups = attr.ib()
    individuals = attr.ib()
    interventions = attr.ib()
    outputs = attr.ib()
    
    def format(self):
        self._format_groups()
        self._format_individuals()
        self._format_interventions()
        self._format_outputs()

    def merge(self):
        all_subjects = self.merge_groups_individuals(self.individuals,self.groups)             
        self.outputs_m = self.merge_all_subjects_interventions_outputs(all_subjects,self.interventions,self.outputs)
    
    def infer_by_bodyweight(self):
        pass
    
    def plot():
        pass
    
    ###############################################################
    # format data
    ###############################################################

    def _format_interventions(self):
        self.interventions.drop("normed",axis=1, inplace=True)
        self.interventions = to_numeric(self.interventions)
        
        
    def _format_outputs(self):
        self.outputs.drop(["normed"],axis=1, inplace=True)
        self.outputs = to_numeric(self.outputs)

        ##################################### 
        # use only outputs with one intervention
        self.outputs["interventions"] =self.outputs["interventions"].apply(
            lambda interventions: interventions[0]['pk'] if len(interventions) == 1 else np.nan)
        self.outputs.dropna(subset = ["interventions"], inplace=True)
        self.outputs.interventions = self.outputs.interventions.astype(int)
        #####################################
        self.outputs.set_index(["study","pk"], inplace=True)
                
                
    @staticmethod            
    def _all_characteristica(subject_data):
        lst_col = 'characteristica_all_normed'
        intermidiate_df = pd.DataFrame(
            {col:np.repeat(subject_data[col].values, subject_data[lst_col].str.len()) for col in subject_data.columns.difference([lst_col])}).assign(**{lst_col:np.concatenate(subject_data[lst_col].values)})[subject_data.columns.tolist()]
        df = intermidiate_df["characteristica_all_normed"].apply(pd.Series)
        df["study"] = intermidiate_df["study"]
        df.drop(["pk"], axis=1,inplace=True)
        df["subject_pk"] = intermidiate_df["pk"]
        df["subject_name"] = intermidiate_df["name"]
        try:
            df["group_count"] = intermidiate_df["count"]
        except KeyError:
            pass
            

        df = to_numeric(df)
        return df
                
    @staticmethod
    def multiple_characteristica(data):
        if any(data):
            if len(data) == 1:
                return tuple(data)[0]
            return tuple(data)
   
        
        
    def _format_individuals(self):
        all_characteristica = self._all_characteristica(self.individuals)   
        self.individuals = all_characteristica.pivot_table(index=["study","subject_pk","subject_name"], columns=["measurement_type"], aggfunc=self.multiple_characteristica)
        self.individuals.columns = self.individuals.columns.swaplevel(0, 1)
        
                
                
    def _format_groups(self):
        all_characteristica = self._all_characteristica(self.groups)
        
        self.groups = all_characteristica.pivot_table(
            index=["study","subject_pk","subject_name","group_count"], 
            columns=["measurement_type"], 
            aggfunc=self.multiple_characteristica)
        
        self.groups.reset_index(level=["group_count"], inplace=True, col_fill='general')
        self.groups.columns = self.groups.columns.swaplevel(0, 1)
        self.groups.dropna(how="all", axis=1, inplace=True)
    
    ###############################################################
    # Merge data
    ###############################################################
    

    @staticmethod
    def merge_groups_individuals(groups, individuals):
        df = pd.concat(
            [groups,individuals], 
            keys=["individual","group"],
            sort=False)
        df.reset_index(inplace=True)
        df.rename(columns={"level_0":"subject_type"},inplace=True)
        df.set_index(["study","subject_type","subject_pk","subject_name"], inplace=True)
        df = df[df.groupby(level=0, axis=0).count().sum().max(level=0).sort_values(ascending=False).index]
        df = df.dropna(how="all", axis=1)
        return df


    @staticmethod
    def merge_all_subjects_interventions_outputs(subjects,interventions,outputs):

        all_complete_intermediate = pd.merge(
            left=outputs.reset_index(),
            right=interventions,  
            how='left', 
            suffixes=('','_intervention'),
            left_on='interventions', 
            right_on="pk")
        all_complete_intermediate["subject_type"] = False
        all_complete_intermediate["subject_pk"] = False

        group_idx = all_complete_intermediate["group_pk"].notnull()
        individual_idx = all_complete_intermediate["individual_pk"].notnull()
        
        all_complete_intermediate.loc[group_idx,"subject_type"] = "group"
        all_complete_intermediate.loc[group_idx,"subject_pk"] = all_complete_intermediate[group_idx]["group_pk"]

        all_complete_intermediate.loc[individual_idx,"subject_type"] = "individual"
        all_complete_intermediate.loc[individual_idx,"subject_pk"] = all_complete_intermediate[individual_idx]["individual_pk"]

        all_complete_df = pd.merge(
            all_complete_intermediate,subjects.reset_index(),
            how='left', 
            suffixes=('',''),
            on=["subject_pk","subject_type"] )
        all_complete_df["inferred"] = False
        all_complete_df = all_complete_df[~all_complete_df.duplicated(subset="pk")]

        return all_complete_df
    
    def infer_from_outputs(self):

        units = self.outputs_m["unit"].unique()
        assert_len_units(units)

        unit_rel = None
        unit_abs = None

        for unit in units:
            dim_of_mass = ureg(unit).dimensionality.get('[mass]')
            if self.outputs_m["measurement_type"].unique()[0] in ["auc_inf","auc_end","concentration"]:
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


        data_rel = convert_unit(self.outputs_m,
                                unit_in=unit_abs,
                                unit_out=unit_rel,
                                factor=1.0 / self.outputs_m[("weight", "value")],
                                unit_field="unit",
                                data_fields=['value'],
                                subset=[("weight", "value"), "value"])

        data_abs_i = convert_unit(self.outputs_m,
                                  unit_in=unit_rel,
                                  unit_out=unit_abs,
                                  factor=self.outputs_m[("weight", "value")],
                                  unit_field="unit",
                                  data_fields=['value'],
                                  subset=[("weight", "value"), "value"])
        data_rel["inferred"] = True
        data_abs_i["inferred"] = True

        self.outputs_m = pd.concat([self.outputs_m, data_rel, data_abs_i], ignore_index=True)

        data_rel = convert_unit(self.outputs_m,
                                unit_in=unit_abs,
                                unit_out=unit_rel,
                                factor=1.0 / self.outputs_m[("weight", "mean")],
                                unit_field="unit",
                                data_fields=['mean', 'median', 'sd', 'se'],
                                subset=[("weight", "mean"), "mean"])

        data_abs = convert_unit(self.outputs_m,
                                unit_in=unit_rel,
                                unit_out=unit_abs,
                                factor=self.outputs_m[("weight", "mean")],
                                unit_field="unit",
                                data_fields=['mean', 'median', 'sd', 'se'],
                                subset=[("weight", "mean"), "mean"])

        data_rel["inferred"] = True
        data_abs["inferred"] = True

        self.outputs_m = pd.concat([self.outputs_m, data_rel, data_abs], ignore_index=True)
        
    def infer_from_interventions(self):
        units = self.outputs_m["unit_intervention"].unique()
        assert_len_units(units)

        unit_rel = "g/kg"
        unit_abs = "g"


        for unit in units:
            dim_of_mass = ureg(unit).dimensionality.get('[mass]')
            if dim_of_mass == 0:
                unit_rel = unit
            elif dim_of_mass == 1:
                unit_abs = unit

        data_rel = convert_unit(self.outputs_m,
                                unit_in=unit_abs,
                                unit_out=unit_rel,
                                factor=1.0 / self.outputs_m[("weight", "value")],
                                unit_field="unit_intervention",
                                data_fields=['value_intervention'],
                                subset=[("weight", "value"), "value"])


        data_abs = convert_unit(self.outputs_m,
                                unit_in=unit_rel,
                                unit_out=unit_abs,
                                factor=self.outputs_m[("weight", "value")],
                                unit_field="unit_intervention",
                                data_fields=['value_intervention'],
                                subset=[("weight", "value"), "value"])
        data_rel["inferred"] = True
        data_abs["inferred"] = True

        self.outputs_m = pd.concat([self.outputs_m, data_rel, data_abs], ignore_index=True)

        data_rel = convert_unit(self.outputs_m,
                                unit_in=unit_abs,
                                unit_out=unit_rel,
                                factor=1.0 / self.outputs_m[("weight", "mean")],
                                unit_field="unit_intervention",
                                data_fields=['value_intervention'],
                                subset=[("weight", "mean"), "mean"])

        data_abs = convert_unit(self.outputs_m,
                                unit_in=unit_rel,
                                unit_out=unit_abs,
                                factor=self.outputs_m[("weight", "mean")],
                                unit_field="unit_intervention",
                                data_fields=['value_intervention'],
                                subset=[("weight", "mean"), "mean"])
        data_rel["inferred"] = True
        data_abs["inferred"] = True
        
        


        self.outputs_m = pd.concat([self.outputs_m, data_rel, data_abs], ignore_index=True)
        # change unit of intervention
        self.outputs_m = convert_unit(self.outputs_m,
                                unit_in="gram / kilogram",
                                unit_out="mg/kg",
                                factor=ureg("g/kg").to("mg/kg"),
                                unit_field="unit_intervention",
                                data_fields=['value_intervention'])

            




