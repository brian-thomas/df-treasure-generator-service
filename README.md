# df-treasure-generator-service

A service implementation for the GURPS Dungeon Fantasy Treasure 
Generator project, https://github.com/brian-thomas/df-treasure-generator.

This service may be called either from the command line 
as a local service or deployed to Heroku.

# Local Service

To use locally, install a new virtual machine using virtualenv.

> virtualenv -p <python3> <directory>
> source <directory>/bin/activate.sh

Next install the dependencies using pip, e.g.

> pip install -r requirements.txt

Now you can run the service locally, e.g.:

> python generator/service.py 

# Heroku Service

If you want deploy to Heroku (http://heroku.com), you will need to 
obtain an account, configure your environment and create a new 
service project to deploy this service to (see Heroku site 
documentation). 

