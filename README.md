# RNDM: React-Nginx-Django-Mysql boilerplate
Full-fledged Web 2.0 Single Page App boilerplate that is ready to be deployed as a containerized docker application

- continuous development using mounted volumes in docker containers
- production web server on [gunicorn](http://gunicorn.org/)
- MySQL db (ready to deploy with docker-compose)
- python 3.6/django 2.0
- you define the project structure you want before the boilerplate is created, using a JSON config file (see `rndm_conf.json`)
- `virtualenv` for development

## Introduction
RNDM was built with the following objectives in mind:
- **Replicability & Portability**
- **Rapid prototyping (hackathons, MVP, etc):** RNDM wires up the entire web stack from the start so that you/your development team can focus on building the API and web interface.

## Requirements
RNDM has been tested on the following setup:
- Docker ^18.03
- docker-compose ^1.12.1

The following are optional; having them would increase development efficiency
- Python 3.6, pip 9.0.1
- Node.js >= 7, npm >= 5

Server instance requirements 

## Usage
Clone this repo then run `setup.sh`:
```
git clone git@github.com:bluepropane/rndm.git && cd rndm
./setup.sh
```

## Running the service
This section assumes you have docker-compose cli installed on your machine.

### Starting the development environment
```
docker-compose up
```
Then, fire up your browser and navigate to [http://localhost](`http://localhost`).
By default, the nginx service binds the react dev server on port 3000 and the django dev server on port 8000.

In the development environment, there should be 4 services running:
- `nginx`
- `web`
- `server`
- `db`
The `web` service runs the webpack development server so that hot reloading is enabled.


### Starting a production server with docker-compose
To initialize a production web server using docker-compose, run
```
docker-compose up -f docker-compose.yml -f docker-compose.production.yml
```
in the generated output `src` folder.

In the production environment, the `web` service is not required as the frontend code is bundled in a build and placed in the server image. Services running:
- `nginx`
- `server`
- `db`
