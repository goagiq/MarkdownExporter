# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies including Node.js and npm
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    nodejs \
    npm \
    fonts-liberation \
    fonts-dejavu-core \
    fonts-dejavu-extra \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Chromium for Mermaid CLI
RUN apt-get update \
    && apt-get install -y chromium \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable for Puppeteer to use Chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Install Mermaid CLI globally
RUN npm install -g @mermaid-js/mermaid-cli

# Verify mmdc installation and make it accessible
RUN mmdc --version && which mmdc

# Copy requirements and install Python dependencies
COPY pyproject.toml ./
COPY README.md ./
RUN pip install --no-cache-dir -e .

# Copy application code
COPY src/ ./src/
COPY config.yaml ./
COPY simple_mcp_server.py ./
COPY simple_api_server.py ./
COPY src/mcp/ ./src/mcp/

# Create necessary directories
RUN mkdir -p results results/images output temp

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose ports
EXPOSE 8001

# Health check - check both API docs and MCP endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/docs && curl -f http://localhost:8001/health/ || exit 1

# Default command - start the simple MCP server
CMD ["python", "simple_mcp_server.py"]
