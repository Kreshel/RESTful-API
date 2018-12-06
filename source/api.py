from flask import Flask,jsonify,request
import json
import jobs

### HW 1 ###
class TimeSeriesDict:

	def __init__(self, fileName):
	# takes input string fileName
	# opens a file with 2 columns and adds its data to a dictionary
		self.file = fileName
		with open(self.file,'r') as f:
			self.header = f.readline().strip().split(',')
			# stores the headers as strings
			for i in range(len(self.header)):
				self.header[i]=self.header[i].strip('"')

			# deletes extraneous header material (should only have 2)
			while len(self.header)>2:
				self.header.pop()
			self.data = []
		
			num = 0
			for line in f:
				x = line.strip().split(',')
				self.data.append({'id':num, self.header[0]:float(x[0].strip('"')), self.header[1]:float(x[1].strip('"'))})
				num=num+1

		# creation of valid dates, limits, and offsets
		self.valDates=[]
		for i in range(len(self.data)):
			self.valDates.append(self.data[i][self.header[0]])
		self.valLimit=len(self.data)
		self.valOffset=len(self.data)


	# "prints" the class
	def show(self):
		print(self.data)

	# prints the header
	def head(self):
		return self.header

	def valid_dates(self):
		return self.valDates

	def valid_limit(self):
		return self.valLimit

	def valid_offset(self):
		return self.valOffset


	def in_between(self, start=None, end=None):
		newTSD = TimeSeriesDict(self.file)
		#columnTwoHeader = list(self.data[0])[1]
		c2Header = self.header[0] # gets the header for column two

		# applies if no input/start before first date/end is first date
		if start==None or start<=self.data[0][c2Header] or end==self.data[0][c2Header]:
			start = self.data[0][c2Header]
		# applies if no input/end after last date/start is last date/end is before start
		if end==None or end>self.data[-1][c2Header] or start ==self.data[-1][c2Header] or end<start:
			end = self.data[-1][c2Header]

		# pops off until start<-->end
		while( newTSD.data[0][c2Header]!=start ):
			newTSD.data.pop(0)
		while( newTSD.data[-1][c2Header]!=end ):
			newTSD.data.pop()

		return newTSD


	def limset(self, limit=None, offset=None):
		newTSD = TimeSeriesDict(self.file)

		# applies if no input/limit higher than length/negative limit
		if limit==None or limit>len(self.data) or limit < 0:
			limit = len(self.data)
		# applies if no input/negative offset
		if offset==None or offset < 0:
			offset = 0
		# applies if offset higher than length
		if offset>len(self.data):
			offset = len(self.data)

		# messy way to pop off to offset
		for i in range(0,int(offset)):
			newTSD.data.pop(0)
		# messy way to pop off until limit
		while( len(newTSD.data)>limit ):
			newTSD.data.pop()

		return newTSD
############

### HW 3 ###
app = Flask(__name__)


def get_data():
	return TimeSeriesDict('data/annual-rainfall-fortaleza-brazil.csv')


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
	# error stuff I used to check
	return jsonify(request.args)
	return str(type(request.args)) +'\n\n\n'


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
def get_rainfall_byyear(yearnum=None):

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
			return True, json.dumps({'status':'Error', 'message': 'Invalid JSON: {}.'.format(e)})

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

@app.route('/jobs/<jid>', methods=['GET'])
def get_job_by_id(jid=None):

	try:
		return json.dumps(jobs.get_job_by_id(jid))
	except:
		return jsonify({'msg':'Job does not exist'}), 400
############




if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')