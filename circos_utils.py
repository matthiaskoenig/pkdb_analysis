import pandas as pd
from itertools import combinations, chain

def study_expand(study,  count_label, threshold, type_name = "raw"):
    outputs = pd.DataFrame()
    study_numbers = study[count_label]
    df_study = study[["label","start","end"]]
    df_study["circle_type"] = None

    if type_name:
        df_study["type"] = type_name


    div, modulo  = divmod(int(study_numbers),threshold)

    if div > 0:
        big_study = df_study.copy()
        big_study["circle_type"] = "circle_type=N"
        expanded_outputs = pd.concat([pd.DataFrame(big_study).T]*div, ignore_index=True)
        outputs = outputs.append(expanded_outputs)

    if modulo > 0:
        df_study["circle_type"] = "circle_type=n"
        expanded_outputs = pd.concat([pd.DataFrame(df_study).T]*modulo, ignore_index=True)
        outputs = outputs.append(expanded_outputs)


    return outputs

def create_ideogram(studies_data):
    type_to_label = studies_data.set_index("type").to_dict()["label"]

    ideogram = pd.DataFrame()
    ideogram["len"] = studies_data.groupby(["type"]).apply(len)
    ideogram.index = ideogram.index.astype(int)
    ideogram["label"] = ideogram.apply(lambda x: type_to_label[x.name], axis=1)
    return ideogram


def bubbles_data(studies_data, big_bubble_size):
    studies_data["outputs_raw_count" ] = studies_data["outputs_count" ] - studies_data["outputs_calculated_count" ]
    studies_data["group_not_individual" ] = studies_data["group_all_count" ] - studies_data["individuals_count" ]
    studies_data["group_not_individual"] = studies_data["group_not_individual"].mask(studies_data["group_not_individual"]<0,0 )



    outputs = pd.DataFrame()
    timecourses = pd.DataFrame()
    group_members = pd.DataFrame()
    interventions = pd.DataFrame()
    for idx,study in studies_data.iterrows():
    #for idx,study in studies_data.iloc[::8,:].iterrows():

        raw_output = study_expand(study,"outputs_raw_count",big_bubble_size,"raw")
        if len(raw_output) > 0:
            outputs = outputs.append(raw_output)

        calc_output = study_expand(study,"outputs_calculated_count",big_bubble_size, "calc")
        if len(calc_output) > 0:
            outputs = outputs.append(calc_output)


        timecourse = study_expand(study,"timecourses_count",big_bubble_size)
        if len(timecourse) > 0:
            timecourses = timecourses.append(timecourse)

        intervention = study_expand(study,"interventions_count",big_bubble_size)
        if len(intervention) > 0:
            interventions = interventions.append(intervention)


        group_subject = study_expand(study,"group_not_individual",big_bubble_size,"group_subject")
        if len(group_subject) > 0:
            group_members = group_members.append(group_subject)

        individual = study_expand(study,"individuals_count",big_bubble_size, "individuals")
        if len(individual) > 0:
            group_members = group_members.append(individual)

        bubble_data =  {
            "outputs":outputs,
            "timecourses":timecourses,
            "group_members":group_members,
            "interventions":interventions
        }

    return bubble_data

