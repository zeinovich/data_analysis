#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
pd.set_option("display.precision", 0)

with open('ds_salaries.csv', 'r') as file:
    data = pd.read_csv(file, index_col=0)

condition = data['company_location'].value_counts() > 5
condition.index.name = 'country'
coun_list = condition.index.tolist()
#%%
coun_conded = [coun for coun in coun_list if condition[coun]]
data = data.loc[data['company_location'].isin(coun_conded)]
#%%
def salary_analysis(dataframe: pd.DataFrame, criteria: str, group: str, dof_skip=False):
    criteria_list = np.unique(dataframe[criteria])
    groups = np.unique(dataframe[group])
    analysis = pd.DataFrame(columns=criteria_list, index=groups)
    analysis.index.name = group
    for crit in criteria_list:
        data = dataframe[dataframe[criteria] == crit]
        data_grouped = data.groupby(group)['salary_in_usd']
        groups = np.unique(data[group])

        mean_ = data_grouped.mean()
        std = data_grouped.std()
        alpha = 0.05

        for grp in groups:
            dof = len(data[data[group] == grp]) - 1

            if dof_skip and dof < 3:
                    mean_.drop(grp)
                    continue

            if dof < 3:
                interval = '-'
                continue

            t_crit = abs(t.ppf(alpha/2, dof))
            conf_int = std[grp]*t_crit / np.sqrt(dof + 1)
            interval = f'+-{conf_int:.0f} ({(conf_int / mean_.loc[grp]*100):.1f}%)'
            mean_[grp] = f'{mean_[grp]:.0f} {interval}'
        analysis[crit] = mean_
    return analysis

yr_exp_mean = salary_analysis(dataframe=data, criteria='work_year', group='experience_level')
print(yr_exp_mean)
print(' ')
# %%
def comparison_analysis(dataframe: pd.DataFrame):
    domestic_workers = dataframe[dataframe['company_location'] == dataframe['employee_residence']]
    foreign_workers = dataframe[dataframe['company_location'] != dataframe['employee_residence']]
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
        data = dataframe[dataframe[group] == grp]
        analysis = salary_analysis(dataframe=data, criteria=criteria_func, group=group_func)
        print(f'{grp}\n{analysis}\n')

group_analysis(dataframe=data, group='work_year',
                group_func='experience_level', criteria_func='company_size')
# %%
