# GS Simulator

## Overview

This app simulates a stream of telemetry that might typically be received from a groundstation during a satellite overpass.

It's a demo to showcase:

- modern python (3.10) incl FastAPI, Pydantic and Strawberry for GraphQL and HTTP apis
- docker for local development and cloud deployment

A few highlights:

- typing via pylance, formatting via black and linting via flake8
- (choice of base image)[https://pythonspeed.com/articles/base-image-python-docker-images/] and use of multistage build and venv to slim python
- (to come) structured logging, unit and integration testing

If this were real I'd:

- integrate with a gs provider & volume test
- swap out broadcaster & global var for for an event stream such as redis streams or kafka
- persist timeseries data in postgres with BRIN index or a specialised db (e.g. Timescale or Influx)
- pin docker image version and convert to an unprivileged container, (running rootless)[https://docs.docker.com/engine/security/rootless/] (or use podman)
- run behind a reverse proxy like nginx and deploy on app runnner or k8s
- instrument with opentelemetry and monitor via prometheus/ grafana or elastic/ kibana

## To do:

- structured logging
- pytest
- deploy on fly.io
- CI/ CD incl. running tests and linter
- frontend
- better docs

## Local quick start

Ensure docker is running & you have docker-compose, then:

```sh
docker compose up
```
