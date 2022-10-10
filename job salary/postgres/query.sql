CREATE EXTENSION IF NOT EXISTS tablefunc;

SELECT * FROM CROSSTAB($$
	WITH us_avg AS (
		SELECT 
		  experience_level,
		  work_year, 
		  ROUND (AVG(salary_in_usd), -3) :: NUMERIC
			AS avg_salary
	FROM job_salary
	GROUP BY experience_level, work_year
	HAVING COUNT(*) > 5)	
					   	
	SELECT 
		experience_level,
		work_year,
		avg_salary
	FROM us_avg
	ORDER BY experience_level ASC, work_year ASC;
$$) as ct (experience_level VARCHAR(10),
		  "2020" NUMERIC,
		  "2021" NUMERIC,
		  "2022" NUMERIC)
ORDER BY "2020" ASC;