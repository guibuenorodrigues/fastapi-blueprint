# Stage 1: Builder - for installing dependencies with uv
FROM python:3.13-slim AS builder

# Copy uv binaries from a specific, stable version to ensure consistent builds
# Use a specific version tag instead of 'latest' for better reproducibility
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables for uv and Python during the build stage
ENV UV_COMPILE_BYTECODE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.13 \
    UV_PROJECT_ENVIRONMENT=/uv_env

# Create a dedicated directory for dependencies to ensure cleaner separation
WORKDIR /tmp/deps

# Copy only the necessary files for dependency resolution
# This is crucial for build cache invalidation: if only pyproject.toml/uv.lock change, this layer rebuilds.
COPY pyproject.toml uv.lock ./

# Install dependencies into /app within the builder stage
# Use a non-root user if possible during build for better security practices,
# though 'uv sync' might require root for creating /app initially.
RUN --mount=type=cache,target=/root/.cache \
    uv sync \
        --locked \
        --no-dev \
        --no-install-project

# Stage 2: Runner - the final, lean image for production
# Use the same base image as the builder for compatibility, but without the build tools
FROM python:3.13-slim AS runner

# Set production environment variables
ENV UV_COMPILE_BYTECODE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.13

# Copy only the compiled Python environment from the builder stage
# This dramatically reduces the final image size by excluding uv, cache, build artifacts, etc.
COPY --from=builder /uv_env /uv_env

# Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the application code
WORKDIR /app

COPY . .

# RUN chmod +x ./startup.sh

# Set the PATH for the uv-managed environment
ENV PATH=/uv_env/bin:$PATH

# Command to run your FastAPI application
# Ensure 'fastapi' is installed as part of your uv dependencies
CMD ["fastapi", "run", "src/main.py", "--port", "80"]
