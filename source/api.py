from flask import Flask,jsonify,request
import json
import jobs
from data import get_data


app = Flask(__name__)

@app.route('/rainfall', methods=['GET'])
def get_rainfall():

	dict_class = get_data()

	# tests if both start/end and limit/offset used together
	if ('start' in request.args or 'end' in request.args) and ('limit' in request.args or 'offset' in request.args):
		return jsonify({'msg':'Please do not use start/end with limit/offset'}), 400

	# if start/end provided, returns appropriate data
	if 'start' in request.args or 'end' in request.args:
		start = None
		end = None
		if 'start' in request.args:
			try:
				start = int(request.args.get('start'))
			except:
				return jsonify({'msg':'Please Enter a Valid Start'}), 400
		
		if 'end' in request.args:
			try:
				end = int(request.args.get('end'))
			except:
				return jsonify({'msg':'Please Enter a Valid End'}), 400

		return jsonify(dict_class.in_between(start=start,end=end).data)

	# if limit/offset provided, returns appropriate data
	if 'limit' in request.args or 'offset' in request.args:
		limit = None
		offset = None

		if 'limit' in request.args:
			try:
				limit = int(request.args.get('limit'))
			except:
				return jsonify({'msg':'Please Enter a Valid Limit'}), 400

		if 'offset' in request.args:
			try:
				offset = int(request.args.get('offset'))
			except:
				return jsonify({'msg':'Please Enter a Valid Offset'}), 400

		return jsonify(dict_class.limset(limit=limit,offset=offset).data)

	return jsonify(dict_class.data)


@app.route('/rainfall/<idnum>', methods=['GET'])
def get_rainfall_by_id(idnum=None):

	dict_class = get_data()

	try:
		idnum = int(idnum)
		try:
			return jsonify(dict_class.data[idnum])
		except:
			return jsonify({'msg':'Integer out of bounds'}), 400
	except:
		return jsonify({'msg':'Please enter an integer'}), 400


@app.route('/rainfall/year/<yearnum>', methods=['GET'])
def get_rainfall_by_year(yearnum=None):

	dict_class = get_data()

	try:
		yearnum = int(yearnum)
		try:
			index = dict_class.valid_dates().index(yearnum)
			return jsonify(dict_class.data[index])
		except:
			return jsonify({'msg':'Please enter a valid year'}), 400
	except:
		return jsonify({'msg':'Please enter an integer'}), 400
###########

### jobs ###
@app.route('/jobs', methods=['GET', 'POST'])
def jobs_api():
	'''
	try:
		job = request.get_json(force=True)
	except Exception as e:
		return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})

	return json.dumps(jobs.add_job(job['start'], job['end']))
	'''
	if request.method == 'POST':
		try:
			job = request.get_json(force=True)
		except Exception as e:
			return json.dumps({'status':'Error', 'message': 'Invalid JSON: {}.'.format(e)})

		# tests if both start/end and limit/offset used together
		if ('start' in job or 'end' in job) and ('limit' in job or 'offset' in job):
			return jsonify({'msg':'Please do not use start/end with limit/offset'}), 400

		# if start/end provided, posts appropriate job
		if 'start' in job or 'end' in job:
			start = None
			end = None
			if 'start' in job:
				try:
					start = int(job['start'])
				except:
					return jsonify({'msg':'Please Enter a Valid Start'}), 400
			
			if 'end' in job:
				try:
					end = int(job['end'])
				except:
					return jsonify({'msg':'Please Enter a Valid End'}), 400

			return json.dumps(jobs.add_job(start, end))

		# if limit/offset provided, posts appropriate job
		if 'limit' in job or 'offset' in rjob:
			limit = None
			offset = None
			# converts start/limit to start/end
			start = 1850
			end = 1979

			if 'offset' in job:
				try:
					offset = int(job['offset'])
					start = start+offset
				except:
					return jsonify({'msg':'Please Enter a Valid Offset'}), 400

			if 'limit' in job:
				try:
					limit = int(job['limit'])
					end = start+limit
				except:
					return jsonify({'msg':'Please Enter a Valid Limit'}), 400

			return json.dumps(jobs.add_job(start, end))

		# makes job with all data if no parameters provided
		return json.dumps(jobs.add_job())


	if request.method == 'GET':
		data = jobs.get_all_jobs()

		return json.dumps(data)

# Retrieves/deletes job from redis by jid
@app.route('/jobs/<jid>', methods=['GET','DELETE'])
def get_job_by_jid(jid=None):

	if request.method == 'GET':
		try:
			return json.dumps(jobs.get_job_by_jid(jid))
		except:
			return jsonify({'msg':'Job does not exist'}), 400
	
	if request.method == 'DELETE':
		jobs.delete_by_jid(jid)

		return json.dumps({'msg':'Job {} successfully deleted'.format(jid)})


# Returns a plot created by the worker 
@app.route('/jobs/<job_id>/plot', methods=['GET'])
def job_plot(job_id):
	plot = jobs.get_job_plot(job_id)
	try:
		return json.dumps({'status': 'Success', 'message': plot})
	except Exception as e:
		return json.dumps({'status': "Error", 'message': e})
############




if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')