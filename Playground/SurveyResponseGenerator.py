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
#   - Single Select Question vs. Multi Select Question
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
    [['Display', 'PMI_Code']]
questions.columns = ['Questions', 'PMI_Code']      

answers = data.query('Type == "Answer"')\
    [['Display', 'Parent_code']]      
answers.columns = ['Answers', 'Parent_code'] 

# %% Join Questions and Answers together by ID
pandas.merge(questions, answers, 
                  left_on='PMI_Code', right_on='Parent_code',
                  how = 'left',indicator = 'matched', 
                  validate = 'many_to_many').\
    matched.value_counts()

# both          181
# left_only     146
# right_only      0

# It means that only a couple questions got answered in the Excel file
#   and for some question remain unanswered. For this project, I am only
#   going to focus on the answers.

# %% Program
# Convert Answer DF to a dictionary

answers.pivot(index = 'Answers', columns = 'Parent_code', 
                values = 'Answers')


# %%
