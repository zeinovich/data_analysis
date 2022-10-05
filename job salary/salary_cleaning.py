import pandas as pd
import os
pd.set_option("display.precision", 0)

os.chdir('C:/Users/nikit/data_analysis/job salary')
with open('ds_salaries.csv', 'r') as file:
    data = pd.read_csv(file, index_col=0)

data = data.reset_index()
data_null = data[data.isnull().any(axis=1)]
# None to clean or treat
with open('ds_salaries.csv', 'wb') as file:
    data.to_csv(file, index=True)