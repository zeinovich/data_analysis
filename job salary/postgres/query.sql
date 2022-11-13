DO $$                  
    BEGIN 
        IF NOT EXISTS
            ( SELECT *
			  FROM job_salary
			  WHERE salary = 100000
            )
        THEN
            INSERT INTO job_salary (work_year, salary)
			VALUES (2020, 100000);
		END IF;
        END IF ;
    END
   $$ ;