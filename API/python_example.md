
An example of how to use this API from Python.


	import requests
	r = requests.get(url='http://localhost:5000/rainfall')
	data = r.json()

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