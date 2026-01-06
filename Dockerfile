# Multi-stage Dockerfile for Django app with optional PostgreSQL support
# Usage:
#  - To use SQLite (default): no extra env vars needed.
#  - To use PostgreSQL: set DATABASE_ENGINE=postgres (or postgresql) and
#    POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT.
#
# This image expects an entrypoint script at ./entrypoint.sh (copied below).
# See: entrypoint.sh (project) -> [entrypoint.sh](entrypoint.sh)
FROM python:3.11-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Build deps for packages that may require compilation (psycopg2 etc.)
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-dev linux-headers

# Copy requirements and build wheels to avoid building in final image
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt psycopg2-binary

# --- Final stage ---
FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Default Django settings module used by manage.py in this repo
ENV DJANGO_SETTINGS_MODULE=DialogueAnchor.settings
ENV USER_ID=1000

WORKDIR /usr/src/app

# Runtime system deps (libpq for Postgres, libffi)
RUN apk add --no-cache libpq libffi

# Create non-root user and static root dir
RUN addgroup -S appgroup && adduser -S appuser -G appgroup -u ${USER_ID} \
    && mkdir -p /vol/web/static \
    && chown -R appuser:appgroup /vol/web

# Copy built wheels and install all python deps
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/* || pip install --no-cache -r requirements.txt

# Copy project files
COPY . .

# 複製 entrypoint
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# 強制將 Windows 換行符轉為 Linux 換行符 (關鍵！)
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh && \
    chown appuser:appgroup /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Use non-root user
RUN chown -R appuser:appgroup /usr/src/app
USER appuser

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "DialogueAnchor.wsgi:application"]