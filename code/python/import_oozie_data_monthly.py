import threading
import json
import psycopg2
import datetime
import subprocess

def Timer():
	threading.Timer(7200.0, Timer).start()
	
	subprocess.call([r'<path>\bat\workflows_get_for_grafana.bat'])
	
	month_input_file = open(r"<path>\data\json\oozie_jobs_trends.json")
	month_json_array = json.load(month_input_file)


	conn = psycopg2.connect(database = "oozie_jobs_db", user = "postgres", password = "", host = "127.0.0.1", port = "5432")
	print("Opened database successfully")

	cur = conn.cursor()

	cur.execute('''
				drop table if exists oozie_jobs_monthly_trend;
				''')
	print("Tables droped successfully")	

	cur.execute('''CREATE TABLE oozie_jobs_monthly_trend(
				 seqKey serial PRIMARY KEY,
				 appName VARCHAR (50),
				 run  SMALLINT,
				 consoleUrl VARCHAR (500),
				 createdTime TIMESTAMP,
				 startTime TIMESTAMP,
				 endTime TIMESTAMP,
				 status VARCHAR (50),
				 userName VARCHAR (50),
				 id VARCHAR (200)
				);''')
			
	print("Tables created successfully")		
						
	i = 0	
	for item in month_json_array['workflows']:
		cur.execute("INSERT INTO oozie_jobs_monthly_trend VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (seqKey) DO NOTHING", (i, item['appName'] , item['run'], item['consoleUrl'], item['createdTime'], item['startTime'], item['endTime'], item['status'], item['user'], item['id']))
		i=i+1
			
	conn.commit()
	print("Records inserted successfully")
	conn.close()
	month_input_file.close()

Timer()
