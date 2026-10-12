# syntax=docker/dockerfile:1

# STAGE 1: setup dependencies
FROM python:3.12-slim-trixie AS setup

# 1. Set up a venv for easy copying
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# 2. Install reqs into venv
#   Mount, rather than copy, reqs file for installing
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt
RUN --mount=type=bind,source=requirements-production.txt,target=requirements-production.txt \
    pip install -r requirements-production.txt

# STAGE 2: Create final image
FROM python:3.12-slim-trixie
WORKDIR /app

# 1. Copy venv from setup stage
COPY --from=setup /app/.venv ./.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ ./
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