import civis
import os
client = civis.APIClient()

script_id = os.environ.get("CIVIS_JOB_ID")
run_id = os.environ.get("CIVIS_RUN_ID")
file_id = 134753755

client.post_containers_runs_outputs(script_id, run_id, "File", file_id)
