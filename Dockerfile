# syntax=docker/dockerfile:1


FROM python:3.10-slim-buster AS apibase
WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN /opt/venv/bin/pip install --upgrade pip setuptools wheel
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt



FROM apibase AS apitest
WORKDIR /app

COPY requirements-dev.txt .

RUN /opt/venv/bin/pip install --no-cache-dir -r requirements-dev.txt

COPY backend/. .
COPY pyproject.toml .

CMD ["pytest", "-n", "auto"]



FROM python:3.10-slim-buster as apiproduction
WORKDIR /app

EXPOSE 8080

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

COPY --from=apibase /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY backend/. .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]



FROM node:lts-alpine  AS webbuild
WORKDIR /app

COPY ./frontend/. .

RUN npm ci
RUN npm run build



FROM nginx:stable-alpine as webproduction
WORKDIR /app

COPY --from=webbuild /app/dist /usr/share/nginx/html
COPY ./frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]