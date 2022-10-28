# groundsim

## Overview

Simulates a stream of groundstation telemetry which might typically be received during an overpass.

It's really a demo designed to showcase:

- modern python (3.10) incl FastAPI, Pydantic and Strawberry for GraphQL and HTTP apis
- docker for local development and cloud deployment
- typing via pylance, formatting via black and linting via flake8
- [choice of base image](https://pythonspeed.com/articles/base-image-python-docker-images/) and use of multistage build and venv to slim python
- unit and integration testing

If this were real I'd:

- add structured logging
- integrate with a gs provider & volume test
- provide cursor-based subscription so clients can better deal with backpressure
- swap out broadcaster & global var for for an event stream such as redis streams or kafka
- persist timeseries data in postgres with BRIN index or a specialised db (e.g. Timescale or Influx)
- pin docker image version and convert to an unprivileged container, [running rootless](https://docs.docker.com/engine/security/rootless/) (or use podman)
- run behind a reverse proxy like nginx and deploy on app runnner or k8s
- protect with oauth bearer tokens or an api key
- instrument the app via opentelemetry and monitor via prometheus/ grafana or elastic/ kibana

## To do:

- CI incl. running tests and linter
- CD to fly.io
- frontend

## Local quick start

Ensure docker-compose is available and docker is running, then:

```sh
# Build and run tests
docker build --target test -t test-api . && docker run -it test-api

# Run the api (uses default docker-compose.yml)
docker-compose up --build --force-recreate

# Debug the api (run then select python:attach from the vscode debug window)
docker-compose up --build --force-recreate -f docker-compose-debug.yml
```

Once the api is running, start the groundsim by POSTing the endpoint:

```sh
http POST http://localhost:8080/simulation
```

Open http://localhost:8080/graphql in a browser, then:

```graphql
# fetch the latest telemetry points in a single query
query {
  latestpoints {
    type
    timestamp
    value
  }
}

# subscribe to the stream of points
subscription {
  points {
    type
    timestamp
    value
  }
}
```
