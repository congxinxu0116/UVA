# merging data for single-select questions

options = data.query("Type == 'Answer'") # 181 survey answer options
# Behaviour for single-select questions
# # Non-COPE data
left_df = data.query("Type == 'Question' & `Answer Type` == 'single-select' & `Parent code` != 'COPE'") # Parent Code != "COPE"
right_df = data.query("Type == 'Answer' ")[["Display","Parent code"]]\
.rename({"Display":"Answer"},axis=1)
non_cope = datagen.merge(left_df,right_df,on=["Parent code"],indicator = "match")
non_cope

# # COPE data - Switching PMI and Parent Data for the option df
left_df = data.query("Type == 'Question' & `Answer Type` == 'single-select' & `Parent code` == 'COPE' ")
right_df = data.query("Type == 'Answer'")[["Display","Parent code"]]\
.rename({"Display":"Answer","Parent code":"PMI Code"},axis=1)
cope_pmi_parent_switch = datagen.merge(left_df,right_df,on=["PMI Code"],indicator = "match")
single_select_data = datagen.merge(non_cope,cope_pmi_parent_switch,how="outer",on=None,indicator=False)
single_select_data.loc[40:55,["Display","PMI Code","Parent code","Answer"]]

