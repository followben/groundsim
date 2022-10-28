# groundsim

## Overview

Simulates a stream of groundstation telemetry which might typically be received during an overpass.

It's really a demo designed to showcase:

- modern python (3.10) incl FastAPI, Pydantic and Strawberry for GraphQL and HTTP apis
- docker for local development and cloud deployment
- typing via pylance, formatting via black and linting via flake8
- [choice of base image](https://pythonspeed.com/articles/base-image-python-docker-images/) and use of multistage build and venv to slim python
- (to come) structured logging, unit and integration testing

If this were real I'd:

- integrate with a gs provider & volume test
- swap out broadcaster & global var for for an event stream such as redis streams or kafka
- persist timeseries data in postgres with BRIN index or a specialised db (e.g. Timescale or Influx)
- pin docker image version and convert to an unprivileged container, [running rootless](https://docs.docker.com/engine/security/rootless/) (or use podman)
- run behind a reverse proxy like nginx and deploy on app runnner or k8s
- instrument the app via opentelemetry and monitor via prometheus/ grafana or elastic/ kibana

## To do:

- test queries
- add structured logging
- better docs
- frontend
- deploy on fly.io
- CI/ CD incl. running tests and linter

## Local quick start

Ensure docker-compose is available and docker is running, then:

```sh
# Build and run tests
docker build --target test -t test-api . && docker run -it test-api

# Run the application (uses default docker-compose.yml)
docker compose up

# Debug the application (run then select python:attach from the vscode debug window)
docker compose up -f docker-compose-debug.yml
```
