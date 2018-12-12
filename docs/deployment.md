# Get Started with One Server


###First clone the repository
%git clone https://kreshel@bitbucket.org/kreshel/flask_api.git

###Then enter the directory
%cd flask_api

###Then build the necessary Docker image
%docker build -t kreshel/flask_api .

###Finally run the server
%docker-compose up


Congratulations! The server is online and you can now make requests.




# Get Started on Different Servers


###First clone the repository
%git clone https://kreshel@bitbucket.org/kreshel/flask_api.git

###Then enter the directory
%cd flask_api

###Then build the necessary Docker image
%docker build -t kreshel/flask_api .

###Then run the Flask API on one server
%docker-compose -f docker-compose-api.yml up

###Finally run the redis app on another server
%docker-compose -f docker-compose-jobs.yml up


Congratulations! You have the project online on multiple servers and can now make requests.