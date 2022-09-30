#%%
import pandas as pd
import numpy as np
import os

os.chdir('C:/Users/nikit/data_analysis/netflix')

with open('netflix1.csv','r', encoding='utf8') as file:
    netflix = pd.read_csv(file, index_col='show_id')

# %%
null_mask = netflix.isin(['Not Given']).any(axis=1)
# %%
null_frame = netflix[null_mask]
netflix_not_null = netflix[null_mask == False]
# %%
for id in null_frame.index.tolist():
    row = null_frame.loc[id]
    if row['director'] == 'Not Given':
        similar = netflix_not_null[(netflix_not_null['type'] == row['type'])&
                                    (netflix_not_null['country'] == row['country'])&
                                    (netflix_not_null['rating'] == row['rating'])]
        if not similar.empty:
            suggest = similar['director'].value_counts().idxmax()
            netflix.loc[id, 'director'] = suggest

    elif row['country'] == 'Not Given':
        similar = netflix_not_null[(netflix_not_null['type'] == row['type'])&
                                    (netflix_not_null['director'] == row['director'])&
                                    (netflix_not_null['rating'] == row['rating'])]
        if not similar.empty:
            suggest = similar['country'].value_counts().idxmax()
            netflix.loc[id, 'country'] = suggest

# %%
missing_dirs = len(netflix.query('director in ("Not Given", 0)'))
missing_couns = len(netflix.query('country in ("Not Given", 0)'))
# %%
print(f'Unable to suggest: {(missing_couns) + (missing_dirs)}')
# %%
