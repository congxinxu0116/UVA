import sys
sys.path.append('../code/')
import importlib
import os

try:
    importlib.util.find_spec("faker"); importlib.util.find_spec("us")
except ImportError:
    os.system("pip3 install faker")
    os.system("pip3 install us")
finally:
    import faker
    from us import states

from classes import * 


try:
    data = pd.read_excel("../data/All of Us _ Public PPI Codebook - COPE.xlsx")
except ImportError:
    os.system("pip3 install xlrd")
    data = pd.read_excel("../data/All of Us _ Public PPI Codebook - COPE.xlsx")

n = 100 # number of survey takers
seed = 126 # arbitrary

datagen = SyntheticData(n,seed)

np.random.seed(seed) # set seed for reproducibility

    
questions = data.query("Type == 'Question'")
questions = questions.reset_index(drop=True)
options = data.query("Type == 'Answer' ")

# Options 
yn = ["Yes","No"]
ynm = ["Yes","No","Not Sure", "Prefer Not to Answer"]
answers = dict()
# descriptors 0
answers[0] = np.nan
# Section 1
# 1-8
for i in range(1,9):
    answers[i] = ['None of the days (0 days)' ,'A few days (1-2 days)', 'Most days (3-4 days)' ,'Every day']
# 9
answers[9] = ['A lot less than normal','Somewhat less than normal', 'About the same as normal', 'More than normal', "A lot more than normal"]
# 10
answers[10] = ["All of the time", "Most of the time", "Sometimes","Rarely"]
# Section 2
answers[11] = yn
answers[12] = 'date'
answers[13] = options[options["Parent code"].str.contains("cdc_covid_19_7_xx23")].Display.to_list()
answers[14] = options[options["Parent code"].str.contains('copect_17')].Display.to_list()
answers[15] = ynm
# Section 3 
answers[16] = ynm
answers[17] = ["Yes", "No","Unknown", "Waiting for Results"]
answers[18] = options[options["Parent code"].str.contains('cdc_covid_19_n_a')].Display.to_list()
answers[19] = ynm
# Section 4
answers[20] = options[options["Parent code"].str.contains('copect_63_xx20')].Display.to_list()
answers[21] = options[options["Parent code"].str.contains('copect_63_xx21')].Display.to_list()
# Section 5
answers[22] = np.nan
sec5ans = ['Not at all', 'A little bit', 'Moderately', 'Quite a bit', 'Extremely']
for i in range(23,29):
    answers[i] = sec5ans
answers[29] = options[options["Parent code"].str.contains('cdc_covid_19_18')].Display.to_list()
answers[30] = options[options["Parent code"].str.contains('cdc_covid_19_23')].Display.to_list()
answers[31] = options[options["Parent code"].str.contains('cdc_covid_19_26')].Display.to_list()
answers[32] = options[options["Parent code"].str.contains('cdc_covid_19_25')].Display.to_list()
# Section 6
answers[33] =  options[options["Parent code"].str.contains('lot_r_1')].Display.to_list()
answers[34] =  options[options["Parent code"].str.contains('ukmh_j1')].Display.to_list()
answers[35] =  options[options["Parent code"].str.contains('ukmh_j3')].Display.to_list()
# Section 7
answers[36] = [i for i in range(0,15)]
answers[37] = [i for i in range(0,14)]
answers[38] = options[options["Parent code"].str.contains('cu_covid')].Display.to_list()
answers[39] = 'text'
answers[40] = options[options["Parent code"].str.contains('basics_12')].Display.to_list()
answers[41] = 'text'
answers[42] = options[options["Parent code"].str.contains('basics_11')].Display.to_list()
answers[43] = 'text'
answers[44] = yn
answers[44] = yn
answers[45] = yn
answers[46] = options[options["Parent code"].str.contains('basics_8')].Display.to_list()
answers[47] = ynm
# Section 8
mos = ["All of the time", "Most of the time", "Some of the time","A little of the time", "None of the time"]
for i in range(48,58):
    answers[i] = mos
# Section 9
gad = ["Not at all","Several days", "Over half of the days", "Nearly every day"]
for i in range(58,65):
    answers[i] = gad
# Section 10
phq= ["Not at all", "Several Days", "More than half the days", "Nearly every day"]
for i in range(65,74):
    answers[i] = phq
answers[74] = np.nan
# Section 11
cpss = ["Never" , "Almost Never", "Sometimes" , "Fairly Often", "Very Often"]
for i in range(75,85):
    answers[i] = cpss
