The analysis is done on Netflix Data: Cleaning, Analysis and Visualization from kaggle (https://www.kaggle.com/datasets/ariyoomotade/netflix-data-cleaning-analysis-and-visualization)
The task is to clean, analyze and visualize dataset. Cleaning and analysis is (or will be) done in Python, visualization will be done in PowerBI.

- Dataset has around 2800 nulls (out of appr. 9000 rows) in it, so those can't be discarded
- For treating missing data I used simple algorithm that finds all similar rows (using on some criteria) and gives a suggestion based on frequency
- This algorithm is unable to treat 997 rows (appr. 30%) seemingly those that are "alone", so now I'm working on another part of it that will find similarities in titles
- Analysis and visualization are now in process
