# RNDM: React-Nginx-Django-Mysql boilerplate
Full-fledged Web 2.0 Single Page App boilerplate that is ready to be deployed as a containerized docker service

- continuous development using mounted volumes in docker containers
- production web server on gunicorn 
- MySQL db (ready to deploy with docker-compose)
- tested on python 3.6
- you define the project structure you want before the boilerplate is created, using a JSON config file (see `project_config.json`)
- `virtualenv` for development

# Usage
Clone this repo then run `setup.sh`:
```
git clone git@github.com:bluepropane/RNDM-boilerplate.git && cd RNDM-boilerplate 
./setup.sh
```

# Running the service
This section assumes you have docker-compose cli installed on your machine.

### Starting the development environment
```
docker-compose up
```
Then, fire up your browser and navigate to `localhost`.
By default, the nginx service binds the react dev server on port 3000 and the django dev server on port 8000. 

### Starting a production server with docker-compose
To initialize a production web server using docker-compose, run
```
docker-compose up -f docker-compose.yml -f docker-compose.production.yml
```
in the generated output `src` folder.