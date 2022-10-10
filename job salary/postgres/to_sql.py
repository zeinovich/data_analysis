import psycopg2

conn = psycopg2.connect(dbname="postgres", user='postgres', password='pass', host='127.0.0.1', port='5432')

conn.autocommit = True
cursor = conn.cursor()

sql = '''CREATE TABLE IF NOT EXISTS job_salary (index int, 
        work_year int, 
        experience_level varchar(10), 
        employment_type varchar(10), 
        job_title varchar(50), 
        salary int, 
        salary_currency varchar(10), 
        salary_in_usd int, 
        employee_residence varchar(10), 
        remote_ratio int,
        company_location varchar(10), 
        company_size varchar(10));'''

cursor.execute(sql)
print("Table created successfully")

sql2 = '''COPY job_salary (index, work_year, experience_level,
                        employment_type, job_title, salary, salary_currency,
                        salary_in_usd, employee_residence, remote_ratio, company_location, company_size) 
                        FROM 'C:/file/ds_salaries.csv' DELIMITER ',' CSV HEADER;'''

cursor.execute(sql2)
print("Data inserted successfully")

sql3 = '''SELECT * FROM job_salary;'''
cursor.execute(sql3)
for i in cursor.fetchall():
    print(i)

conn.commit()
conn.close()