Quick start

Ensure docker is running & you have docker-compose

docker compose up

TODO:

- pytest
- sense check typing everywhere
- CI/ CD incl. tests and linting for flake8
- Write up overview production deployment and enhancements
- Frontend

Overview

- choice of image (https://pythonspeed.com/articles/base-image-python-docker-images/)
- use of multistage build
  - use venv to slim python

Productionise

- Pin docker image version
- Run behind a reverse proxy like nginx
- Deploy on app runnner or k8s
- Use secrets rather than env for database secrets
- Monitoring

Enhancements

- Volume test
- BRIN index or use a Timeseries db (e.g. Timescale)
- Structured logging
- Convert to an unprivileged container and run docker rootless (https://docs.docker.com/engine/security/rootless/) or use podman
