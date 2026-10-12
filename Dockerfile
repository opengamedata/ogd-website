# syntax=docker/dockerfile:1

# STAGE 1: setup dependencies
FROM python:3.12-slim-trixie AS setup
WORKDIR /app

# 1. Set up a venv for easy copying
RUN python -m venv ./.venv
ENV PATH="/app/.venv/bin:$PATH"

# 2. Install reqs into venv
#   Mount, rather than copy, reqs file for installing
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt
RUN --mount=type=bind,source=requirements-production.txt,target=requirements-production.txt \
    pip install -r requirements-production.txt

# STAGE 2: setup scripts & styling
FROM node:26-trixie-slim AS css
WORKDIR /app

COPY src/ ./src
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    npm install
# Need to install gulp package before we can run the build
RUN apt-get update && apt-get install -y gulp
RUN --mount=type=bind,source=gulpfile.js,target=gulpfile.js \
    gulp build

# STAGE 3: Create final image
FROM python:3.12-slim-trixie
WORKDIR /app

# 1. Copy venv from setup stage
COPY --from=setup                                       /app/.venv      ./.venv
COPY --from=css   --exclude=/app/src/assets/styles/scss /app/src/assets ./assets

ENV PATH="/app/.venv/bin:$PATH"

COPY --exclude=assets src/ ./
# Remove redundant copy of the package code
COPY config/AppConfig.py ./AppConfig.py
COPY config/game_list.json ./game_list.json

CMD ["gunicorn", \
     "--bind",    ":8080", \
     "--workers", "1", \
     "--threads", "8", \
     "--timeout", "0", \
     "app:application" \
]