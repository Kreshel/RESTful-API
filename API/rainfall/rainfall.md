# GET /rainfall #


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



#Query Parameters#
Start/end may be used together and limit/offset may be used together, but cross combinations not allowed.

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