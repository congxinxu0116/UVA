import pandas as pd
import warnings
import importlib
import sys
import os 
import warnings
warnings.simplefilter("ignore")
try:
    importlib.util.find_spec("faker"); importlib.util.find_spec("us")
except ImportError:
    os.system("pip3 install faker")
    os.system("pip3 install us")
finally:
    import faker
    from us import states
try:
    data = pd.read_excel("../data/All of Us _ Public PPI Codebook - COPE.xlsx")
except ImportError:
    os.system("pip3 install xlrd")
    data = pd.read_excel("../data/All of Us _ Public PPI Codebook - COPE.xlsx")
sys.path.append('../code/')
from classes import * 


data_lower = data
data_lower.loc[:,"Answer Type"] = data_lower["Answer Type"].str.lower()
grouped = data_lower.groupby(["Type","Answer Type"])

n = 100 # number of survey takers
seed = 126 # arbitrary

datagen = SyntheticData(n,seed)

np.random.seed(seed) # set seed for reproducibility

# -------- Gender -------
genders = ["Male","Female","Other","Prefer Not to Say"] # initialize gender
p_genders = [0.4,0.4,0.04,0.16] # initialize probability of each gender
gender = datagen.generate_data(genders,p_genders)

# ------- Race --------
races = ["Hispanic/Latino", "American Indian or Alaska Native", "Asian",\
         "Black or African American", "Native Hawaiian or Other Pacific Islander",\
          "White","Two or more races."]
p_races = np.array([np.random.randint(low=1,high=100) for i in range(len(races))])
p_races = p_races / sum(p_races)
race = datagen.generate_data(races,p_races)

# ------- State --------
state_names = [state.name for state in states.STATES_AND_TERRITORIES]
p_states = np.array([np.random.randint(low=1,high=100) for i in range(len(state_names))])
p_states = p_states / sum(p_states)
state = datagen.generate_data(state_names,p_states)

# ------- Age Categories -------
age_categories = ["Under 12 years old.","12-17 years old.", "18-24 years old.",
                    "25-34 years old.", "35-44 years old.","45-54 years old.","Older than 55 years"]
p_age = np.array([np.random.randint(low=1,high=100) for i in range(len(age_categories))])
p_age = p_age / sum(p_age)
age = datagen.generate_data(age_categories, p_age)

# -------- Employment Status --------
employment_categories = [
    "Employed for wages", "Self-employed","Out of work and looking for work",\
    "Out of work but not currently looking for work","A homemaker","A student",\
    "Military","Retired","Unable to work"
]
p_employment = np.array([15*x for x in range(len(employment_categories),)[::-1]])
p_employment = p_employment/ sum(p_employment)
employment = datagen.generate_data(employment_categories,p_employment)

# --------- Generating Demographics
demographics = pd.DataFrame({"Gender":gender, "Ethnicity":race, "State":state,"Age":age,"Employment":employment})

print("Generated demographics...")

os.chdir("../data") # enter data folder in order to create the file in there
os.system("python3 ../code/data_cleaning.py") # run python data cleaning script
os.chdir("../Notebooks/") # enter back into Notebook folder
# print("Format:")
# print("question id                       Question                      Possible Answers")
qa_df = pd.read_json('../data/ques_ans_clean.json')
print("Generated question database")


survey_data = pd.DataFrame(np.zeros((n,len(qa_df))),columns=qa_df.qid) # row length - number of subjects
# print("qid", end=  " ")
for qid in qa_df.qid:
    selections = False
#     print(qid, end= " ") # debugging
    
    # -------- Indexing questions -------
    answers = qa_df.loc[qid,'answers'] # Note: only works if df index and qid match up perfectly
#     answers = qa_df.query(f"qid == {qid}")["answers"] # use this otherwise
    
    # -------- Matching types of questions ------- # 
    q_type = qa_df.loc[qid,'Answer Type']
    if q_type.lower() == "multi-select":
        selections = True # enables multiselect

    if answers != None:
        # --------- Text questions (generate 3 sentences)---------- # 
        if answers == 'text':
            survey_data[qid] = survey_data[qid].apply(lambda x: datagen.generate_text(3))
        # --------- Date questions (generate a date between Feb 14th and today)---------- # 
        elif answers == 'date':
            answers = [datagen.generate_date() for i in range(n)]
            survey_data[qid] = datagen.generate_data(answers,\
                                                        datagen.generate_probabilities(len(answers)))
        else:
        # --------- Multi-Select questions ------- # 
            if selections:
                responses = []
                for item_num in range(n):
                    num_answers = np.random.randint(low=1,high=len(answers))
                    response = np.random.choice(answers,size=num_answers,replace=False)
                    responses.append(response)
                survey_data[qid] = responses
        # --------- Single-select questions ---------- # 
            else:
                survey_data[qid] = datagen.generate_data(answers,\
                                                        datagen.generate_probabilities(len(answers)))
    else:
            survey_data[qid] = survey_data[qid].apply(lambda x: np.nan)
print("Generated survey data...")
            
prob_array = pd.DataFrame(np.array([[np.random.random() for i in range(len(qa_df.qid))] for i in range(n)]))
index_array = np.array([prob_array[column].apply((lambda x: True if x > 0.2 else False)) for column in prob_array.columns]).T
for i in range(index_array.shape[0]):
    for j,column in enumerate(survey_data.columns): #num columns == index_array.shape[1]
        if index_array[i,j] == False:
            survey_data.loc[i,column] = np.nan
print("Generated missing values (20% of data)...")



full_survey_results = pd.concat([pd.Series([i for i in range(len(demographics))],name="user_id"),demographics,survey_data],axis=1)

print("Merged dataframes...")

full_survey_results.to_csv("../data/survey.csv",index=False)

print("Outputed results to '../data/survey.csv'...")
print("Done!")