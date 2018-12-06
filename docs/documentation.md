
# Accessing through Curl/Python
## Curl Example
An example of how to use this API from the command line.

### GET/POST/DELETE rainfall/jobs
Insert appropriate METHOD (GET, POST, DELETE). Use the brackets with POST requests, otherwise ignore

	%curl -X <METHOD> [--data '{"start":"1850","end":"1979"}'] "http://localhost:5000/rainfall"

		[
		  {
			"Annual rainfall at fortaleza": 852.0, 
			"Year": 1850.0, 
			"id": 0
		  }, 
		  {
			"Annual rainfall at fortaleza": 1806.0, 
			"Year": 1851.0, 
			"id": 1
		  }, 
		  .
		  .
		  .
		  {
			"Annual rainfall at fortaleza": 996.0, 
			"Year": 1979.0, 
			"id": 129
		  }
		]

### GET jobs/<job_id>/plot
Will download a plot image into working directory

	%curl --output <file_name.png> localhost:5000/jobs/<jid>/plot


## Python Example
An example of how to use this API from Python.

### GET
	import requests
	r = requests.get(url='http://localhost:5000/rainfall')
	assert r.status_code == 200
	return r.content

		[
		  {
			"Annual rainfall at fortaleza": 852.0, 
			"Year": 1850.0, 
			"id": 0
		  }, 
		  {
			"Annual rainfall at fortaleza": 1806.0, 
			"Year": 1851.0, 
			"id": 1
		  }, 
		  .
		  .
		  .
		  {
			"Annual rainfall at fortaleza": 996.0, 
			"Year": 1979.0, 
			"id": 129
		  }
		]

### POST
	import requests
	r = requests.post(url='http://localhost:5000/jobs', data={"start":"1880","end":"1900"})
	assert r.status_code == 200
	return r.content

		{
			"id": "25cdb58e-e802-489b-89e1-2cb7813dccd8", 
			"status": "submitted", 
			"start": 1880, 
			"end": 1900, 
			"plot": "NULL"}
		}

### DELETE
	import requests
	r = requests.delete(url='http://localhost:5000/jobs/<jid>)
	assert r.status_code == 200
	return r.content

		{
			"msg": "Job 25cdb58e-e802-489b-89e1-2cb7813dccd8 successfully deleted"
		}

# Documentation
## Retrieving Rainfall Data
### GET /rainfall


This endpoint retrieves all available data for rainfall in Fortaleza, Brazil.

GET /rainfall

		[
		  {
			"Annual rainfall at fortaleza": 852.0, 
			"Year": 1850.0, 
			"id": 0
		  }, 
		  {
			"Annual rainfall at fortaleza": 1806.0, 
			"Year": 1851.0, 
			"id": 1
		  }, 
		  .
		  .
		  .
		  {
			"Annual rainfall at fortaleza": 996.0, 
			"Year": 1979.0, 
			"id": 129
		  }
		]


##### Query Parameters
Start/end may be used together and limit/offset may be used together, but cross combinations are not allowed.

	start: integer, optional
		Retrieves data points starting at 'start' year
	end: integer, optional
		Retrieves data points ending at 'end' year

	limit: integer, optional
		Retrieves up to n='limit' data points 
	offset integer, optional
		Retrieves data points starting at index 'offset'


GET /rainfall?limit=2&offset=3

		[
		  {
			"Annual rainfall at fortaleza": 1233.0, 
			"Year": 1853.0, 
			"id": 3
		  }, 
		  {
			"Annual rainfall at fortaleza": 1590.0, 
			"Year": 1854.0, 
			"id": 4
		  }
		]


### GET /rainfall/<id_num>

This endpoint retrieves the rainfall data for index 'idnum'.


GET /rainfall/10

		{
		  "Annual rainfall at fortaleza": 1114.0, 
		  "Year": 1950.0, 
		  "id": 100
		}


### GET rainfall/year/<year_num>


This endpoint returns the rainfall data for year 'yearnum'.


GET /rainfall/year/1893

		{
		  "Annual rainfall at fortaleza": 1430.0, 
		  "Year": 1893.0, 
		  "id": 43
		}


## Retrieving Jobs/Plots
### GET jobs

This endpoint allows the client to retrieve all available jobs.

GET /jobs

	{
		[
			{
				"id": "5b6a0b60-13b7-426a-997b-b0330ee4c961", 
				"status": "in_progress", 
				"start": "1880", 
				"end": "1900", 
				"plot": "NULL"
			}
			.
			.
			.
			{
				"id": "cbaa1e0d-17c8-4ae8-a881-4bc356892f53", 
				"status": "in_progress", 
				"start": "1880", 
				"end": "1950", 
				"plot": "NULL"
			}
		]
	}

### POST jobs

This endpoint allows the client to post a job request.

POST /jobs

		{
			"id": "25cdb58e-e802-489b-89e1-2cb7813dccd8", 
			"status": "submitted", 
			"start": 1880, 
			"end": 1950, 
			"plot": "NULL"}
		}

### GET jobs/<job_id>

This endpoint allows the client to retrieve the status on a job by id.

GET /jobs/<job_id>

		{
			"id": "25cdb58e-e802-489b-89e1-2cb7813dccd8", 
			"status": "in_progress", 
			"start": "1880", 
			"end": "1950", 
			"plot": "NULL"
		}

### DELETE jobs/<job_id>

This endpoint allows the client to delete a job by id.

DELETE /jobs/<job_id>

		{
			"msg": "Job 25cdb58e-e802-489b-89e1-2cb7813dccd8 successfully deleted"
		}

### GET jobs/<job_id>/plot

This endpoint allows the client to retrieve a plot job.

	GET /jobs/<job_id>/plot

		{
		}