def create_config_files(studies_data, directory):

    rows_per_study  = 1
    ideogram = create_ideogram(studies_data)
    with open(f"{directory}/data/studies.txt","w") as f:

        for idx, substance in ideogram.iterrows():

            number = idx + 1
            #color_mapping[substance.label] = f"fill_color=spectral-5-div-{number}"
            f.write(f"chr - {substance.label} {substance.label} 0 {substance.len*rows_per_study} pastel2-6-qual-{number}\n")


    frames = []
    for _ , data in studies_data.groupby("label"):

        data["start"] = range(0,len(data)*rows_per_study,rows_per_study)
        data["end"] = range(rows_per_study,(len(data)+1)*rows_per_study,rows_per_study)
        frames.append(data)
    studies_data = pd.concat(frames)

    #names 2d track
    studies_data[["label","start","end","name"]].to_csv(f"{directory}/data/study_names.txt", sep=" ",header=False,index=False)
    # all subjects number for number track
    studies_data[["label","start","end","group_all_count"]].to_csv(f"{directory}/data/all_subjects_number.txt", sep=" ",header=False,index=False)
    studies_data[["label","start","end","timecourses_count"]].to_csv(f"{directory}/data/timecourse_number.txt", sep=" ",header=False,index=False)
    studies_data[["label","start","end","outputs_count"]].to_csv(f"{directory}/data/output_number.txt", sep=" ",header=False,index=False)
    studies_data[["label","start","end","interventions_count"]].to_csv(f"{directory}/data/intervention_number.txt", sep=" ",header=False,index=False)
    #studies_data[["label","start","end","ones","fill_color"]].to_csv(f"{directory}/data/substance_pie.txt", sep=" ",header=False,index=False)

    bubbles_data_dict = bubbles_data(studies_data,25)
    for name, data in bubbles_data_dict.items():
        data[["label","start","end","type","circle_type"]].to_csv(f"{directory}/data/{name}_bubble.txt", sep=" ",header=False,index=False)


def substance_cooccurrence_matrix(studies_data, substances_data):

    substance_dict = substances_data.name.to_dict()
    substance_dict_rev = {v: k for k, v in substance_dict.items()}

    # create substance combinations map
    substance_combinations = iter(())
    substances_all =[]
    for study in studies_data.itertuples():
        if isinstance(study.substances,str):
            this_substance_combinations = study.substances.split(",")
            this_substance_combinations = [x.strip() for x in this_substance_combinations]
            substances_all.extend(this_substance_combinations)
            this_substance_combinations = iter(this_substance_combinations)
            substance_combinations = chain(substance_combinations,combinations(this_substance_combinations,2))

    substances_combinations = pd.DataFrame(list(substance_combinations),columns=["substance1","substance2"])
    substances_combinations["occurance"] = 1
    coocurence_count = substances_combinations.groupby(["substance1","substance2"]).occurance.count().reset_index()
    coocurence_count["substance1_id"] = coocurence_count["substance1"].apply(lambda x : substance_dict_rev[x])
    coocurence_count["substance2_id"] = coocurence_count["substance2"].apply(lambda x : substance_dict_rev[x])

    substances_combinations2 = pd.DataFrame()
    substances_combinations2["substance1"] = substances_combinations["substance2"]
    substances_combinations2["substance2"] = substances_combinations["substance1"]
    substances_combinations2["occurance"] = substances_combinations["occurance"]

    com = substances_combinations2.append(substances_combinations, ignore_index=True)
    coocurence_both_count = com.groupby(["substance1","substance2"]).occurance.count().reset_index()
    result = com.pivot_table(index="substance1", columns="substance2",aggfunc="sum")
    return result.fillna(0) #res

def find_label(substance_type,type_to_label):
    try:
        return type_to_label[substance_type["type"]]
    except KeyError:
        return None
def most_common(lst):
    return max(set(lst), key=lst.count)

def find_study_type(substances_string,substance_to_type):
    substances = str(substances_string).split(",")
    study_type = []
    for substance in substances:
        s = substance.strip()
        if s and s!= "nan":
            study_type.append(substance_to_type[s])
    #substances = [substance.strip() for substance in substances]
    try:
        return int(most_common(study_type))
    except ValueError:
        return None

def add_label_and_type(study_data, substance_data,substance_to_type):

    study_data["type"] = study_data.substances.apply(find_study_type,substance_to_type=substance_to_type)
    substance_data["type"] = substance_data["name"].apply(lambda x : substance_to_type[x])

    # type to label
    name_type=substance_data.loc[substance_data.groupby("type")["study_number"].idxmax()][["name","type"]]
    type_to_label = name_type.set_index("type").to_dict()["name"]
    label_to_type = name_type.set_index("name").to_dict()["type"]

    # label  studies and substances
    study_data["label"] = study_data.apply(find_label,type_to_label=type_to_label, axis=1)
    substance_data["label"] = substance_data.apply(find_label,type_to_label=type_to_label, axis=1)

    return study_data, substance_data
