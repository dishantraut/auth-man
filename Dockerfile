# Stage 1: Build Dependencies
FROM python:3.10.16-alpine3.21 as build

# Install system dependencies required for Flask, SQLAlchemy, and Flask-Pydantic
RUN apk add --no-cache \
    postgresql-dev \
    libffi-dev \
    gcc \
    musl-dev \
    bash \
    py3-toml

# Create virtual environment and install Python dependencies
COPY ./requirements.txt /tmp/requirements.txt
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt


########## * Stage 2: Final Image * ##########
FROM python:3.10.16-alpine3.21

ENV PYTHONUNBUFFERED=1
ENV PATH="/py/bin:$PATH"

# Install runtime dependencies only
RUN apk add --no-cache \
    postgresql-client \
    mariadb-connector-c \
    libjpeg-turbo \
    zlib \
    freetype \
    bash \
    py3-toml

# Copy virtual environment from the build stage
COPY --from=build /py /py

# Copy application code
COPY ./app /app
WORKDIR /app

# Add a non-root user
RUN adduser --disabled-password --no-create-home flask-user
USER flask-user

# Expose port and define entrypoint
EXPOSE 8000

# CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.main:app"]

# End of Dockerfile