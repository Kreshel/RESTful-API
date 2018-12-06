from jobs import q, update_job_status, execute_job as execute

@q.worker
def execute_job(jid):
	# update job status
	update_job_status(jid, 'in_progress')
	
	# generate a graph from the data
	execute(jid)

	update_job_status(jid, 'completed')

execute_job()