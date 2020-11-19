# https://dash.plotly.com/dash-core-components/tabs
import numpy as np
import statsmodels
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                  encoding='cp1252', 
                  na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                             'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

paragraph1 = '''According to [this report]
(https://www.cnbc.com/2020/09/18/new-census-data-reveals-no-progress-has-been-made-closing-the-gender-pay-gap.html) 
by CNBC, the gender wage gap still exist in the United States. Based on [the data from U.S Census Bureau]
(https://www.census.gov/newsroom/press-releases/2020/income-poverty.html), for every dollar earned, 
the average full-time working woman still earn $0.18 less than the average full-time working men between 2018 and 2019.'''

paragraph2 = '''The GSS collects data on modern Aermican societies. GSS stands for General Social Survey. It keeps tracks
of hundreds of societal trends since 1972. The GSS contains questions in the area of demography, behavior, 
opinions as well as special interests. The GSS will scientifically select its survey participants to make sure that 
the every section of the country has been meaningfully represented. The GSS has been the gold standard of unbiased
social sicence research for over 40 years. You can learn more about GSS in [here]
(https://gss.norc.org/About-The-GSS).'''

table2 = gss_clean[['income', 'job_prestige', 'socioeconomic_index', 'education', 'sex']].\
    groupby('sex').mean().round(2).reset_index()

table2 = ff.create_table(table2)


table3 = gss_clean[['id', 'sex', 'male_breadwinner']].groupby(['sex', 'male_breadwinner']).count().reset_index()
table3 = table3.rename({'id':'count'}, axis = 1)

fig3 = px.bar(table3, x='male_breadwinner', y='count', color='sex',
              labels={'male_breadwinner':'Level of Agreement with Male Breadwinner Question', 'count':'Number of People'},
              hover_data = ['male_breadwinner'],
              text='male_breadwinner',
              barmode = 'group')

fig3.update_layout(showlegend=True)
fig3.update(layout=dict(title=dict(x=0.5)))


table4 = gss_clean[['sex', 'job_prestige', 'income', 'education', 'socioeconomic_index']]

fig4 = px.scatter(table4, x='job_prestige', y='income', 
                  color = 'sex', 
                  trendline='ols',
                  height=600, width=600,
                  labels={'job_prestige':'Occupational Prestige Score', 
                          'income':'Annual Income'},
                  hover_data=['job_prestige', 'income', 'socioeconomic_index', 'education'])

fig4.update(layout=dict(title=dict(x=0.5)))


table5_income = gss_clean[['sex', 'income']]

fig5_income = px.box(table5_income, x='income', y = 'sex', color = 'sex', 
                     labels={'income':'Annual Income', 'sex':''})

fig5_income.update(layout=dict(title=dict(x=0.5)))
fig5_income.update_layout(showlegend=False)


table5_prestige = gss_clean[['sex', 'job_prestige']]

fig5_prestige = px.box(table5_prestige, x='job_prestige', y = 'sex', color = 'sex',
                       labels={'job_prestige':'Occupational Prestige Score', 'sex':''})

fig5_prestige.update(layout=dict(title=dict(x=0.5)))
fig5_prestige.update_layout(showlegend=False)


table6 = gss_clean[['income', 'sex', 'job_prestige']]

table6['job_prestige_group'] = pd.cut(table6.job_prestige, 
                                      bins = 6, 
                                      labels=("1 Very Low", "2 Low", "3 Medium", 
                                              "4 High", "5 Very High", "6 Super High"))
table6 = table6.dropna()

table6 = table6.sort_values('job_prestige_group')


fig6 = px.box(table6, x = 'income', y = 'sex', color = 'sex', 
              facet_col='job_prestige_group', facet_col_wrap=2,
              color_discrete_map = {'male':'blue', 'female':'red'},
              labels={'income':'Annual', 'sex':''})

fig6.update(layout=dict(title=dict(x=0.5)))
fig6.update_layout(showlegend=False)

bar_columns = ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork'] 
group_columns = ['sex', 'region', 'education'] 

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Gender Difference within United States"),
        
        dcc.Markdown(children = paragraph1),
        dcc.Markdown(children = paragraph2),
        
        html.H2("Gender Difference in Annual Income, Job Prestige, Socioeconomic Status and Years of Formal Education"),
        
        dcc.Graph(figure = table2),
        
        html.H2("Gender Difference in Level of Agreement for the Male Breadwinner Question"),
        dcc.Markdown(children = 'Agree or Disagree with: "It is much better for everyone involved if the man \
        is the achiever outside the home and the woman takes care of the home and family."'),
        
        # dcc.Graph(figure=fig3),
        
        html.Div([
            
            html.H3("Select the variable you want to see. "),
            
            dcc.Dropdown(id='bar',
                         options=[{'label': i, 'value': i} for i in bar_columns],
                         value='male_breadwinner'),
            
            html.H3("Select the grouping variable you want to use"),
            
            dcc.Dropdown(id='group',
                         options=[{'label': i, 'value': i} for i in group_columns],
                         value='sex')
        
        ], style={'width': '25%', 'float': 'left', 'margin-bottom': 100}),
        
        html.Div([
            
            dcc.Graph(id="graph")
        
        ], style={'width': '70%', 'float': 'right'}),        
        
        html.Div([
            
            html.H2("Scatterplot of Job Prestige versus Annual Income by Gender"),
        
            dcc.Graph(figure=fig4),

            html.H2("Distribution of Annual Income by Gender"),

            dcc.Graph(figure=fig5_income),

            html.H2("Distribution of Job Prestige by Gender"),

            dcc.Graph(figure=fig5_prestige),

            html.H2("Distribution of Annual Income by Job Prestige group by Gender"),

            dcc.Graph(figure=fig6)], style={'width': '100%', 'float': 'left','padding': 10})    
    ]
)

@app.callback(Output(component_id="graph",component_property="figure"), 
                  [Input(component_id='bar',component_property="value"),
                   Input(component_id='group',component_property="value")])

def make_figure(bar, group):
    
    table3 = gss_clean[['id', group, bar]].groupby([group, bar]).count().reset_index()
    table3 = table3.rename({'id':'count'}, axis = 1)

    return px.bar(table3, x=bar, y='count', color = group, barmode = 'group')

if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')
    # app.run_server(mode='inline', debug=True, port=1234)
