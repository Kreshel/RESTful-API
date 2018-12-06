from uuid import uuid4
from redis import StrictRedis
from hotqueue import HotQueue
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import os
from data import get_data

'''
I wasn't exactly sure for some parts since I missed class 
so I drew some inspiration from Carrie's.
Please look at previous iterations of this for original source code.
'''

#
REDIS_IP = os.environ.get('REDIS_IP', '172.17.0.1')
try:
	REDIS_PORT = int(os.environ.get('REDIS_PORT'))
except:
	REDIS_PORT = 6379

# Redis DBs
DATA_DB = 0
QUEUE_DB = 1

rd = StrictRedis(host=REDIS_IP, port=REDIS_PORT, db=DATA_DB)
q = HotQueue("queue", host=REDIS_IP, port=REDIS_PORT, db=QUEUE_DB)

#rd = StrictRedis(host='172.17.0.1', port=6379, db=0)
#q = HotQueue("queue", host='172.17.0.1', port=6379, db=0)

# creates a unique id for job
def _create_jid():
	return str(uuid4())

# adds a 'job. in front of jid to use as a key
def _create_job_key(jid):
	return 'job.{}'.format(jid)

# creates a job dictionary object with metadata
def _create_job(jid, status='NULL', start=1850, end=1979, plot='NULL'):
	if type(jid) == str:
		return {'id': jid,
				'status': status,
				'start': start,
				'end': end,
				'plot': plot
		}
	return {'id': jid.decode('utf-8'),
			'status': status.decode('utf-8'),
			'start': start.decode('utf-8'),
			'end': end.decode('utf-8'),
			'plot': plot.decode('utf-8')
	}
# retrieves job using job key
def _get_job_by_job_key(job_key):
	jid, status, start, end, plot = rd.hmget(job_key, 'id', 'status', 'start', 'end', 'plot')
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

def queue_job(jid):
	q.put(jid)

def finalize_job(jid, file_path):
	"""Update the job in the db with status and plot once worker has completed it."""
	job = get_job_by_id(jid)
	job['status'] = 'completed'
	job['plot'] = open(file_path, 'rb').read()
	rd.hmset(jid, job)

def get_job_plot(jid):
	"""Returns the plot, as binary data, associated with the job"""
	job_dict = get_job_by_id(jid)
	if not job_dict['status'] == 'completed':
		return "job not complete."
	return rd.hmget(jid, 'plot')

# Execute worker
def execute_job(jid):
	"""Execute the job. This is the callable that is queued and worked on asynchronously."""
	job_dict = get_job_by_id(jid)
	#points = get_data(job['start'], job['end'])
	#years = [int(p['year']) for p in points]
	#population = [p['population'] for p in points]
	#plt.scatter(years, population)
	points = get_data(job_dict['start'], job['end'])
	years = [int(p['Year']) for p in points]
	rainfall = [p['Annual rainfall at fortaleza'] for p in points]
	plt.scatter(years,rainfall)

	tmp_file = '/tmp/{}.png'.format(jid)
	plt.savefig(tmp_file, dpi=150)
	finalize_job(jid, tmp_file)







