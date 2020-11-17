import pandas as pd
import numpy as np
import datetime
from faker import Faker
from faker.providers import lorem

class SyntheticData():
    def __init__(self,size,seed=123):
        '''
        size: number of data points to generate
        '''
        Faker.seed(seed)
        self.faker = Faker()
        self.faker.add_provider(lorem)
        self.n = size
    
    def generate_probabilities(self,n_choices):
        p = np.array([np.random.randint(low=1,high=100) for i in range(n_choices)])
        p = p / sum(p)
    
    def generate_data(self, data, p):
        '''
        data: array/list of choices
        p: probabilities of choices
        '''
        gen_data  = np.random.choice(data, size = self.n, p = p)
        return gen_data
    

    def merge(self,left,right,on,how = "left",indicator = "match",validate=None):

        merged = pd.merge(
        left, # left dataframe
        right,  # joining answers to left df
        how=how, # left join
        on=on, # join on column `Parent Code`
        indicator=indicator,
        validate=validate
        )    
        return merged

    def generate_date(self,start_date = datetime.datetime(2020,2,14),end_date = datetime.datetime.now()):
        days_between = (end_date - start_date).days
        random_day = np.random.randint(low=1,high=days_between)
        random_date = start_date + datetime.timedelta(days=random_day)
        return random_date
    
    def generate_text(self,n_sentences):
        return self.faker.paragraph(nb_sentences=5)
    
    def generate_word(self,n_words):
        return self.faker.word()
        


# def random_genders(genders, p, size):
#     '''
#     genders: array of genders 
#     p: probability associated with those genders
#     size: number of samples to draw
#     '''
#     return np.random.choice(genders,size=size,p=p)

# def random_location()
