from uuid import uuid4
from redis import StrictRedis
from hotqueue import HotQueue
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import os
from data import get_data

'''
I wasn't exactly sure for parts since I missed class 
so I drew some inspiration from Carrie's.
Please look at previous iterations of this for "original" source code.
'''

# Environment setup
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

# adds a 'job.' in front of jid to use as a key
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
			'plot': plot
	}

# retrieves job using job key
def _get_job_by_job_key(job_key):
	jid, status, start, end, plot = rd.hmget(job_key, 'id', 'status', 'start', 'end', 'plot')
	if plot:
		plot = 'True'
	else:
		plot = 'False'
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

# Adds a job to redis db
def add_job(start=1850, end=1979, status='submitted'):
	jid = _create_jid()
	job_dict = _create_job(jid, status, start, end)

	rd.hmset(_create_job_key(jid), job_dict)
	queue_job(jid)

	return job_dict

# updates job in redis with new status
def update_job_status(jid, status):
	job_dict = get_job_by_jid(jid)
	if job_dict:
		job_dict['status'] = status
		rd.hmset(_create_job_key(jid), job_dict)
	else:
		raise Exception()

# deletes a job off of redis db
def delete_by_jid(jid):
	rd.delete(_create_job_key(jid))

def queue_job(jid):
	q.put(jid)

# puts the plot into redis db once it's completed
def finalize_job(jid, file_path):
	job = get_job_by_jid(jid)
	job['status'] = 'completed'
	job['plot'] = open(file_path, 'rb').read()
	rd.hmset(jid, job)

# retrieves plot as binary data
def get_job_plot(jid):
	job_dict = get_job_by_jid(jid)
	if not job_dict['status'] == 'completed':
		return "job not complete."
	return rd.hmget(jid, 'plot')

# job that the worker executes (creates plots)
def execute_job(jid):
	job_dict = get_job_by_jid(jid)

	points = get_data()
	points = points.in_between(start=int(job_dict['start']), end=int(job_dict['end'])).data
	years = [int(p['Year']) for p in points]
	rainfall = [p['Annual rainfall at fortaleza'] for p in points]
	plt.scatter(years,rainfall)
	plt.title(_create_job_key(jid))
	plt.xlabel('Year')
	plt.ylabel('Rainfall (mm)')

	tmp_file = '/tmp/{}.png'.format(jid)
	plt.savefig(tmp_file, dpi=150)
	finalize_job(jid, tmp_file)







