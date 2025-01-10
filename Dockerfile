FROM python:3.12-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjemalloc2 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set up jemalloc
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2

# Install Poetry
ENV POETRY_VERSION=2.0.0
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock ./

# Project initialization
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --no-dev

# Copy project
COPY . .

# Build and install the project
RUN poetry build && pip install dist/*.whl

# Run stage
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages and built project from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app/dist/*.whl /app/

# Install jemalloc
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjemalloc2 \
    && rm -rf /var/lib/apt/lists/*

# Set up jemalloc
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2

# Install the project
RUN pip install --no-cache-dir /app/*.whl

CMD ["python", "bot.py"]
