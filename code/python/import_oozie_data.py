import threading
import json
import psycopg2
import datetime
import subprocess

def Timer():
	threading.Timer(300.0, Timer).start()
	
	subprocess.call([r'<path>\bat\helix_prod_workflows_live.bat'])
	
	failed_input_file = open(r"<path>\data\json\oozie_jobs_failed_live.json")
	failed_json_array = json.load(failed_input_file)

	success_input_file = open(r"<path>\data\json\oozie_jobs_succeeded_live.json")
	success_json_array = json.load(success_input_file)

	killed_input_file = open(r"<path>\data\json\oozie_jobs_killed_live.json")
	killed_json_array = json.load(killed_input_file)

	running_input_file = open(r"<path>\data\json\oozie_jobs_running_live.json")
	running_json_array = json.load(running_input_file)

	queue_input_file = open(r"<path>\data\json\queue_live.json")
	queue_json_array = json.load(queue_input_file)


	conn = psycopg2.connect(database = "oozie_jobs_db", user = "postgres", password = "", host = "127.0.0.1", port = "5432")
	print("Opened database successfully")

	cur = conn.cursor()

	cur.execute('''
				drop table if exists oozie_jobs_failed_live;
				drop table if exists oozie_jobs_success_live;
				drop table if exists oozie_jobs_killed_live;
				drop table if exists oozie_jobs_running_live;
				''')
	print("Tables droped successfully")	

	cur.execute('''CREATE TABLE oozie_jobs_failed_live(
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

	cur.execute('''CREATE TABLE oozie_jobs_success_live(
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

	cur.execute('''CREATE TABLE oozie_jobs_killed_live(
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

	cur.execute('''CREATE TABLE oozie_jobs_running_live(
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
				
	cur.execute('''CREATE TABLE IF NOT EXISTS queue_live(
				 queueName VARCHAR (50),
				 max_memory  INT,
				 max_vCores  INT,
				 fair_memory  INT,
				 fair_vcores  INT,
				 used_memory  INT,
				 used_vcores  INT,
				 createdTime TIMESTAMP
				);''')	
				
	print("Tables created successfully")	

	print("Purging old data from the tables")
	
	cur.execute('''DELETE FROM queue_live WHERE to_char(createdTime,'yyyy-mm-dd') < to_char(now(),'yyyy-mm-dd')''')	
				
	i = 0
	for item in failed_json_array['workflows']:
		cur.execute("INSERT INTO oozie_jobs_failed_live VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (seqKey) DO NOTHING", (i, item['appName'] , item['run'], item['consoleUrl'], item['createdTime'], item['startTime'], item['endTime'], item['status'], item['user'], item['id']))
		i=i+1
		
	i = 0	
	for item in success_json_array['workflows']:
		cur.execute("INSERT INTO oozie_jobs_success_live VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (seqKey) DO NOTHING", (i, item['appName'] , item['run'], item['consoleUrl'], item['createdTime'], item['startTime'], item['endTime'], item['status'], item['user'], item['id']))
		i=i+1
		
	i = 0	
	for item in killed_json_array['workflows']:
		cur.execute("INSERT INTO oozie_jobs_killed_live VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (seqKey) DO NOTHING", (i, item['appName'] , item['run'], item['consoleUrl'], item['createdTime'], item['startTime'], item['endTime'], item['status'], item['user'], item['id']))
		i=i+1	
		
	i = 0	
	for item in running_json_array['workflows']:
		cur.execute("INSERT INTO oozie_jobs_running_live VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (seqKey) DO NOTHING", (i, item['appName'] , item['run'], item['consoleUrl'], item['createdTime'], item['startTime'], item['endTime'], item['status'], item['user'], item['id']))
		i=i+1
		

	cur.execute("INSERT INTO queue_live VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", ('rootQueue' , str(queue_json_array['scheduler']['schedulerInfo']['rootQueue']['maxResources']['memory'] ), str(queue_json_array['scheduler']['schedulerInfo']['rootQueue']['maxResources']['vCores']), str(queue_json_array['scheduler']['schedulerInfo']['rootQueue']['steadyFairResources']['memory']), str(queue_json_array['scheduler']['schedulerInfo']['rootQueue']['steadyFairResources']['vCores']), str(queue_json_array['scheduler']['schedulerInfo']['rootQueue']['usedResources']['memory']), str(queue_json_array['scheduler']['schedulerInfo']['rootQueue']['usedResources']['vCores']),datetime.datetime.now()))


	for item in queue_json_array['scheduler']['schedulerInfo']['rootQueue']['childQueues']['queue']:
		cur.execute("INSERT INTO queue_live VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (item['queueName'] , item['maxResources']['memory'] , item['maxResources']['vCores'], item['steadyFairResources']['memory'], item['steadyFairResources']['vCores'], item['usedResources']['memory'], item['usedResources']['vCores'],datetime.datetime.now()))
			
		
	conn.commit()
	print("Records inserted successfully")
	conn.close()
	failed_input_file.close()
	success_input_file.close()
	killed_input_file.close()
	queue_input_file.close()

Timer()