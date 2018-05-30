# DRMN: Django-React-Mysql-Nginx boilerplate
django 2 server boilerplate that is ready to be deployed to a docker container with python 3.6.

- production web server on gunicorn 
- MySQL backend (ready to deploy with docker-compose)
- python 3 only
- you define the project structure you want before the boilerplate is created, using a JSON config file (see `project_config.json`)
- virtualenv for development

# Usage
Clone this repo then run `start.sh`:
```
git clone git@github.com:bluepropane/DRMN-boilerplate.git && cd DRMN-boilerplate 
./start.sh
```

# Building for docker
Assumes you have docker cli installed on your machine.
```
docker build -t <desired image name> .
docker run -t <desired image name>
```

# Starting a production server with docker-compose
Assumes you have docker-compose cli installed on your machine.
To initialize a production web server using docker-compose, run
`
docker-compose up
`