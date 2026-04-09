# Dockerfile for SUBIT-NOUS

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (optional, for PDF support)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the package source
COPY src/ ./src/
COPY pyproject.toml .
COPY README.md .

# Install the package in development mode (or we could do a proper build)
RUN pip install --no-cache-dir -e .

# Expose API port
EXPOSE 8000

# Default command: show help
ENTRYPOINT ["nous"]
CMD ["--help"]