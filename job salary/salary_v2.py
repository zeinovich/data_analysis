#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
import os
pd.set_option("display.precision", 0)

os.chdir('C:/Users/nikit/data_analysis/job salary')
with open('ds_salaries.csv', 'r') as file:
    data = pd.read_csv(file, index_col=0)

condition = data['company_location'].value_counts() > 5
condition.index.name = 'country'
coun_list = condition.index.tolist()
coun_conded = [coun for coun in coun_list if condition[coun]]
data = data.query('company_location not in @coun_conded')
#%%
def salary_analysis(dataframe: pd.DataFrame, criteria: str, group: str, dof_skip=False):
    criteria_list = np.unique(dataframe[criteria])
    groups = np.unique(dataframe[group])
    print(criteria_list)
    analysis = {}
    for crit in criteria_list:
        print(crit, criteria)
        data = dataframe.query(f"{criteria} == {crit}") 
        print(data)
        mean = data.groupby(group)['salary_in_usd'].mean()
        count = data.groupby(group)['salary_in_usd'].agg('count')
        std = data.groupby(group)['salary_in_usd'].std()
        mean.name = 'mean'
        count.name = 'count'
        std.name = 'std'
        groups = np.unique(data[group])
        salary = pd.DataFrame(index=groups, columns=['mean', 'count', 'std'])
        salary.index.name = 'experience_level'
        salary.loc[:, 'mean'] = mean
        salary.loc[:, 'count'] = count
        salary.loc[:, 'std'] = std
        alpha = 0.05

        for grp in groups:
            dof = salary.loc[grp, 'count'] - 1
            if dof_skip and dof < 3:
                    salary.drop(grp)
                    continue

            if dof < 3:
                salary.loc[grp, 'conf_int'] = '-'
                continue

            t_crit = abs(t.ppf( alpha / 2, dof))
            conf_int = salary.loc[grp, 'std'] * t_crit / np.sqrt(dof + 1)
            salary.loc[grp, 'conf_int'] = conf_int
        analysis[crit] = salary

    analysis = pd.concat(analysis, names=[criteria, group])
    return analysis

yr_exp_mean = salary_analysis(dataframe=data, criteria='work_year', group='experience_level')
print(yr_exp_mean)
print(' ')
# %%
def comparison_analysis(dataframe: pd.DataFrame):
    domestic_workers = dataframe.query('company_location == employee_residence')
    foreign_workers = dataframe.query('company_location != employee_residence')
    dw_mean = domestic_workers.groupby(['company_location'])['salary_in_usd'].mean()
    fw_mean = foreign_workers.groupby(['company_location'])['salary_in_usd'].mean()
    dw_mean.name = 'domestic_salary'
    fw_mean.name = 'foreign_salary'
    fw_keys = fw_mean.keys()
    analysis = pd.DataFrame(index=coun_conded, columns=['domestic_salary', 'foreign_salary'])
    for coun in coun_conded:
        
        if coun not in fw_keys:
            fw_mean[coun] = '----'

        analysis.loc[coun, 'domestic_salary'], analysis.loc[coun, 'foreign_salary'] = dw_mean[coun], fw_mean[coun]
    print(analysis)
    print(' ')

comparison_analysis(dataframe=data)
# %%
size_exp_mean = salary_analysis(dataframe=data, criteria='company_size', group='experience_level')
print(size_exp_mean)
print(' ')
# %%
size_yr_mean = salary_analysis(dataframe=data, criteria='company_size', group='work_year')
print(size_yr_mean)
print(' ')
# %%
def group_analysis(dataframe: pd.DataFrame, group: str, 
                    criteria_func: str, group_func: str):
    groups = np.unique(dataframe[group]) 
    for grp in groups:
        data_grp = dataframe.query(f"{group} == {grp}").copy()   
        analysis = salary_analysis(dataframe=data_grp, criteria=criteria_func, group=group_func)
        print(f'{grp}\n{analysis}\n')

group_analysis(dataframe=data, group='work_year',
                group_func='experience_level', criteria_func='company_size')
# %%
