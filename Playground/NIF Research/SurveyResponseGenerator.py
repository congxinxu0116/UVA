# COPE Survey Response Generator
# Author: Congxin (David) Xu
# Date: 2020-11-08

# Workflow:
# 1. Read in the Survey Questions and Answers
# 2. For each Parent Code:
#   - Identify the questions 
#   - Identify the potential responses
#   - Create a hash table with responses
#   - Set up a random process to generate responses based on existing ones.
# 3. Write out the survey response

# %% Import Modules
import pandas 
import numpy

# %% Read In the Data and Preview
# Read in Data from Excel
data = pandas.read_excel("All of Us _ Public PPI Codebook - COPE.xlsx",
                         sheet_name = "COPE Survey")
# Rename column names for better use
data.columns = ['Display', 'Topic', 'Type', 'Answer_Type', 'PMI_System', 
                'PMI_Code', 'Parent_code', 'Date_of_Last_Update']

# Remove not important rows and columns
data = data.query('Type in ("Question", "Answer")')
data = data[['Display', 'Type', 'Answer_Type', 'PMI_Code', 'Parent_code']]
data.head()

# %% Separate Questions and Answers
questions = data.query('Type == "Question"')\
    [['Display', 'PMI_Code', 'Answer_Type']]
questions.columns = ['Questions', 'PMI_Code', 'Answer_Type']      

answers = data.query('Type == "Answer"')\
    [['Display', 'Parent_code']]      
answers.columns = ['Answers', 'Parent_code'] 

# %% Join Questions and Answers together by ID
pandas.merge(questions, answers, 
             left_on='PMI_Code', right_on='Parent_code',
             how = 'left',indicator = 'matched', 
             validate = 'many_to_many').matched.value_counts()

# both          181
# left_only     146
# right_only      0

# It means that only a couple questions got answered in the Excel file
#   and for some question remain unanswered. For this project, I am only
#   going to focus on the questions with answers.

# %% Add Race,  Gender, Age Group to answers:
tmp =  {'Answers': ['American Indian or Alaska Native', 'Asian', 
                    'Black or African American', 'Hispanic or Latino',
                    'Native Hawaiian or Other Pacific Islander',
                    'White', 'Male', 'Female', 'Other', 
                    'Under 12 years old', '12-17 years old', 
                    '18-24 years old.', '25-34 years old.', 
                    '35-44 years old', '45-54 years old.', 
                    '55-64 years old.', '65 or older'], 
        'Parent_code': ['Race', 'Race','Race', 'Race', 'Race', 'Race',
                         'Gender', 'Gender', 'Gender', 'Age_Group', 
                         'Age_Group', 'Age_Group', 'Age_Group', 'Age_Group', 
                         'Age_Group', 'Age_Group', 'Age_Group']}
answers = answers.append(pandas.DataFrame.from_dict(tmp))

# %% Function that generate the survey response
def generate_survey_response(question_id, answers):
    # Filter on the answers with correct answers
    tmp_answers = answers[answers['Parent_code'] == question_id]
    
    if (len(tmp_answers) != 0):
        if (len(tmp_answers) == 1):
            row = 0
        else:
            # Randomly select a row to return
            row = numpy.random.randint(0, len(tmp_answers) - 1)
        # Return the answers of that row
        return tmp_answers.iloc[row, 0]
    else:
        return("NA")


# %% Generate output csv file 
number_of_response = 1000
output = list()
question_id = ['ResponderID', 'Race', 'Gender', 'Age_Group'] + \
    sorted(questions.PMI_Code.unique())

for k in range(1, number_of_response + 1):
    tmp = ['Responder ' + str(k)]
    for i in range(1, len(question_id)):    
        tmp += [generate_survey_response(question_id[i], answers)]

    output += [tmp]

# %%
final = pandas.DataFrame(data = output,columns = question_id)
final.to_csv('RandomSurveyResponse.csv')
