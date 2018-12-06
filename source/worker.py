#from jobs import q, update_job_status, IN_PROGRESS, COMPLETE_STATUS, execute_job as execute
import jobs

@q.worker
def execute_job(jid):
    # update job status
    update_job_status(jid, IN_PROGRESS)
    
    # generate a graph from the data
    execute(jid)

    update_job_status(jid, COMPLETE_STATUS)

execute_job()