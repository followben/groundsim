FROM python:3.10-slim-buster AS build
WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN /opt/venv/bin/pip install --upgrade pip setuptools wheel
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.10-slim-buster
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY main.py main.py
COPY tracking.json tracking.json
COPY api api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
