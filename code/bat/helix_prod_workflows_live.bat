curl "<oozie_server_address>:11000/oozie/v2/jobs?offset=1&len=5000&filter=status%%3DSUCCEEDED" -o <path>\data\json\oozie_jobs_succeeded_live.json

curl "<oozie_server_address>:11000/oozie/v2/jobs?len=5000&filter=status%%3DFAILED" -o <path>\data\json\oozie_jobs_failed_live.json

curl "<oozie_server_address>:11000/oozie/v2/jobs?len=5000&filter=status%%3DKILLED" -o <path>\data\json\oozie_jobs_killed_live.json

curl "<oozie_server_address>:11000/oozie/v2/jobs?len=5000&filter=status%%3DRUNNING" -o <path>\data\json\oozie_jobs_running_live.json

curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET <name_node_address>:8088/ws/v1/cluster/scheduler/ -o <path>\data\json\queue_live.json
