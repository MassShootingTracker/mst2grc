# GunsAreCool update from MassShootingTracker website. 

## Setup 

### Running as Container (preferred)

#### 1. Install Docker and docker-compose
    
Installation and use of these tools is beyond the scope of these instructions

#### 2. Create a config.json

Copy config.json.example and update the api-key, google doc urls, and OAuth credentals for the reddit bot. 

#### 3. Create docker-compose.yml

Copy deploy-tools/docker-compose.yml into the directory as your config.json. If needed change the port of the service.   This container uses a gunicorn webserver, a reverse proxy from nginx is recommended. 

#### 4. Run the container. 

Start the service with `docker-compose up`.  You can add the option `-d` to start it daemon mode.  docker-compose will download the lastest container from dockerhub if needed and start the service with the configuration found in your config.json. 

### Running on Host.

#### 1. Install
   
Clone project to a directory. Optionally create a virtualenv with setuptools.  Run setup.py to install the requirements.  

#### 2. create config.json

Copy config.json.example to config.json and change your subreddit, OAuth2 credentias and supply urls to Google sheets. 

The script looks for config.json in the root directory.   You can change the location and name by storing a full path in the `MSTGRC_CFG` environment variable.  

#### 2. Run in Dev Mode

You can either run wsgi.py which starts a local webserver at `http://127.0.0.1:5000` or run mst2grc directly.  

#### 3. Run in production

This requires a webserver with a properly configured wsgi module, such as mod_wsgi/Apachi or gunicorn/nginx. The setup of these are beyond the scope of these instructions. 

A sample bottle wsgi script can be found in wsgi.py.  #### 4. Navigate to endpoint and refresh from google docs. 

    http://[url]:[port]/update/grc?key=[api key]&year=[year]

From a bash command line:

    curl --data "key=[key from environment variable]&year=[year to update]" http://[url]:[port]/update/grc
    
To update all years, omit `year`.  The api-key is stored in an environment variable `MSTGRC_KEY`, otherwise it defaults to none. 

