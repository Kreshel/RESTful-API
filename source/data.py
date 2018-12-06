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

	# tests for correcct start/end
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

	# tests for correct limit/offset
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

def get_data():
	return TimeSeriesDict('data/annual-rainfall-fortaleza-brazil.csv')