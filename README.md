# groundsim

![Build & Test](https://github.com/followben/groundsim/actions/workflows/main.yml/badge.svg)

Simulate a stream of groundstation telemetry received during an overpass.

## Quick start

Open https://gs.fly.dev and press the button!

Or directly query the api with graphql or via https://gsapi.fly.dev/graphql:

```graphql
# subscribe to the stream of points
subscription {
  points {
    type
    timestamp
    value
  }
}

# run simulation
mutation {
  createSimulation
}

# fetch the latest telemetry points in a single query
query {
  latestpoints {
    type
    timestamp
    value
  }
}
```

Alternatively, use the REST api (here via [httpie](https://httpie.io/cli)):

```sh
# GET the latest telemetry points
http GET https://gsapi.fly.dev/latestpoints

# or POST to create the simulation
http POST https://gsapi.fly.dev/simulation
```

## What is this?

It's really a demo playground to showcase:

- modern python (3.10) incl FastAPI, Pydantic and Strawberry for GraphQL and HTTP apis
- docker for local development and cloud deployment
- typing via pylance, formatting via black and linting via flake8
- [choice of base image](https://pythonspeed.com/articles/base-image-python-docker-images/) and use of multistage build and venv to slim python
- unit and integration testing via pytest
- CI/ CD via Github Actions to

If this were real I'd:

- include linting/ static analysis as part of CI
- integrate with a gs provider & volume test
- provide cursor-based subscription so clients can better deal with backpressure
- swap out broadcaster & global var for for an event stream such as redis streams or kafka
- persist timeseries data in postgres with BRIN index or a specialised db (e.g. Timescale or Influx)
- pin docker image version and convert to an unprivileged container, [running rootless](https://docs.docker.com/engine/security/rootless/) (or use podman)
- run behind a reverse proxy like nginx and deploy on app runnner or k8s
- protect with oauth bearer tokens or an api key
- instrument via opentelemetry and add structured logging; then monitor via prometheus/ grafana or elastic/ kibana

## To do:

- graphql subscription for simulation state
- data vis in the frontend
- lose the second compose file for vscode
- api testing for subscriptions and mutations

## Local development

Ensure docker-compose is available and docker is running, then:

```sh
# Build and run backend tests
docker build --target apitest -t test-api . && docker run test-api

# Run the api on localhost:8080 and the frontend on localhost:3000
docker compose up --build --force-recreate

# Debug the api via localhost:8080 (run then select python:attach from the vscode debug window)
docker compose up --build --force-recreate -f docker-compose-debug.yml
```