# Section 12
answers[85] = yn
answers[86] = [i for i in range(1,8)]
answers[87] = [i for i in range(0,24)]
answers[88] = [i for i in range(0,60)]
answers[89] = yn
answers[90] = [i for i in range(1,8)]
answers[91] = [i for i in range(0,24)]
answers[92] = [i for i in range(0,60)]
answers[93] = yn
answers[94] = [i for i in range(1,8)]
answers[95] = [i for i in range(0,24)]
answers[96] = [i for i in range(0,60)]
answers[97] = np.nan
answers[98] = [i for i in range(0,24)]
answers[99] = [i for i in range(0,60)]
# Section 13
ucla_ls = ["Never","Rarely","Sometimes","Often"]
for i in range(100,108):
    answers[i] = ucla_ls
# Section 14
cope = ["Yes, Every day", "Yes, Some days", "Not currently, but in the past", "No, Never", "Prefer not to answer"]
answers[108] = cope
answers[109] = np.nan # fix
answers[110] = [i for i in range(0,4)]
answers[111] = [i for i in range(0,12)]
answers[112] = [i for i in range(0,100)]
answers[113] = cope 
answers[114] = cope
answers[115] = np.nan
answers[116] = [i for i in range(0,4)]
answers[117] = [i for i in range(0,12)]
answers[118] = [i for i in range(0,100)]
answers[119] = ["Never","Montly or less", "2-4 times a month",\
                "2-3 times a week", "4 or more times a week", "Prefer not to answer"]
answers[120] = ["1 or 2", "3 or 4", "5 or 6", "7 to 9", "10 or more","Prefer not to answer"]
answers[121] = ["Never","Less than monthly", "Monthly", "Weekly", "Daily or almost daily", "Prefer not to answer"]
answers[122] = options[options["Parent code"].str.endswith('tsu_ds5_13_xx')].Display.to_list()
use_time = ['Only a few times','1-3 times per month', '1-5 times per week' ,'Daily']
use_freq = ["Less often than usual","The same as usual", "More often than usual"]
# Cannabis
answers[123] = use_time
answers[124] = yn # cannabis
answers[125] = use_freq
# Synthetic Cannabis
answers[126] = use_time
answers[127] = yn
answers[128] = use_freq
# Cocaine
answers[129] = use_time
answers[130] = yn
answers[131] = use_freq
# Prescription stimulants
answers[132] = use_time
answers[133] = ["Yes","No","None","Prefer not to answer"]
answers[134] = use_freq
# Meth
answers[135] = use_time
answers[136] = yn
answers[137] = use_freq
# Synthetic stimulants
answers[138] = use_time
answers[139] = yn
answers[140] = use_freq
# Inhalants
answers[141] = use_time
answers[142] = use_freq
# Prescription Sedatives
answers[143] = use_time
answers[144] = ["Yes","No","None","Prefer not to answer"]
answers[145] = use_freq
# Hallucinogens
answers[146] = use_time
answers[147] = yn
answers[148] = use_freq
# Heroin
answers[149] = use_time
answers[150] = yn
answers[151] = use_freq
# Prescription opioids
answers[152] = ["Yes","No","None","Prefer not to answer"]
answers[153] = use_time
answers[154] = yn
answers[155] = use_freq
# Other substance
answers[156] = ["drug1","drug2","drug3"] # example drugs
answers[157] = use_time
answers[158] = yn
answers[159] = use_freq
# Section 15
brcs = ["Does not describe me at all", "Does not describe me Neutral","Describes me", "Describes me very well"]
for i in range(160,164):
    answers[i] = brcs
# Section 16
teds = ["Almost everyday", "At least once a week", "A few times a month", "Never"]
for i in range(164,173):
    answers[i] = teds
answers[173] = options[options["Parent code"].str.contains('eds_follow_up_1')].Display.to_list()
answers[174] = 'text'
answers[175] = ["Never","Once","2 - 5 times","More than 5 times"]
answers[176] = ynm
answers[177] = options[options["Parent code"].str.contains("nhs_covid_fhc17b")].Display.to_list()
answers[178] = 'text'

# --------- Saving to CSV  ----------
# Convert to one-column df
answer_col = {"answers":answers}
# Save to csv
pd.concat([pd.DataFrame({"qid": [i for i in range(0, len(questions))]}) , questions[["Display","Answer Type"]] ,pd.DataFrame(answer_col)],axis=1).to_json('../data/ques_ans_clean.json')

print("Cleaned questions and answers to json!")