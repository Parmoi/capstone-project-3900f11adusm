# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-alpine as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /server

ENV FLASK_APP=server.py
ENV PYTHONPATH "${PYTHONPATH}:/server/main"
ENV PYTHONPATH "${PYTHONPATH}:/server/main/database"
ENV PYTHONPATH "${PYTHONPATH}:/server/helpers"
ENV PYTHONPATH "${PYTHONPATH}:/server/mock_data"

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
COPY requirements.txt .

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD python3 -m flask run --host=0.0.0.0

