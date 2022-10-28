# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster AS base
WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN /opt/venv/bin/pip install --upgrade pip setuptools wheel
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


FROM base AS test
WORKDIR /app

COPY requirements-dev.txt .

RUN /opt/venv/bin/pip install --no-cache-dir -r requirements-dev.txt

COPY backend/. .
COPY pyproject.toml .

CMD ["pytest", "-n", "auto"]


FROM python:3.10-slim-buster as production
WORKDIR /app

EXPOSE 8080

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

COPY --from=base /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY backend/. .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
