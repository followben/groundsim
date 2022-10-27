# GS Simulator

## Overview

This app simulates groundstation telemetry that might be typically received during a satellite overpass.

It employs:

- modern python (3.10) incl FastAPI, Pydantic and Strawberry for GraphQL and HTTP apis
- docker for local development and cloud deployment

A few highlights:

- structured logging, unit and integration testing
- (choice of base image)[https://pythonspeed.com/articles/base-image-python-docker-images/] and use of multistage build and venv to slim python

If this were real I'd:

- integrate with a gs provider & volume test
- swap out broadcaster for redis streams or kafka for event streaming
- persist timeseries data in postgres with BRIN index or a specialised db (e.g. Timescale or Influx)
- pin docker image version and convert to an unprivileged container, (running rootless)[https://docs.docker.com/engine/security/rootless/] (or use podman)
- run behind a reverse proxy like nginx and deploy on app runnner or k8s
- setup monitoring with an apm solution like datadog or sentry

## To do:

- structured logging
- pytest
- sense check typing everywhere
- CI/ CD incl. tests and linting for flake8
- Frontend

## Local quick start

Ensure docker is running & you have docker-compose, then:

```sh
docker compose up
```
