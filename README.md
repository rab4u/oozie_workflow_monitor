Contents

1. Introduction
2. Architecture
3. Installation & Usage
4. References

# oozie_workflow_monitor
Oozie Workflow Monitor is a simple,insightful &amp; agent less live dashboard for monitoring the Oozie workflows. It is packed with eye catching widgets to monitor the workflow performance, success rate, failure rate and long running workflows that helps to make some quick decisions to tune the workflows and cluster. With web-based dashboard we can easily and seamlessly view the dashboard anywhere and share the results across the teams
# Live Dashbaord 
![](images/live_dashboard.png)
# Monthy Trend
![](images/monthly_trend_dashboard.png)
# High Level Architecture
Helix Oozie Workflow Monitor uses all the open source and light weight components and it can run on any commodity system. 

Main Components :
1. Python ( As a ETL Tool)
2. PostgreSQLPortable (As a DB)
3. Grafana (The open platform for beautiful analytics and monitoring)

![](images/high_architecture.png)
# Installation & Usage
Installation and setup is straight forward, Just follow the below steps

Steps
1. Installing python - Download the latest Python distributions (I used Anaconda, as it comes with most of the libs and tools required)
https://www.anaconda.com/download/

2. please download all the files and directories in /code directory, extract and place it in any of the directory you wish and changes the respective paths in get_monthly_workflows_data.bat file and get_live_workflows_data.bat


3. Installing postgresql portable.
Download the zip file and extract : https://sourceforge.net/projects/postgresqlportable/
after extracting the start the postgreSQL by clicking : PostgreSQLPortable application
Create DB with name helix_prod_oozie_jobs_db ( cmd :  CREATE DATABASE oozie_jobs_db )

4. Run the python code : import_oozie_data.py.
Currently the refresh rate is to 5 mins. you can change refresh rate by modifying the following line of code in the python script : threading.Timer(300.0, Timer).start() 
cmd : python import_oozie_data.py

5. Now, its time to setup the dashboard
Installing grafana -  Download and install from the following link : http://docs.grafana.org/installation/windows/
please follow the link to import Helix Oozie Workflows Monitoring dashboard. 
http://docs.grafana.org/features/export_import/#import
Import the following json files persent in the directory /grafana_oozie_dashboards

6. Open the dashboard : http://localhost:9009/ 
Default credentials (admin, admin)
You're done. Hurray (smile)
