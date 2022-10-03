#%%
import pandas as pd
import numpy as np
import os

os.chdir('C:/Users/nikit/data_analysis/netflix')

with open('/datasets/netflix_clean.csv','r', encoding='utf8') as file:
    netflix = pd.read_csv(file, index_col='show_id')

#%%
country_count = netflix['country'].value_counts()
country_count.name = 'total_count'
country_count.index.name = 'country'
country_count = pd.DataFrame(country_count)

tv_count = netflix[netflix['type'] == 'TV Show']['country'].value_counts()
tv_count.name = 'tv_count'
tv_count.index.name = 'country'

country_count = country_count.join(tv_count, on='country')
country_count['tv_count'] = country_count['tv_count'].fillna(0)

movie_count = netflix[netflix['type'] == 'Movie']['country'].value_counts()
movie_count.name = 'movie_count'
movie_count.index.name = 'country'

country_count = country_count.join(movie_count, on='country')
country_count['movie_count'] = country_count['movie_count'].fillna(0)

country_count = country_count.astype(int)

with open('/data for power bi/country_count.csv','wb') as file:
    country_count.to_csv(file)
# %%
director_count = netflix['director'].value_counts()
director_count.name = 'total_count'
director_count.index.name = 'director'
director_count = pd.DataFrame(director_count[:11])

movie_count = netflix[netflix['type'] == 'Movie']['director'].value_counts()
movie_count.name = 'movie_count'
movie_count.index.name = 'director'
director_count = director_count.join(movie_count, on='director')

tv_count = netflix[netflix['type'] == 'TV Show']['director'].value_counts()
tv_count.name = 'tv_count'
tv_count.index.name = 'director'
director_count = director_count.join(tv_count, on='director')
director_count['tv_count'] = director_count['tv_count'].fillna(0)

# We know that Martin Scorcese had not directed any TV Shows
director_count.loc['Martin Scorcese', :] = [12, 12, 0]
director_count = director_count.drop('Martin Scorsese')

director_count = director_count.sort_values(by='total_count', ascending=False)
director_count = director_count.astype(int)

with open('/data for power bi/director_count.csv','wb') as file:
    director_count.to_csv(file, index=True)
# %%
genre_count = netflix['listed_in'].str.split(', ', expand=True).stack().value_counts()
genre_count.name = 'total_count'
genre_count.index.name = 'genre'
genre_count = pd.DataFrame(genre_count)
#%%
movie_count = netflix[netflix['type'] == 'Movie']['listed_in'].str.split(', ', expand=True).stack().value_counts()
movie_count.name = 'movie_count'
movie_count.index.name = 'genre'
genre_count = genre_count.join(movie_count, on='genre')
genre_count['movie_count'] = genre_count['movie_count'].fillna(0)
#%%
tv_count = netflix[netflix['type'] == 'TV Show']['listed_in'].str.split(', ', expand=True).stack().value_counts()
tv_count.name = 'tv_count'
tv_count.index.name = 'genre'
genre_count = genre_count.join(tv_count, on='genre')
genre_count['tv_count'] = genre_count['tv_count'].fillna(0)
#%%
genre_count = genre_count.astype(int)
# %%
with open('/data for power bi/genre_count.csv','wb') as file:
    genre_count.to_csv(file)
# %%
