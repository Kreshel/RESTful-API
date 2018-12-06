from uuid import uuid4
from redis import StrictRedis
#from hotqueue import HotQueue
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

'''
I wasn't sure exactly how to implement code so I drew some inspiration from Carrie's
Please look at previous iterations of this for original source code.
'''

rd = StrictRedis(host='172.17.0.1', port=6379, db=0)
#q = HotQueue("queue", host='172.17.0.1', port=6379, db=0)

# creates a unique id for job
def _create_jid():
    return str(uuid4())

# adds a 'job. in front of jid to use as a key
def _create_job_key(jid):
    return 'job.{}'.format(jid)

# creates a job dictionary object with metadata
def _create_job(jid, status, start, end, plot):
	if type(jid) == str:
    return {'id': jid,
                'status': status,
                'start': start,
                'end': end,
                'plot': plot}

    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'start': start.decode('utf-8'),
            'end': end.decode('utf-8'),
            'plot': plot.decode('utf-8')}

# retrieves job using job key
def _get_job_by_job_key(job_key):
	jid, status, start, end = rd.hmget(job_key, 'id', 'status', 'start', 'end', 'plot')
    if jid:
        return _create_job(jid, status, start, end, plot)
    return None

# retrieves job using jid
def get_job_by_jid(jid):
	return _get_job_by_job_key(_create_job_key(jid))

# retrieves all available jobs
def get_all_jobs():
	job_objects = []
	for job_key in rd.keys():
		job_objects.append(_get_job_by_job_key(job_key))

	return job_objects

# Adds a job to redis queue
def add_job(start=1850, end=1979, status='submitted'):
	jid = _create_jid()
	job_dict = _create_job(jid, status, start, end)

	rd.hmset(_create_job_key(jid), job_dict)
	queue_job(jid)

	return job_dict

# updates job in redis with new status
def update_job_status(jid, status):
    job_dict = get_job_by_id(jid)
    if job_dict:
        job_dict['status'] = status
        rd.hmset(_create_job_key(jid), job_dict)
    else:
        raise Exception()

# deletes a job off of redis queue
def delete_by_id(jid):
    rd.delete(_create_job_key(jid))


# Queue --

def queue_job(jid):
    q.put(jid)

def finalize_job(jid, file_path):
    """Update the job in the db with status and plot once worker has completed it."""
    job = get_job_by_id(jid)
    job['status'] = COMPLETE_STATUS
    job['plot'] = open(file_path, 'rb').read()
    rd.hmset(jid, job)

def get_job_plot(jid):
    """Returns the plot, as binary data, associated with the job"""
    job = get_job_by_id(jid)
    if not job['status'] == COMPLETE_STATUS:
        return True, "job not complete."
    return False, rd.hmget(jid, 'plot')

# Execute worker
def execute_job(jid):
    """Execute the job. This is the callable that is queued and worked on asynchronously."""
    job = get_job_by_id(jid)
    points = get_data(job['start'], job['end'])
    years = [int(p['year']) for p in points]
    population = [p['population'] for p in points]
    plt.scatter(years, population)
    tmp_file = '/tmp/{}.png'.format(jid)
    plt.savefig(tmp_file, dpi=150)
    finalize_job(jid, tmp_file)







