###########################################
# STAGE 1: BUILD (install deps)
###########################################
FROM python:3.12-slim AS builder
WORKDIR /app

# Install build-time tools
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

###########################################
# STAGE 2: RUNTIME (slim, secure, full Python)
###########################################
FROM python:3.12-slim

# Install runtime tools (curl for health checks)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /app /app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run app
CMD ["python", "app.py"]