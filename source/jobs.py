from uuid import uuid4
from redis import StrictRedis
#from hotqueue import HotQueue
import time

rd = StrictRedis(host='172.17.0.1', port=6379, db=0)
#q = HotQueue("queue", host='172.17.0.1', port=6379, db=0)

def create_jid():
    return str(uuid4())

def create_job_key(jid):
    return 'job.{}'.format(jid)


def create_job(jid, status, start, end):
	seconds = time.time()
	M_D_YR = str(time.ctime(seconds))

	return {'id': jid,
			'status': status,
			'start': start,
			'end': end,
			'create_time': M_D_YR,
			'last_update _time': M_D_YR }

def add_job(start=1850, end=1979, status='submitted'):
	jid = create_jid()
	job_dict = create_job(jid, status, start, end)

	rd.hmset(create_job_key(jid), job_dict)

	return job_dict

# my add job/POST works but I cannot for the life of me make the GETs work
def get_job_by_id(jid):
	return rd.hgetall(create_job_key(jid))

def get_all_jobs():
	job_objects = []
	for key in rd.keys():
		item = rd.hgetall(key)
		for element in item:
			element = str(element)
		job_objects.append(item)
	return job_objects