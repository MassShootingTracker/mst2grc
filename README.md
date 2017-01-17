# GunsAreCool update from MassShootingTracker website. 

## Setting up the project

### 1. Install
   
Clone project to a directory. Optionally create a virtualenv with setuptools.  Run setup.py to install the requirements.  

### 2. create config.json

Copy config.json.example to config.json and change your subreddit, OAuth2 credentias and supply urls to Google sheets. 

The script looks for config.json in the root directory.   You can change the location and name by storing a full path in the `MSTGRC_CFG` environment variable.  

### 2. Run in Dev Mode

You can either run wsgi.py which starts a local webserver at `http://127.0.0.1:5000` or run mst2grc directly.  

### 3. Run in production

This requires a webserver with a properly configured wsgi module, such as mod_wsgi/Apachi or gunicorn/nginx. The setup of these are beyond the scope of these instructions. 

A sample bottle wsgi script can be found in wsgi.py.
 
### 4. Navigate to endpoint and refresh from google docs. 

    http://[url]:[port]/update/grc?key=[api key]&year=[year]

From a bash command line:

    curl --data "key=[key from environment variable]&year=[year to update]" http://[url]:[port]/update/grc
    
To update all years, omit `year`.  The api-key is stored in an environment variable `MSTGRC_KEY`, otherwise it defaults to none. 

