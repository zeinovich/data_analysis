import pandas as pd
import numpy as np
import os

os.chdir('C:/Users/nikit/data_analysis/netflix')

with open('netflix1.csv','r', encoding='utf8') as file:
    netflix = pd.read_csv(file, index_col='show_id')

def get_null(df: pd.DataFrame) -> pd.DataFrame:
    null_mask = df.isin(['Not Given']).any(axis=1)
    null_frame = df[null_mask]
    df_not_null = df[null_mask == False]
    
    return null_frame, df_not_null
def print_missing(df: pd.DataFrame) -> None:
    print('Missing values:')
    print(df.isin(['Not Given']).sum())
null_frame, netflix_not_null = get_null(netflix)

split_title = netflix['title'].str.replace(r'(\S+)\s(\S+).*', r'\1 \2', regex=True)
split_title = pd.DataFrame(split_title, columns=['title'])
split_title.index.name = 'show_id'

# Treatment by similarities in titles
for id in null_frame.index.tolist():
    row = null_frame.loc[id]
    title = row['title'].split(' ')[:2]
    title = ' '.join(title)
    rep_id = split_title[split_title['title'] == title]
    if not rep_id.empty:
        rep_id = rep_id.index[0]
        rep_row = netflix.loc[rep_id]
        if row['director'] == 'Not Given':
            netflix.loc[id, 'director'] = rep_row['director']
        if row['country'] == 'Not Given':
            netflix.loc[id, 'country'] = rep_row['country']

print_missing(netflix)

null_frame, netflix_not_null = get_null(netflix)

# Treatment by other similarities
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

print(print_missing(netflix))

null_frame, netflix_not_null = get_null(netflix)

# Final treatment of nulls
for id in null_frame.index.tolist():
    row = null_frame.loc[id]
    if row['country'] == 'Not Given':
        similar = netflix_not_null.query('director == @row.director')
        if not similar.empty:
            suggest = similar['country'].value_counts().idxmax()
            netflix.loc[id, 'country'] = suggest

print_missing(netflix)

# As far as there are only ~450 missing values, we can drop them
_, netflix = get_null(netflix) 

# As those are useless for visualization, we can drop them
netflix = netflix.drop(columns=['date_added', 'listed_in'], axis=1)

with open('netflix_clean.csv', 'wb') as file:
    netflix.to_csv(file, )