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
CONFIGURING IPsCONFIGURING IPsCONFIGURING IPsCONFIGURING IPsCONFIGURING IPsCONFIGURING IPs
###Then run the API on one server
%docker-compose-api up

###Finally run the Jobs on another server
%docker-compose-jobs up


Congratulations! You have the project online on multiple servers and can now make requests.