The analysis is done on Data Science Job Salaries dataset from kaggle (https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries)
Though dataset is pretty small (~600 rows), it was interesting to find some patterns, like a drop in salaries across all experience levels in 2021 (drop a line here
if you have any idea why). 

- As data cleaning for further analysis, I dropped samples from countries that represent less than 5 samples overall as statistically unsignificant. 
- I used dof_skip criteria to skip samples with less than 3 degrees of freedom for aforementioned reasons
- Confidence intervals are calculated using t-statistics
- For ease and readability, more than one group analysis is done with group_analysis function (I found it hard to operate with more 2 layers of indexing)
