# Get Started

%docker pull kreshel/flask_api

%docker-compose up


### Curl Example


An example of how to use this API from the command line.


	%curl "http://localhost:5000/rainfall"

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


### Python Example


An example of how to use this API from Python.


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

	GET jobs/
	{
	}

### GET jobs/<job_id>

This endpoint allows the client to retrieve the status on a job by id.

	GET jobs/<job_id>
		{
		}


### POST jobs

This endpoint allows the client to post a job request.

	POST /jobs
		{
		}
